# -*- coding: utf-8 -*-
from time import sleep, time
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

class terrariumWebcam():

  def __init__(self, id = None, location = '', name = '', rotation = None):
    if id is None:
      self.id = md5(b'' + str(int(time()))).hexdigest()
    else:
      self.id = id

    # Main config
    self.tile_size = 256 # Smaller tile sizes does not work with LeafJS
    self.tile_location = 'static/webcam/'
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
    stream = BytesIO()
    if 'rpicam' == self.location:
      with PiCamera(resolution=(1920, 1080)) as camera:
        camera.start_preview()
        sleep(2)
        camera.capture(stream, format='png')

    elif self.location.startswith('/dev/video'):
      camera = cv2.VideoCapture(int(self.location[10:]))
      camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
      camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
      sleep(2)
      readok, image = camera.read()

      if readok:
        png = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        stream = StringIO.StringIO()
        png.save(stream,'JPEG')

      camera.release()

    elif self.location.startswith('http://') or self.location.startswith('https://'):
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

    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    # Store image in memory for further processing
    self.raw_image = Image.open(stream)
    self.raw_image.save(self.get_raw_image(),'jpeg',quality=95)
    self.state = True
    self.last_update = int(time())

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

    # as long as there is a new layer, continue
    while zoom_factor >= 0:
      # Create black canvas on zoom factor dimensions
      canvas = Image.new("RGB", ((int(round(canvas_width)),int(round(canvas_height)))), "black")
      # Scale the raw image to the zoomfactor dimensions
      source = self.raw_image.resize((int(round(source_width)),int(round(source_height))))
      # Set the timestamp on resized image
      self.__set_timestamp(source)

      # Calculate the center in the canvas for pasting raw image
      paste_center_position = (int(round((canvas_width - source_width) / 2)),int(round((canvas_height - source_height) / 2)))
      canvas.paste(source,paste_center_position)

      # Loop over the canvas to create the tiles
      for row in xrange(0,int(math.ceil(canvas_height/self.tile_size))):
        for column in xrange(0,int(math.ceil(canvas_width/self.tile_size))):
          crop_size = ( int(row*self.tile_size), int(column*self.tile_size) ,int((row+1)*self.tile_size), int((column+1)*self.tile_size))
          tile = canvas.crop(crop_size)
          tile.save(self.tile_location + self.id + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg','jpeg',quality=95)

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
    self.__get_raw_image()
    self.__tile_image()

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
