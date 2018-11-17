# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import time
import cv2
import math
import datetime
import os
import glob
import re
import sys

from picamera import PiCamera, PiCameraError
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from hashlib import md5
from shutil import copyfile

from terrariumUtils import terrariumUtils

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWebcamSource(object):
  # Class defaults
  TILE_SIZE = 256
  TILE_LOCATION = 'webcam/'
  ARCHIVE_LOCATION = TILE_LOCATION + 'archive/'
  JPEG_QUALITY = 95
  FONT_SIZE = 10
  RETRIES = 3
  WARM_UP = 2
  OFFLINE = 'offline'
  ONLINE = 'online'
  UPDATE_TIMEOUT = 60
  VALID_ROTATIONS = ['0','90','180','270','h','v']

  def __init__(self, webcam_id, location, name = '', rotation = '0', width = 640, height = 480, archive = False, archive_light = 'ignore', archive_door = 'ignore', environment = None):
    # Variables per webcam
    self.raw_image = None

    # 'Hidden' variables
    self.__max_zoom = 0
    self.__last_update = 0
    self.__last_archive = 0

    self.__running = False
    self.__previous_image = None
    self.__state = None
    self.__environment = environment

    # Per webcam config
    self.set_location(location)
    self.set_name(name)
    self.set_resolution(width,height)
    self.set_rotation(rotation)
    self.set_archive(archive)
    self.set_archive_light(archive_light)
    self.set_archive_door(archive_door)

    if webcam_id is None:
      self.__id = md5(self.get_location().encode()).hexdigest()
    else:
      self.__id = id

    logger.info('Initialized %s webcam \'%s\' on location %s' %
                (self.get_type(),
                 self.get_name(),
                 self.get_location()))

    self.update()

  def __set_timestamp(self,image):
    # Get the image dimensions
    source_width, source_height = image.size
    # Select font
    font = ImageFont.truetype('fonts/DejaVuSans.ttf',terrariumWebcamSource.FONT_SIZE)
    # Draw on image
    draw = ImageDraw.Draw(image)
    # Create black box on the bottom of the image
    draw.rectangle([0,source_height-(terrariumWebcamSource.FONT_SIZE+2),source_width,source_height],fill='black')
    # Draw the current time stamp on the image
    draw.text((1, source_height-(terrariumWebcamSource.FONT_SIZE+1)), self.name + ' @ ' + (datetime.datetime.now()).strftime('%d/%m/%Y %H:%M:%S') ,(255,255,255),font=font)

  def __tile_image(self):
    starttime = time.time()
    # Original width
    source_width, source_height = self.raw_image.size

    # Calc new square canvas size
    longest_side = float(source_width if source_width > source_height else source_height)
    max_size = float(math.pow(2,math.ceil(math.log(longest_side,2))))

    # Set canvas dimensions
    canvas_width = canvas_height = max_size
    resize_factor = max_size / longest_side
    # Set raw image new dimensions
    source_width *= resize_factor
    source_height *= resize_factor

    # Calculate the max zoom factor
    zoom_factor = int(math.log(max_size/terrariumWebcamSource.TILE_SIZE,2))
    self.__max_zoom = zoom_factor
    logger.debug('Tiling image with source resolution %s, from %sx%s with resize factor %s in %s steps' %
                  (self.resolution, source_width,source_height,resize_factor, zoom_factor))

    # as long as there is a new layer, continue
    while zoom_factor >= 0:
      # Create black canvas on zoom factor dimensions
      logger.debug('Creating new black canvas with dimensions %sx%s' % (canvas_width,canvas_height))
      canvas = Image.new("RGB", ((int(round(canvas_width)),int(round(canvas_height)))), "black")
      # Scale the raw image to the zoomfactor dimensions
      logger.debug('Scale raw image to new canvas size (%sx%s)' % (canvas_width,canvas_height))
      source = self.raw_image.resize((int(round(source_width)),int(round(source_height))))
      # Set the timestamp on resized image
      self.__set_timestamp(source)

      # Calculate the center in the canvas for pasting raw image
      paste_center_position = (int(round((canvas_width - source_width) / 2)),int(round((canvas_height - source_height) / 2)))
      logger.debug('Pasting resized image to center of canvas at position %s' % (paste_center_position,))
      canvas.paste(source,paste_center_position)

      # Loop over the canvas to create the tiles
      logger.debug('Creating the lose tiles with dimensions %sx%s' % (canvas_width, canvas_height,))
      for row in range(0,int(math.ceil(canvas_height/terrariumWebcamSource.TILE_SIZE))):
        for column in range(0,int(math.ceil(canvas_width/terrariumWebcamSource.TILE_SIZE))):
          crop_size = ( int(row*terrariumWebcamSource.TILE_SIZE), int(column*terrariumWebcamSource.TILE_SIZE) ,int((row+1)*terrariumWebcamSource.TILE_SIZE), int((column+1)*terrariumWebcamSource.TILE_SIZE))
          logger.debug('Cropping image from position %s' % (crop_size,))
          tile = canvas.crop(crop_size)
          logger.debug('Saving cropped image to %s' % (terrariumWebcamSource.TILE_LOCATION + self.__id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg',))
          tile.save(terrariumWebcamSource.TILE_LOCATION + self.__id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg','jpeg',quality=terrariumWebcamSource.JPEG_QUALITY)
          logger.debug('Done saving %s' % (terrariumWebcamSource.TILE_LOCATION + self.__id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg',))

      # Scale down by 50%
      canvas_width /= 2.0
      canvas_height /= 2.0
      source_width /= 2.0
      source_height /= 2.0
      zoom_factor -= 1

    logger.debug('Done tiling webcam image \'%s\' in %.5f seconds' % (self.get_name(),time.time()-starttime))

  def set_offline_image(self):

    def draw_text_center(im, draw, text, font, **kwargs):
      text_height = text_top = None
      linecounter = 0
      for line in text:
        text_size = draw.textsize(line, font)
        if text_height is None:
          text_height = len(text) * ( text_size[1])
          text_top = (im.size[1] - text_height) / 2

        draw.text(
          ((im.size[0] - text_size[0]) / 2, (text_top + (linecounter * text_height)) / 2),
          line, font=font, **kwargs)

        linecounter += 1

    self.raw_image = Image.open('static/images/webcam_offline.png')

    mask = Image.open('static/images/mask_offline.png')
    draw = ImageDraw.Draw(mask)
    font = ImageFont.truetype('fonts/DejaVuSans.ttf',40)
    text = [_('Offline since') + ':',datetime.datetime.now().strftime('%A %d %B %Y'),datetime.datetime.now().strftime('%H:%M:%S')]
    draw_text_center(mask,draw,text,font)

    mask_width, mask_height = mask.size
    source_width, source_height = self.raw_image.size

    self.raw_image.paste(mask, ((source_width/2)-(mask_width/2),(source_height/2)-(mask_height/2)), mask)

  def get_archive_images(self):
    regex = r'(' + terrariumWebcamSource.ARCHIVE_LOCATION + ')\d+/\d+/\d+/([^_]+_archive_)\d+(\..*)'
    subst = '\\1*/*/*/\\2*\\3'
    file_filter = re.sub(regex, subst, self.get_raw_image(True))
    files = glob.glob(file_filter)
    files.sort(key=os.path.getmtime,reverse = True)
    return files

  def archive_image(self):
    if self.get_archive() != 'disabled' and \
         ((self.get_archive_light() == 'ignore' or \
           self.get_archive_light() == 'on'     and self.__environment is not None and self.__environment.light_on() or \
           self.get_archive_light() == 'off'    and self.__environment is not None and not self.__environment.light_on()) and \
          (self.get_archive_door()  == 'ignore' or \
           self.get_archive_door()  == 'open'   and self.__environment is not None and self.__environment.is_door_open() or \
           self.get_archive_door()  == 'closed' and self.__environment is not None and not self.__environment.is_door_open())):

      archive_image = self.get_raw_image(True)
      if not os.path.isdir(os.path.dirname(archive_image)):
        try:
          os.makedirs(os.path.dirname(archive_image))
        except Exception as ex:
          pass

      if self.get_archive() == 'motion':
        # https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
        try:
          current_image = cv2.imread(self.get_raw_image())
          current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
          current_image = cv2.GaussianBlur(current_image, (21, 21), 0)

          # Reset previous image. This is needed/happening when resolution of image changes due to rotation or settings update
          if self.__previous_image is None or self.__previous_image.shape[0] != current_image.shape[0] or self.__previous_image.shape[1] != current_image.shape[1]:
            self.__previous_image = current_image

          thresh = cv2.threshold(cv2.absdiff(self.__previous_image, current_image), 25, 255, cv2.THRESH_BINARY)[1]
          thresh = cv2.dilate(thresh, None, iterations=2)

          cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
          if sys.version_info.major == 2:
            # On pyton2 we use OpenCV2. Is different then Python 3 with OpenCV3
            (cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
          elif sys.version_info.major == 3:
            # On pyton2 we use OpenCV2. Is different then Python 3 with OpenCV3
            (_,cnts,__) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

          self.__previous_image = current_image
          motion_detected = False
          raw_image = cv2.imread(self.get_raw_image())
          # loop over the contours
          for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
              continue

            motion_detected = True
            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(raw_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

          if motion_detected:
            cv2.imwrite(archive_image,raw_image)
            logger.info('Saved webcam %s image for archive due to motion detection' % (self.get_name(),))
            self.__last_update = int(time.time())
            self.__environment.notification.message('webcam_motion',self.get_data(),[archive_image])

        except Exception as ex:
          logger.exception('Error in motion detection for webcam \'%s\' with error message: %s' % (self.get_name(),ex))

      elif int(time.time()) - self.__last_archive >= int(self.get_archive()):
        copyfile(self.get_raw_image(),archive_image)
        logger.info('Saved webcam %s image for archive due to timer interval %s seconds' % (self.get_name(),self.get_archive()))
        self.__last_archive = int(time.time())
        self.__last_update = int(time.time())
        self.__environment.notification.message('webcam_motion',self.get_data(),[archive_image])

  def rotate_image(self):
    # Rotate image if needed
    if '90' == self.get_rotation():
      self.raw_image = self.raw_image.transpose(Image.ROTATE_90)
    elif  '180' == self.get_rotation():
      self.raw_image = self.raw_image.transpose(Image.ROTATE_180)
    elif '270' == self.get_rotation():
      self.raw_image = self.raw_image.transpose(Image.ROTATE_270)
    elif 'h' == self.get_rotation():
      self.raw_image = self.raw_image.transpose(Image.FLIP_TOP_BOTTOM)
    elif 'v' == self.get_rotation():
      self.raw_image = self.raw_image.transpose(Image.FLIP_LEFT_RIGHT)

    logger.debug('Rotated raw image %s to %s' % (self.get_name(),self.get_rotation()))

  def update(self):
    starttime = time.time()
    if not self.__running and ((int(starttime) - self.get_last_update()) >= terrariumWebcamSource.UPDATE_TIMEOUT):
      self.__running = True
      logger.debug('Start getting raw image data for webcam \'%s\' from location: \'%s\'' % (self.get_name(),self.get_location(),))

      state = terrariumWebcamSource.OFFLINE
      for trying in range(0,terrariumWebcamSource.RETRIES):
        try:
          if self.get_raw_data():
            # Webcam is online
            state = terrariumWebcamSource.ONLINE
            # "Rewind" the stream to the beginning so we can read its content
            logger.debug('Resetting raw image %s' % (self.get_name(),))
            self.raw_image.seek(0)
            # Store image in memory for further processing
            self.raw_image = Image.open(self.raw_image)
            logger.debug('Loaded raw image %s to memory' % (self.get_name(),))
            # Rotate image if needed
            self.rotate_image()
            # Store copy on disk
            self.raw_image.save(self.get_raw_image(),'jpeg',quality=terrariumWebcamSource.JPEG_QUALITY)
            logger.debug('Saved raw image %s to disk: %s' % (self.get_name(),self.get_raw_image()))
            # Store archive image if needed based on time or motion and door detection
            self.archive_image()
            # Tile the images for Leaflet.js
            self.__tile_image()
            break

        except Exception as ex:
          pass

      if self.get_state() != state and state == terrariumWebcamSource.OFFLINE:
        logger.error('Raw image \'%s\' at location %s is not available!' % (self.get_name(),self.get_location(),))
        # Set the offline message
        self.set_offline_image()
        # Store copy on disk
        self.raw_image.save(self.get_raw_image(),'jpeg',quality=terrariumWebcamSource.JPEG_QUALITY)
        # Tile the images for Leaflet.js
        self.__tile_image()

      self.__state = state
      self.__last_update = int(starttime)
      self.__running = False
      logger.info('Done updating webcam \'%s\' at location %s in %.5f seconds' % (self.get_name(), self.get_location(),time.time()-starttime))

  def get_raw_image(self):
    self.set_offline_image()
    return True

  def get_data(self,archive = False):
    data = {'id': self.get_id(),
            'location': self.get_location(),
            'name': self.get_name(),
            'rotation' : self.get_rotation(),
            'resolution': self.get_resolution(),
            'max_zoom' : self.get_max_zoom(),
            'state' : self.get_state(),
            'last_update' : self.get_last_update(),
            'image': self.get_raw_image(),
            'preview': self.get_preview_image(),
            'archive': self.get_archive(),
            'archivelight': self.get_archive_light(),
            'archivedoor': self.get_archive_door(),
            'archive_images' : []
            }

    if archive:
      data['archive_images'] = self.get_archive_images()

    return data

  def get_id(self):
    return self.__id

  def get_type(self):
    return None

  def get_name(self):
    return self.name

  def set_name(self,name):
    self.name = name

  def get_location(self):
    return self.location

  def set_location(self,location):
    self.location = location

  def get_rotation(self):
    return self.rotation

  def set_rotation(self,rotation):
    if rotation in terrariumWebcamSource.VALID_ROTATIONS:
      self.rotation = rotation

  def set_resolution(self,width,height):
    try:
      self.resolution = {'width'  : int(width),
                         'height' : int(height)}
    except Exception as ex:
      self.resolution = {'width'  : 640,
                         'height' : 480}

  def get_resolution(self):
    return self.resolution

  def get_max_zoom(self):
    return self.__max_zoom

  def get_archive(self):
    return self.archive

  def set_archive(self,enabled):
    self.archive = enabled

  def get_archive_light(self):
    return self.archive_light_state

  def set_archive_light(self,state):
    self.archive_light_state = state

  def set_archive_door(self,state):
    self.archive_door_state = state

  def get_archive_door(self):
    return self.archive_door_state

  def get_state(self):
    return self.__state

  def get_last_update(self):
    return self.__last_update

  def get_raw_image(self,archive = False):
    image = terrariumWebcamSource.TILE_LOCATION + self.get_id() + '_raw.jpg'
    if archive:
      image = terrariumWebcamSource.ARCHIVE_LOCATION + (datetime.datetime.now()).strftime("%Y/%m/%d") + '/' + self.get_id() + '_archive_' + str(int(time.time())) + '.jpg'

    return image

  def get_preview_image(self):
    return terrariumWebcamSource.TILE_LOCATION + self.get_id() + '_tile_0_0_0.jpg'

class terrariumWebcamRPI(terrariumWebcamSource):
  TYPE = 'rpicam'
  VALID_SOURCE = '^rpicam$'

  def set_resolution(self,width,height):
    self.resolution = {'width' : 1920,
                       'height' : 1080}

  def get_raw_data(self):
    logger.debug('Using RPICAM')
    stream = BytesIO()
    try:
      with PiCamera(resolution=(self.resolution['width'], self.resolution['height'])) as camera:
        logger.debug('Open rpicam')
        camera.start_preview()
        logger.debug('Wait %s seconds for preview' % (terrariumWebcamSource.WARM_UP,))
        time.sleep(terrariumWebcamSource.WARM_UP)
        logger.debug('Save rpicam to jpeg')
        camera.capture(stream, format='jpeg')
        logger.debug('Done creating RPICAM image')
        self.raw_image = stream
        return True
    except PiCameraError:
      logger.exception('Error getting raw RPI image from webcam \'%s\' with error message:' % (self.get_name(),))

    return False

  def get_type(self):
    return terrariumWebcamRPI.TYPE

  def get_location(self):
    return terrariumWebcamRPI.VALID_SOURCE[1:-1]

class terrariumWebcamUSB(terrariumWebcamSource):
  TYPE = 'usb'
  VALID_SOURCE = '^/dev/video\d+'

  def get_raw_data(self):
    logger.debug('Using USB device: %s' % (self.location,))
    readok = False
    stream = BytesIO()
    camera = None

    try:
      logger.debug('Open USB')
      camera = cv2.VideoCapture(int(self.location[10:]))
      logger.debug('Set USB height')
      camera.set(3, float(self.resolution['width']))
      logger.debug('Set USB width')
      camera.set(4, float(self.resolution['height']))
      logger.debug('Wait %s seconds for preview' % (terrariumWebcamSource.WARM_UP,))
      time.sleep(terrariumWebcamSource.WARM_UP)
      logger.debug('Save USB to raw data')
      readok, image = camera.read()

      if readok:
        logger.debug('Save USB to jpeg')
        jpeg = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        jpeg.save(stream,'JPEG')
        logger.debug('Done creating USB image')
        self.raw_image = stream

      logger.debug('Release USB camera')
      camera.release()
      logger.debug('Done release USB camera')
      return True

    except Exception:
      logger.exception('Error getting raw USB image from webcam \'%s\' with error message:' % (self.get_name(),))

    return False

  def get_type(self):
    return terrariumWebcamUSB.TYPE

class terrariumWebcamRemote(terrariumWebcamSource):
  TYPE = 'remote'
  VALID_SOURCE = '^http(s)?://'

  def get_raw_data(self):
    logger.debug('Using URL: %s' % (self.location,))
    try:
      remote_image = terrariumUtils.get_remote_data(self.location)
      if remote_image is None:
        raise terrariumWebcamRAWUpdateException()

      self.raw_image = BytesIO(remote_image)
      return True
    except terrariumWebcamRAWUpdateException as ex:
      logger.warning('Error getting raw online image from webcam \'%s\' with error message: %s' % (self.get_name(),ex))

    return False

  def get_type(self):
    return terrariumWebcamRemote.TYPE

class terrariumWebcamSourceException(Exception):
  '''The entered online webcam source is not known or invalid'''

class terrariumWebcamRAWUpdateException(Exception):
  '''The entered online webcam source is not available'''

# Factory class
class terrariumWebcam(object):
  SOURCES = {terrariumWebcamRPI,
             terrariumWebcamUSB,
             terrariumWebcamRemote}

  def __new__(self,webcam_id, location, name = '', rotation = '0', width = 640, height = 480, archive = False, archive_light = 'ignore', archive_door = 'ignore', environment = None):
    for webcam_source in terrariumWebcam.SOURCES:
      if re.search(webcam_source.VALID_SOURCE, location, re.IGNORECASE):
        return webcam_source(webcam_id,location,name,rotation,width,height,archive,archive_light,archive_door,environment)

    raise terrariumWebcamSourceException()
