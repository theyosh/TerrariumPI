#import terrarium.birdy.twitter
from birdy.twitter import UserClient

from datetime import datetime, timedelta
import base64
import os

class terrariumTwitter:

  TWITTER_IMAGES = os.path.join(os.path.dirname(os.path.realpath(__file__)) ,'twitter_images')

  def __init__(self,enabled,confObj):
    self.__enabled = enabled in ['1','True','true','on', True]
    
    self.__conf = confObj
    self.__log = None
    self.__twitter = False

    self.__twitterProfile = ''
    self.__lastUpdate = datetime.fromtimestamp(0)

    self.__load_images()

    if self.__enabled:
      self.enable()

  def __load_images(self):
    media_ids = {}
    with open(terrariumTwitter.TWITTER_IMAGES + '/.media_ids', 'rb') as file:
      data = (file.readline()).split(':')
      if len(data) == 2:
        media_ids[data[0]] = data[1]

    self.__tiwtter_images = {'sunrise' : [], 'moonrise' : [], 'humidity' :[], 'heater':[] , 'lights_off' : [], 'lights_on' : []}
    #print 'list files in ' + terrariumTwitter.TWITTER_IMAGES
    for file in os.listdir(terrariumTwitter.TWITTER_IMAGES):
      fullpath = os.path.join(terrariumTwitter.TWITTER_IMAGES,file)
      media_id = (media_ids[file] if file in media_ids else -1)

      twitter_image = {'fullpath' : fullpath, 'media_id' : media_id}
      twitter_image_type = None

      if file.startswith('sunrise'):
        twitter_image_type = 'sunrise'
      elif file.startswith('moonrise'):
        twitter_image_type = 'moonrise'
      elif file.startswith('humidity'):
        twitter_image_type = 'humidity'
      elif file.startswith('heater'):
        twitter_image_type = 'heater'
      elif file.startswith('lights_off'):
        twitter_image_type = 'lights_off'
      elif file.startswith('lights_on'):
        twitter_image_type = 'lights_on'

      if twitter_image_type is not None:
        self.__tiwtter_images[twitter_image_type].append(twitter_image)

    #print self.__tiwtter_images

  def __upload_new_media(self):
    pass

  def enable(self):
    self.__enabled = True
    conf = self.__conf.getTwitterConfig()
    if False == self.__twitter and conf['api_key'] and conf['api_secret'] and conf['token'] and conf['token_secret']:
      self.__twitter = UserClient(conf['api_key'],
                    conf['api_secret'],
                    conf['token'],
                    conf['token_secret'])

      self.__twitterProfile = self.__twitter.api.account.settings.get().data

  def disable(self):
    self.__enabled = False

  def getTwitterProfileUrl(self):
    if self.__enabled:
      return 'https://twitter.com/' + str(self.__twitterProfile['screen_name'])
    else:
      return False

  def online(self):
    return {'online':self.__enabled == True,'link': self.getTwitterProfileUrl()}

  def post(self,tweet):
    if self.__enabled:
      self.__lastUpdate = datetime.now()
      

      if 'media' in tweet:
        response = self.__twitter.api.statuses.update_with_media.post(status=str(tweet['message']),media=open(str(tweet['media']),'rb'))
      else:
        response = self.__twitter.api.statuses.update.post(status=str(tweet['message']))
