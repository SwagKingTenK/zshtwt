#Colby Cox

import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

try:
    with open('config.txt') as file:
        file=file.readlines()
        CONSUMER_KEY=file[0].strip()
        CONSUMER_SECRET=file[1].strip()
except:
    print('Set your consumer key & consumer secret in config.txt. ')
    quit()        

class Auth(object):

   def __init__(self):
       try:
           self.user_config_file = open('user_config.txt').readlines()
           self.token, self.secret = self.user_config_file[0].strip(), self.user_config_file[1].strip()
       except:
           self.token, self.secret = self.getAuth()
       self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=self.token, resource_owner_secret=self.secret)

   def getAuth(self):
       #Request client token
       self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
       #Gather credentials
       self.credentials = parse_qs(requests.post(url=REQUEST_TOKEN_URL, auth=self.oauth).text)
       self.RESOURCE_OWNER_KEY = self.credentials.get('oauth_token')[0]
       self.RESOURCE_OWNER_SECRET = self.credentials.get('oauth_token_secret')[0]
       #Authorize
       A_URL = AUTHORIZE_URL+self.RESOURCE_OWNER_KEY
       print("Please visit: ",A_URL," and record the pin for authorization.")
       self.verifier = str(input('Please enter the recorded pin: ')).strip()
       self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=self.RESOURCE_OWNER_KEY, resource_owner_secret=self.RESOURCE_OWNER_SECRET, verifier=self.verifier)
       self.credentials = parse_qs(requests.post(url=ACCESS_TOKEN_URL, auth=self.oauth).text)
       self.token = self.credentials.get('oauth_token')[0]
       self.secret = self.credentials.get('oauth_token_secret')[0]
       with open('user_config.txt', 'w') as file:
           file.write(self.secret+'\n'+self.token)
       return self.token, self.secret
