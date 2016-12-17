# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from time import time
from io import BytesIO
import StringIO

from picamera import PiCamera
import cv2
from PIL import Image, ImageDraw, ImageFont

from hashlib import md5
import math
from datetime import datetime

import urllib2
import base64

from gevent import monkey, sleep
monkey.patch_all()

class terrariumWebcam():

  def __init__(self, id = None, location = '', name = '', rotation = None):
    if id is None:
      self.id = md5(b'' + str(int(time()))).hexdigest()
    else:
      self.id = id

    # Main config
    self.tile_size = 256 # Smaller tile sizes does not work with LeafJS
    self.tile_location = 'webcam/'
    self.font_size = 10

    # Per webcam config
    self.set_location(location)
    self.set_name(name)
    self.set_rotation(rotation)

    self.max_zoom = 0
    self.raw_image = None
    self.resolution = None
    self.last_update = None
    self.state = None

    self.update()

  def __get_raw_image(self):
    logger.debug('Start getting raw image data from location: %s' % (self.location,))
    stream = BytesIO()

    try:
      if 'rpicam' == self.location:
        logger.debug('Using RPICAM')
        with PiCamera(resolution=(1920, 1080)) as camera:
          logger.debug('Open rpicam')
          camera.start_preview()
          logger.debug('Wait 2 seconds for preview')
          sleep(2)
          logger.debug('Save rpicam to jpeg')
          camera.capture(stream, format='jpeg')
          logger.debug('Done creating RPICAM image')

      elif self.location.startswith('/dev/video'):
        logger.debug('Using USB')
        logger.debug('Open USB')
        camera = cv2.VideoCapture(int(self.location[10:]))
        logger.debug('Set USB height to 1280')
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
        logger.debug('Set USB width to 720')
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
        logger.debug('Wait 2 seconds for preview')
        sleep(2)
        logger.debug('Save USB to raw data')
        readok, image = camera.read()

        if readok:
          logger.debug('Save USB to jpeg')
          jpeg = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
          stream = StringIO.StringIO()
          jpeg.save(stream,'JPEG')
          logger.debug('Done creating USB image')

        logger.debug('Release USB camera')
        camera.release()
        logger.debug('Done release USB camera')

      elif self.location.startswith('http://') or self.location.startswith('https://'):
        logger.debug('Using URL')
        if '@' in self.location:
          start = self.location.find('://') + 3
          end = self.location.find('@', start)
          auth = self.location[start:end]
          webcamurl = urllib2.Request(self.location.replace(auth+'@',''))
          auth = auth.split(':')
          base64string = base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
          webcamurl.add_header("Authorization", "Basic %s" % base64string)
        else:
          webcamurl = urllib2.Request(self.location)

        stream = StringIO.StringIO(urllib2.urlopen(webcamurl,None,15).read())

      self.state = True

      # "Rewind" the stream to the beginning so we can read its content
      logger.debug('Reset raw image')
      stream.seek(0)
      # Store image in memory for further processing
      logger.debug('Copy raw image to memory')
      self.raw_image = Image.open(stream)

      # Rotate image if needed
      logger.debug('Rotate image at %s' % (self.get_rotation(),))
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

      logger.debug('Saving image to disc: %s' % (self.get_raw_image(),))
      self.raw_image.save(self.get_raw_image(),'jpeg',quality=95)
      logger.debug('Done saving image to disc: %s' % (self.get_raw_image(),))

    except Exception, err:
      # Error loadig image, so load offline image
      if self.state is not False:
        logger.warning('Image at location %s is not available. Exception: %s' % (self.location,err,))
        self.__get_offline_image()
        self.state = False

    self.last_update = int(time())

  def __get_offline_image(self):

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
    text = ['Offline since:',datetime.now().strftime("%A %d %B %Y"),datetime.now().strftime("%H:%M:%S")]
    draw_text_center(mask,draw,text,font)

    mask_width, mask_height = mask.size
    source_width, source_height = self.raw_image.size

    self.raw_image.paste(mask, ((source_width/2)-(mask_width/2),(source_height/2)-(mask_height/2)), mask)

  def __set_timestamp(self,image):
    # Get the image dimensions
    source_width, source_height = image.size
    # Select font
    font = ImageFont.truetype('fonts/DejaVuSans.ttf',self.font_size)
    # Draw on image
    draw = ImageDraw.Draw(image)
    # Create black box on the bottom of the image
    draw.rectangle([0,source_height-(self.font_size+2),source_width,source_height],fill='black')
    # Draw the current timestamp on the image
    draw.text((1, source_height-(self.font_size+1)), self.name + ' @ ' + (datetime.now()).strftime("%d/%m/%Y %H:%M:%S") ,(255,255,255),font=font)
    del draw

  def __tile_image(self):
    # Original width
    source_width, source_height = self.raw_image.size
    self.resolution = self.raw_image.size

    # Calc new square canvas size
    longest_side = float(source_width if source_width > source_height else source_height)
    max_size = float(math.pow(2,math.ceil(math.log(longest_side,2))))

    # Set canvas dimensions
    canvas_width = canvas_height = max_size
    resize_factor = max_size / longest_side
    # Set raw image new dimensions
    source_width *= resize_factor
    source_height *= resize_factor

    # Calculate the max zoomfactor
    zoom_factor = int(math.log(max_size/self.tile_size,2))
    self.max_zoom = zoom_factor
    logger.debug('Tileing image with source resolution %s, from %sx%s with resize factor %s in %s steps' %
                  (self.resolution, source_width,source_height,resize_factor, zoom_factor))

    # as long as there is a new layer, continue
    while zoom_factor >= 0:
      # Create black canvas on zoom factor dimensions
      logger.debug('Createing new black canvas with dimensions %sx%s' % (canvas_width,canvas_height))
      canvas = Image.new("RGB", ((int(round(canvas_width)),int(round(canvas_height)))), "black")
      # Scale the raw image to the zoomfactor dimensions
      logger.debug('Scale raw image to new canvas size (%sx%s)' % (canvas_width,canvas_height))
      source = self.raw_image.resize((int(round(source_width)),int(round(source_height))))
      # Set the timestamp on resized image
      logger.debug('Put timestamp on scaled image')
      self.__set_timestamp(source)

      # Calculate the center in the canvas for pasting raw image
      logger.debug('Calculate center position')
      paste_center_position = (int(round((canvas_width - source_width) / 2)),int(round((canvas_height - source_height) / 2)))
      logger.debug('Pasting resized image to center of canvas at position %s' % (paste_center_position,))
      canvas.paste(source,paste_center_position)

      # Loop over the canvas to create the tiles
      logger.debug('Creating the lose tiles with dimensions %sx%s' % (canvas_width, canvas_height,))
      for row in xrange(0,int(math.ceil(canvas_height/self.tile_size))):
        for column in xrange(0,int(math.ceil(canvas_width/self.tile_size))):
          crop_size = ( int(row*self.tile_size), int(column*self.tile_size) ,int((row+1)*self.tile_size), int((column+1)*self.tile_size))
          logger.debug('Cropping image from position %s' % (crop_size,))
          tile = canvas.crop(crop_size)
          logger.debug('Saving cropped image to %s' % (self.tile_location + self.id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg',))
          tile.save(self.tile_location + self.id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg','jpeg',quality=95)
          logger.debug('Done saving %s' % (self.tile_location + self.id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg',))

      # Scale down by 50%
      canvas_width /= 2.0
      canvas_height /= 2.0
      source_width /= 2.0
      source_height /= 2.0
      zoom_factor -= 1

    # Clear memory, not sure if needed
    del source
    del canvas

  def get_data(self):
    return {'id': self.get_id(),
            'location': self.get_location(),
            'name': self.get_name(),
            'rotation' : self.get_rotation(),
            'resolution': self.get_resolution(),
            'max_zoom' : self.get_max_zoom(),
            'state' : self.get_state(),
            'last_update' : self.get_last_update(),
            'image': self.get_raw_image(),
            'preview': self.get_preview_image()
            }

  def update(self):
    logger.info('Updating webcam %s at location %s' % (self.get_name(), self.get_location(),))
    self.__get_raw_image()
    self.__tile_image()
    logger.info('Done updating webcam %s at location %s' % (self.get_name(), self.get_location(),))

  def get_id(self):
    return self.id

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
    self.rotation = rotation

  def get_resolution(self):
    return self.resolution

  def get_max_zoom(self):
    return self.max_zoom

  def get_state(self):
    return 'online' if self.state else 'offline'

  def get_last_update(self):
    return self.last_update

  def get_raw_image(self):
    return self.tile_location + self.get_id() + '_raw.jpg'

  def get_preview_image(self):
    return self.tile_location + self.get_id() + '_tile_0_0_0.jpg'
