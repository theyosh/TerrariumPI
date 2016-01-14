# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import sleep

import urllib2
import base64
import urlparse
import math

#import picamera

from hashlib import md5
from PIL import Image, ImageDraw, ImageFont
from shutil import copy, move
import os
import StringIO

import logging
terrarium_log = logging.getLogger('root')

class terrariumWebcam:
  def __init__(self,name,location,archive,rotation,configObj):
    self.__id = md5(b'' + location).hexdigest()
    self.__name = name
    self.__sourcelocation = location
    self.__config = configObj
    self.__type = 'RPI'
    if not 'RPI' in self.__sourcelocation:
      self.__type = 'HTTP'

    self.__resolution_width = 0
    self.__resolution_height = 0
    self.__size = 0
    self.__image = ''
    self.__rotation = str(rotation)
    self.__font_size = 16
    self.__tile_size = 256
    self.__tile_path = 'webroot/webcam/' + self.__id
    self.__max_zoom = 0

    self.__online = True
    self.__lastOnline = datetime.fromtimestamp(0)
    self.__lastOffline = datetime.fromtimestamp(0)

    self.__cacheTimeOut = timedelta(seconds=20)
    self.__lastUpdate = datetime.fromtimestamp(0)

    self.__archiveTimeout = timedelta(seconds=int(archive) * 60)
    self.__archiveLast = datetime.fromtimestamp(0)
    self.__archive = self.__archiveTimeout > timedelta(seconds=0)

    self.update()

  def __is_number(s):
    try:
      float(s)
      return True
    except ValueError:
      return False

  def getID(self):
    return self.__id

  def setName(self,name):
    self.__name = name

  def getName(self):
    return self.__name

  def setUrl(self,url):
    self.__sourcelocation = url

  def getUrl(self):
    return self.__sourcelocation

  def getRotation(self):
    return self.__rotation

  def setRotation(self,rotation):
    self.__rotation = rotation

  def getArchive(self):
    return self.__archive

  def getArchiveTimeout(self):
    return int(self.__archiveTimeout.total_seconds());

  def getCacheTimeout(self):
    return self.__cacheTimeOut

  def setCacheTimeout(self,timeout):
    self.__cacheTimeOut = timedelta(seconds=int(timeout))

  def getLastUpdateTimeStamp(self):
    return self.__lastUpdate

  def getWidth(self):
    return self.__resolution_width

  def getHeight(self):
    return self.__resolution_height

  def getResolution(self):
    return str(self.getWidth()) + 'x' + str(self.getHeight())

  def getMaxZoom(self):
    return self.__max_zoom

  def update(self):
    now = datetime.now()
    if now - self.__lastUpdate >= self.__cacheTimeOut:
      try:
        if self.__type == 'RPI':
          webcamimg = StringIO.StringIO()
#          with picamera.PiCamera() as camera:
#            camera.resolution = (2592, 1944)
#            camera.awb_mode = 'auto'
#            camera.brightness = 50
#            camera.shutter_speed = 1000000
#            camera.framerate = Fraction(1, 3)
#            camera.exposure_mode = 'auto'
#            camera.iso = 800
#            sleep(3)
#            camera.capture(webcamimg, format='jpeg',quality=95)

        else:
          if '@' in self.__sourcelocation:
            start = self.__sourcelocation.find('://') + 3
            end = self.__sourcelocation.find('@', start)
            auth = self.__sourcelocation[start:end]
            webcamurl = urllib2.Request(self.__sourcelocation.replace(auth+'@',''))
            auth = auth.split(':')
            base64string = base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
            webcamurl.add_header("Authorization", "Basic %s" % base64string)
          else:
            webcamurl = urllib2.Request(self.__sourcelocation)

          webcamimg = StringIO.StringIO(urllib2.urlopen(webcamurl,None,15).read())

        terrarium_log.debug('Updated webcam %s with source %s', self.getName(),self.getUrl())
        webcamimg.seek(0)
        tmp = Image.open(webcamimg)
        if '90' == self.__rotation:
          self.__image = tmp.transpose(Image.ROTATE_90)
        elif  '180' == self.__rotation:
          self.__image = tmp.transpose(Image.ROTATE_180)
        elif '270' == self.__rotation:
          self.__image = tmp.transpose(Image.ROTATE_270)
        elif 'h' == self.__rotation:
          self.__image = tmp.transpose(Image.FLIP_TOP_BOTTOM)
        elif 'v' == self.__rotation:
          self.__image = tmp.transpose(Image.FLIP_LEFT_RIGHT)
        else :
          self.__image = tmp

        terrarium_log.debug('Rotated webcam %s to %s degress', self.getName(), self.getRotation())

        self.__resolution_width, self.__resolution_height = self.__image.size
        self.__lastUpdate = now
        if not self.__online:
          terrarium_log.info('Webcam %s at source %s came online after %d seconds!', self.getName(), self.getUrl(),(now - self.__lastOnline).total_seconds())
          self.__online = True
          self.__lastOnline = now

        self.__setTimeStamp()
#        self.archiveImage()
        self.__tileImage()
        del webcamimg
        del tmp

      except Exception, e:
        print 'Exception:'
        print e

        if self.__online:
          # Switch from online to offline. So this image is created only once when offline
          self.__online = False
          self.__lastOffline = now

          self.__image = Image.open('webroot/images/webcam/offline.png')
          self.__resolution_width, self.__resolution_height = self.__image.size

          mask = Image.open('webroot/images/webcam/mask.png')
          mask_width, mask_height = mask.size
          fontsize = 40
          draw = ImageDraw.Draw(mask)
          font = ImageFont.truetype('fonts/Verdana.ttf',fontsize)

          temp = draw.textsize('Offline since:', font)
          text_width, text_height = temp
          draw.text(((mask_width/2)-(text_width/2), 20),'Offline since:',(255,255,255),font=font)

          temp = draw.textsize(self.__lastOffline.strftime("%A %d %B %Y"), font)
          text_width, text_height = temp
          draw.text(((mask_width/2)-(text_width/2), 85),self.__lastOffline.strftime("%A %d %B %Y") ,(255,255,255),font=font)

          temp = draw.textsize(self.__lastOffline.strftime("%H:%M:%S"), font)
          text_width, text_height = temp
          draw.text(((mask_width/2)-(text_width/2), 135),self.__lastOffline.strftime("%H:%M:%S") ,(255,255,255),font=font)

          self.__image.paste(mask, ((self.__resolution_width/2)-(mask_width/2),(self.__resolution_height/2)-(mask_height/2)), mask)
          self.__resolution_width, self.__resolution_height = self.__image.size

          terrarium_log.warn('Webcam %s at source %s went offline with error: %s', self.getName(),self.getUrl(),e)
          self.__tileImage()

  def archiveImage(self):
    now = datetime.now()
    if self.__archive == True and now - self.__archiveLast > self.__archiveTimeout and os.path.isfile(self.__destination):
      if not os.path.isdir('webroot/archive/' + self.getID()):
        os.makedirs('webroot/archive/' + self.getID())
      copy(self.__destination,'webroot/archive/' + self.getID() + '/' + str((datetime.now()).strftime('%s')) + '.jpg')
      #log.logLine(terrariumLog.INFO,'Archiving webcam ' + self.__name + ' on location webroot/archive/' + + self.getID() + '/' + str(now) + '.jpg')
      self.__archiveLast = now

  def __tileImage(self):
    source = self.__image
    source_width, source_height = source.size

    # Calc new canvas size
    longest_side = source_width if source_width > source_height else source_height
    max_size = int(math.pow(2,math.ceil(math.log(longest_side,2))))
    canvas_width = canvase_height = max_size
    resize_factor = float(max_size) / float(longest_side)

    # Create new source image (scale up to canvas)
    canvas = Image.new("RGB", (canvas_width,canvase_height), "black")
    source = source.resize((int(round(resize_factor*source_width)),int(round(resize_factor*source_height))))
    source_width, source_height = source.size
    paste_position = (int(round((canvas_width - source_width) / 2)),int(round((canvase_height - source_height) / 2)))
    canvas.paste(source,paste_position)
    self.__max_zoom = zoom_factor = int(math.log(max_size/self.__tile_size,2))

    while zoom_factor >= 0:
      for row in xrange(0,int(math.ceil(canvase_height/self.__tile_size))):
        for column in xrange(0,int(math.ceil(canvas_width/self.__tile_size))):
          crop_size = ( int(row*self.__tile_size), int(column*self.__tile_size) ,int((row+1)*self.__tile_size), int((column+1)*self.__tile_size))
          tile = canvas.crop(crop_size)
          tile.save(self.__tile_path + '_tile_' + str(zoom_factor) + '_' + str(row) + '_' + str(column) + '.jpg','jpeg',quality=95)

      canvas = canvas.resize((int(round(canvas_width/2)),int(round(canvase_height/2))))
      canvas_width, canvase_height = canvas.size
      zoom_factor -= 1

    # Clear memory, not sure if needed
    del source
    del canvas

  def __setTimeStamp(self):
    font = ImageFont.truetype('fonts/Verdana_Bold.ttf',self.__font_size)
    draw = ImageDraw.Draw(self.__image)
    draw.rectangle([0,0,self.__resolution_width,self.__font_size+2],fill='black')
    draw.text((1, -2), self.__name + ' last update: ' + (datetime.now()).strftime("%A %d %B %Y %H:%M:%S") ,(255,255,255),font=font)
    del draw

  def saveConfig(self):
    self.__config.saveWebCamSettings(self.getID(),self.getName(),self.getUrl(),self.getArchiveTimeout(),self.getRotation())
