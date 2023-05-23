# -*- coding: utf-8 -*-
import terrariumLogging
logger = terrariumLogging.logging.getLogger(__name__)

import inspect
from importlib import import_module
import sys

from pathlib import Path
from hashlib import md5
from operator import itemgetter
from datetime import datetime, timedelta
from time import time
from gevent import sleep
from func_timeout import func_timeout, FunctionTimedOut

import math
#import glob
import cv2

# pip install retry
from retry import retry
# pip install Pillow
from PIL import Image, ImageDraw, ImageFont
# pip install piexif
import piexif

from terrariumUtils import terrariumUtils, terrariumCache, classproperty

class terrariumWebcamException(TypeError):

  '''There is a problem with loading a hardware switch. Invalid power switch action.'''

  def __init__(self, message, *args):
    self.message = message
    super().__init__(message, *args)

class terrariumWebcamLoadingException(terrariumWebcamException):
  pass

class terrariumWebcamUpdateException(terrariumWebcamException):
  pass

class terrariumWebcamActionException(terrariumWebcamException):
  pass

# https://www.bnmetrics.com/blog/factory-pattern-in-python3-simple-version
class terrariumWebcam(object):
  HARDWARE     = None
  NAME         = None
  VALID_SOURCE = None
  INFO_SOURCE  = None

  __STATIC_LOCATION  = Path(__file__).parent.parent.parent / 'webcam'

  #.parent.parent.joinpath('app/base/static/webcams/')
  _STORE_LOCATION   = Path('/dev/shm/webcam/')
  _TILE_LOCATION    = 'tiles/'
  __ARCHIVE_LOCATION = __STATIC_LOCATION / 'archive/'

  __TILE_SIZE = 256
  __JPEG_QUALITY = 95
  __FONT_SIZE = 10
  __OFFLINE = 'offline'
  __ONLINE = 'online'
  __UPDATE_TIMEOUT = 1
  __VALID_ROTATIONS = ['0','90','180','270','h','v']

  # Can be overridden in child classes if used.
  _WARM_UP = 2

  @classproperty
  def available_hardware(__cls__):
    __CACHE_KEY = 'known_webcams'
    cache = terrariumCache()

    data = cache.get_data(__CACHE_KEY)
    if data is None:
      data = {}
      # Start dynamically loading sensors (based on: https://www.bnmetrics.com/blog/dynamic-import-in-python3)
      for file in sorted(Path(__file__).parent.glob('*_webcam.py')):
        imported_module = import_module( '.' + file.stem, package='{}'.format(__name__))

        for i in dir(imported_module):
          attribute = getattr(imported_module, i)

          if inspect.isclass(attribute) and attribute != terrariumWebcam and issubclass(attribute, terrariumWebcam):
            setattr(sys.modules[__name__], file.stem, attribute)
            data[attribute.HARDWARE] = attribute

      cache.set_data(__CACHE_KEY,data,-1)

    return data

  @classproperty
  def available_webcams(__cls__):
    data = []
    for (hardware_type, webcam) in __cls__.available_hardware.items():
      data.append({'hardware' : hardware_type, 'name' : webcam.NAME})

    return sorted(data, key=itemgetter('name'))

  # Return polymorph webcam....
  def __new__(cls, _, hardware_type, address, name = '', rotation = '0', width = 640, height = 480, wb = 'auto'):
    known_webcams = terrariumWebcam.available_hardware

    if hardware_type not in known_webcams:
      raise terrariumWebcamException(f'Webcam of hardware type {hardware_type} is unknown.')

    return super(terrariumWebcam, cls).__new__(known_webcams[hardware_type])

  def __init__(self, device_id, _, address, name = '', width = 640, height = 480, rotation = '0', awb = 'auto'):
    """Create a new Webcam instance based on type"""

    self._device = {'device'      : None,
                    'id'          : None,
                    'address'     : None,
                    'name'        : None,
                    'rotation'    : None,
                    'resolution'  : None,
                    'awb'         : None,

                    'last_update' : None,
                    'state'       : True,
                    'max_zoom'    : None,}

    self.id = device_id

    self.name = name
    self.resolution = (width,height)
    self.rotation = rotation
    self.awb = awb

    self.__last_archive_image = self.__get_last_archive_image()
    self.__compare_image = None

    # This will trigger a load hardware call when the address changes
    self.address = address

    store_location = Path(self._STORE_LOCATION).joinpath(self.id)
    store_location.mkdir(parents=True,exist_ok=True)

    sym_link = self.__STATIC_LOCATION.joinpath(self.id)
    if not sym_link.is_symlink():
      sym_link.symlink_to(store_location,target_is_directory=True)

    if not self.live:
      store_location.joinpath(self._TILE_LOCATION).mkdir(parents=True,exist_ok=True)

  def __repr__(self):
    """
    Return a readable name back for the Webcam

    Returns:
        string: The webcam type and name with address
    """
    return f'{self.NAME} named \'{self.name}\' at address \'{self.address}\''

  @retry(tries=3, delay=0.5, max_delay=2)
  def load_hardware(self):
    try:
      hardware = self._load_hardware()
    except Exception as ex:
      raise terrariumWebcamLoadingException(f'Unable to load webcam {self}: {ex}.')

    if hardware is None:
      raise terrariumWebcamLoadingException(f'Unable to load webcam {self}: Did not return a device.')

    self._device['device'] = hardware

  def __get_last_archive_image(self):
    # Today archive path:
    archive = self.__ARCHIVE_LOCATION / self.id / f'{datetime.now().strftime("%Y/%m/%d")}'
    files = sorted(archive.glob('*.jpg'))
    if len(files) == 0:
      # Yesterday archive path:
      archive = self.__ARCHIVE_LOCATION / self.id / f'{(datetime.now()-timedelta(days=1)).strftime("%Y/%m/%d")}'
      files = sorted(archive.glob('*.jpg'))
      if len(files) == 0:
        # No archive files found in 24-48 hours history
        return None

    return files[-1]

  def __rotate(self):
    # Rotate image if needed
    if self.__raw_image is None:
      return

    if '90' == self.rotation:
      self.__raw_image = self.__raw_image.transpose(Image.Transpose.ROTATE_90)
    elif '180' == self.rotation:
      self.__raw_image = self.__raw_image.transpose(Image.Transpose.ROTATE_180)
    elif '270' == self.rotation:
      self.__raw_image = self.__raw_image.transpose(Image.Transpose.ROTATE_270)
    elif 'h' == self.rotation:
      self.__raw_image = self.__raw_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif 'v' == self.rotation:
      self.__raw_image = self.__raw_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    logger.debug('Rotated raw image %s to %s' % (self.name,self.rotation))

  def __set_timestamp(self, image):
    # Get the image dimensions
    source_width, source_height = image.size
    # Select font
    font = ImageFont.truetype('fonts/DejaVuSans.ttf',self.__FONT_SIZE)
    # Draw on image
    draw = ImageDraw.Draw(image)
    # Create black box on the bottom of the image
    draw.rectangle([0,source_height-(self.__FONT_SIZE+2),source_width,source_height],fill='black')
    # Draw the current time stamp on the image
    draw.text((1, source_height-(self.__FONT_SIZE+1)), ('NoName' if self.name is None else self.name) + ' @ ' + (datetime.now()).strftime('%d/%m/%Y %H:%M:%S') ,(255,255,255),font=font)

  def __tile_image(self):
    starttime = time()
    # Original width
    source_width, source_height = self.__raw_image.size

    # Calc new square canvas size
    longest_side = float(max(source_width,source_height))
    max_size     = float(math.pow(2,math.ceil(math.log(longest_side,2))))

    # Set canvas dimensions
    canvas_width  = canvas_height = max_size
    resize_factor = max_size / longest_side
    # Set raw image new dimensions
    source_width  *= resize_factor
    source_height *= resize_factor

    # Calculate the max zoom factor
    zoom_factor     = int(math.log(max_size/self.__TILE_SIZE,2))

    self._device['max_zoom'] = zoom_factor

    #self.__max_zoom = zoom_factor
    logger.debug('Tiling image with source resolution %s, from %sx%s with resize factor %s in %s steps' %
                  ('{}x{}'.format(self.width ,self.height), source_width,source_height,resize_factor, zoom_factor))

    if not self.live:
      self.raw_image_path.parent.joinpath(self._TILE_LOCATION).mkdir(parents=True,exist_ok=True)

    # as long as there is a new layer, continue
    while zoom_factor >= 0:
      # Create black canvas on zoom factor dimensions
      logger.debug('Creating new black canvas with dimensions %sx%s' % (canvas_width,canvas_height))
      canvas = Image.new("RGB", ((int(round(canvas_width)),int(round(canvas_height)))), "black")
      # Scale the raw image to the zoom factor dimensions
      logger.debug('Scale raw image to new canvas size (%sx%s)' % (canvas_width,canvas_height))
      start = time()
      source = self.__raw_image.resize((int(round(source_width)),int(round(source_height))))
      logger.debug(f'Resizing {self.name} image to {source_width}x{source_height} for tiling took: {time()-start:.2f} seconds')
      # Set the timestamp on resized image

      start = time()
      self.__set_timestamp(source)
      logger.debug(f'Setting correct timestamp image {self.name} took: {time()-start:.2f} seconds')

      # Calculate the center in the canvas for pasting raw image
      paste_center_position = (int(round((canvas_width - source_width) / 2)),int(round((canvas_height - source_height) / 2)))
      logger.debug('Pasting resized image to center of canvas at position %s' % (paste_center_position,))
      start = time()
      canvas.paste(source,paste_center_position)
      logger.debug(f'Pasting image {self.name} into canvas took: {time()-start:.2f} seconds')

      # Loop over the canvas to create the tiles
      logger.debug('Creating the lose tiles with dimensions %sx%s' % (canvas_width, canvas_height,))
      start2 = time()
      for row in range(0,int(math.ceil(canvas_height/self.__TILE_SIZE))):
        for column in range(0,int(math.ceil(canvas_width/self.__TILE_SIZE))):
          crop_size = ( int(row*self.__TILE_SIZE), int(column*self.__TILE_SIZE) ,int((row+1)*self.__TILE_SIZE), int((column+1)*self.__TILE_SIZE))
          #logger.debug('Cropping image from position %s' % (crop_size,))
          start = time()
          tile = canvas.crop(crop_size)
          logger.debug(f'Cropping image size: {crop_size} took: {time()-start:.2f} seconds')
          #logger.debug('Saving cropped image to %s' % (terrariumWebcamSource.TILE_LOCATION + self.__id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg',))

          tile_file_name = self.raw_image_path.parent.joinpath(self._TILE_LOCATION,'tile_{}_{}_{}.jpg'.format(zoom_factor,row,column))
          tile.save(tile_file_name,'jpeg',quality=self.__JPEG_QUALITY)
          logger.debug('Done saving {}'.format(tile_file_name))

      logger.debug(f'Webcam {self.name}: Done creating tiles in {time()-start2:.2f} seconds')

      # Scale down by 50%
      canvas_width /= 2.0
      canvas_height /= 2.0
      source_width /= 2.0
      source_height /= 2.0
      zoom_factor -= 1

    logger.debug('Done tiling webcam image \'%s\' in %.5f seconds' % (self.name,time()-starttime))

  def __set_offline_image(self):

    def draw_text_center(im, draw, text, font, **kwargs):
      text_height = text_top = None
      linecounter = 0
      for line in text:
        text_size = draw.textbbox((0,0), line, font, anchor='lt')
        if text_height is None:
          text_height = len(text) * ( text_size[3] + 6) # Add some top-bottom padding (+6)
          text_top = (im.size[1] - text_height) / 2

        draw.text(
          ((im.size[0] - text_size[2]) / 2, (text_top + (linecounter * text_height)) / 2),
          line, font=font, **kwargs)

        linecounter += 1

    raw_image = Image.open(Path(__file__).parent.joinpath('images/webcam_offline.png'))

    mask = Image.open(Path(__file__).parent.joinpath('images/mask_offline.png'))
    draw = ImageDraw.Draw(mask)
    font = ImageFont.truetype('fonts/DejaVuSans.ttf',40)
    text = ['Offline since' + ':',datetime.now().strftime('%A %d %B %Y'),datetime.now().strftime('%H:%M:%S')]
    draw_text_center(mask,draw,text,font)

    mask_width, mask_height = mask.size
    source_width, source_height = raw_image.size

    raw_image.paste(mask, (int((source_width/2)-(mask_width/2)),int((source_height/2)-(mask_height/2))), mask)

    # Upscale the error image, so the zoomfactors are still working...
    logger.debug('Resize error image from {}x{} to {}x{} keeping aspect ratio.'.format(source_width, source_height,self.width, self.height))
    raw_image.thumbnail( (self.width, self.height))

    return raw_image

  @property
  def __exit_data(self):
    # Add some exif data to the image
    zeroth_ifd = {
      piexif.ImageIFD.Artist: 'TerrariumPI',
      piexif.ImageIFD.XResolution: (self.width, 1),
      piexif.ImageIFD.YResolution: (self.height, 1),
      piexif.ImageIFD.Software: 'TerrariumPI',
      piexif.ImageIFD.ImageDescription: f'Webcam image from {self}',
      piexif.ImageIFD.DateTime: datetime.now().strftime('%Y-%m-%d %H:%m:%S'),
      piexif.ImageIFD.Copyright: f'(c) {datetime.now().year} - TerrariumPI',
    }
    exif_ifd = {
      piexif.ExifIFD.DateTimeOriginal: datetime.now().strftime('%Y-%m-%d %H:%m:%S'),
    }

    exif_dict = {'0th': zeroth_ifd, 'Exif': exif_ifd}
    try:
      exif_bytes = piexif.dump(exif_dict)
    except Exception as ex:
      logger.debug(f'No exif data available: {ex}')
      return None

    return exif_bytes

  @property
  def address(self):
    return self._device['address']

  @address.setter
  def address(self, value):
    value = terrariumUtils.clean_address(value)
    if value is not None and '' != value:
      if self.address != value:
        self._device['address'] = value
        self.load_hardware()

  @property
  def awb(self):
    return self._device['awb']

  @awb.setter
  def awb(self, value):
    if value is not None and '' != str(value).strip():
      self._device['awb'] = str(value).strip()

  @property
  def device(self):
    return self._device['device']

  @property
  def id(self):
    if self._device['id'] is None:
      self._device['id'] = md5('{}{}'.format(self.HARDWARE, self.address).encode()).hexdigest()

    return self._device['id']

  @id.setter
  def id(self, value):
    if value is not None and '' != str(value).strip():
      self._device['id'] = str(value).strip()

  @property
  def height(self):
    return self._device['resolution'][1]

  @property
  def name(self):
    return self._device['name']

  @name.setter
  def name(self, value):
    if value is not None and '' != str(value).strip():
      self._device['name'] = str(value).strip()

  @property
  def resolution(self):
    return self._device['resolution']

  @resolution.setter
  def resolution(self, value):
    if len(value) == 2:
      self._device['resolution'] = value

  @property
  def rotation(self):
    return self._device['rotation']

  @rotation.setter
  def rotation(self, value):
    value = value.lower()
    if value is not None and str(value).strip() in self.__VALID_ROTATIONS:
      self._device['rotation'] = str(value).strip()

  @property
  def width(self):
    return self._device['resolution'][0]

  @property
  def state(self):
    return terrariumUtils.is_true(self._device['state'])

  @property
  def value(self):
    return 'online' if self.state else 'offline'

  @property
  def live(self):
    return self.HARDWARE.lower().endswith('-live')

  @property
  def last_update(self):
    return self._device['last_update']

  @property
  def raw_image_path(self):
    return self._STORE_LOCATION.joinpath(self.id,f'{self.id}_raw.jpg')

  @property
  def raw_archive_path(self):
    return self.__ARCHIVE_LOCATION.joinpath(self.id, datetime.now().strftime('%Y/%m/%d'), f'{self.id}_archive_{int(time())}.jpg')

  def update(self, relays = None):
    # Readonly call
    if relays is None:
      return self.value

    # To early update
    if not (self._device['last_update'] is None or (datetime.now() - self._device['last_update']).total_seconds() > self.__UPDATE_TIMEOUT):
      return self.value

    # Toggle on relays (flash)
    if len(relays) > 0:
      start = time()
      for relay in relays:
        relay.on()

      sleep(1)
      logger.debug(f'Webcam {self.name}: Toggle on flash lights took {time()-start:.3f} seconds')

    start = time()
    for x in range(3):
      try:
        image = func_timeout(15, self._get_raw_data)
        if image is not False:
          try:
            start2 = time()
            self.__raw_image = Image.open(image)
            self._device['state'] = True
            logger.debug(f'Webcam {self.name}: Loaded image in memory took: {time()-start2:.3f} seconds')
            break
          except Exception as ex:
            logger.error(f'Could not process webcam image {self}: {ex}')
            image = False

      except FunctionTimedOut:
        logger.error(f'Webcam {self} timed out after 15 seconds during updating...')
        image = False

      if x < 3:
        sleep(1)

    logger.debug(f'Webcam {self.name}: Getting a new image took: {time()-start:.3f} seconds')

    # except Exception as ex:
    #   logger.error(f'Webcam {self} has exception: {ex}')
    #   image = False

    if len(relays) > 0:
      start = time()
      for relay in relays:
        relay.off()

      logger.debug(f'Webcam {self.name}: Toggle off flash lights took {time()-start:.3f} seconds')

    if image is False:
      # Camera is offline!!
#      logger.warning('Webcam {} has errors!'.format(self.name))
      if self.state:
        self._device['state'] = False
        logger.error('Webcam {} has gone offline! Please check your webcam connections.'.format(self.name))
        self.__raw_image = self.__set_offline_image()
        self.__tile_image()
        self.__raw_image.save(self.raw_image_path,'jpeg', quality=self.__JPEG_QUALITY)

      return False

    # After here, no errors should happen, the image data should be save and correct
    if not self.live:
      try:
        start = time()
        self.__rotate()
        logger.debug(f'Webcam {self.name}: Rotating image took: {time()-start:.3f} seconds')
        start = time()
        self.__tile_image()
        logger.debug(f'Webcam {self.name}: Tiling image took: {time()-start:.3f} seconds')
      except Exception as ex:
        logger.error(f'Could not process webcam image {self}: {ex}')
        return False

    start = time()
    self.__raw_image.save(self.raw_image_path,'jpeg', quality=self.__JPEG_QUALITY, exif=self.__exit_data)
    logger.debug(f'Webcam {self.name}: Saving image to disk took: {time()-start:.3f} seconds')
    self._device['last_update'] = datetime.now()

    return self.value

  def archive(self,timeout):
    if not self.state:
      return

    archive = self.__last_archive_image is None or int(time() - self.__last_archive_image.stat().st_mtime) >= timeout
    if archive:
      start = time()
      self.__last_archive_image = self.raw_archive_path
      self.__last_archive_image.parent.mkdir(parents=True,exist_ok=True)
      self.__raw_image.save(self.__last_archive_image,'jpeg', quality=self.__JPEG_QUALITY, exif=self.__exit_data)
      #self.__environment.notification.message('webcam_archive',self.get_data(),[archive_image])
      logger.debug(f'Webcam {self.name}: Archiving image to disk took: {time()-start:.3f} seconds')


  def motion_capture(self, motion_frame = 'last', motion_threshold = 25, motion_area = 500, motion_boxes = 'green'):
    if not self.state:
      return

    start = time()

    # https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
    #try:
    current_image = cv2.imread(str(self.raw_image_path))
    current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    current_image = cv2.GaussianBlur(current_image, (21, 21), 0)

    if self.__compare_image is None or self.__compare_image.shape[0] != current_image.shape[0] or self.__compare_image.shape[1] != current_image.shape[1]:
      # If we have no previous image to compare, just set it to the current and we are done.
      # OR when the dimensions changes. This will give an error when comparing...
      self.__compare_image = current_image
      return

    threshold = cv2.threshold(cv2.absdiff(self.__compare_image, current_image), int(motion_threshold), 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    # Different OpenCV versions (docker vs native)
    try:
      (cnts ,_) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except Exception as ex:
      logger.debug(f'Wrong CV2 version. Retry: {ex}')
      (_,cnts ,_) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # don't draw if motion boxes is disabled
    # Color Red and Blue are swapped... very strange...
    box_color = None
    if 'red' == motion_boxes:
      box_color = (0, 0, 255)
    elif 'green' == motion_boxes:
      box_color = (0, 255, 0)
    elif 'blue' == motion_boxes:
      box_color = (255, 0, 0)

    # Reread the current image, as in the first part, we have changed the image with filters to motion detection
    raw_image = cv2.imread(str(self.raw_image_path))
    # loop over the contours
    motion_detected = False
    for c in cnts:
      # if the contour is too small, ignore it
      if cv2.contourArea(c) < motion_area:
        continue

      motion_detected = True
      # compute the bounding box for the contour, draw it on the frame with the selected color,
      if box_color is not None:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(raw_image, (x, y), (x + w, y + h), box_color, 2)

    if motion_detected:
      self.__last_archive_image = self.raw_archive_path
      self.__last_archive_image.parent.mkdir(parents=True,exist_ok=True)
      cv2.imwrite(str(self.raw_archive_path),raw_image)
      # Store the current image for next comparison round.
      self.__compare_image = current_image
      logger.info(f'Saved webcam {self} image for archive due to motion detection')
      #self.__environment.notification.message('webcam_motion',self.get_data(),[archive_image])

    elif 'last' == motion_frame:
      # Only store the current frame when we use the 'last' frame option
      self.__compare_image = current_image

    logger.debug(f'Webcam {self.name}: Motion detection image took: {time()-start:.3f} seconds')


  # TODO: What to stop....?
  def stop(self):
    pass
