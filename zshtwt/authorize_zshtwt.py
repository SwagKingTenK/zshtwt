#Colby Cox

import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs 

'''
The requests module is the basic HTTP requests module. 
OAuth1 is used for, well, OAuth.
parse_qs from cgi is used for parsing the token and secret from the 
user.
'''

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

'''These are the constants of the URLs required for this authentication.'''


try:
    with open('config.txt') as file:
        file=file.readlines()
        CONSUMER_KEY=file[0].strip()
        CONSUMER_SECRET=file[1].strip()
except:
    print('Set your consumer key & consumer secret in config.txt. ')
    quit()        
'''
The program tries to read from the 'config.txt' file. This file entails the 
consumer (app) key, as well as the consumer secret, which MUST be set in
order to utilize this interface. If the file cannot be accessed, or the key
and secret are not on the first and second line respectively, the program issues
the exception and quits.
'''

class Auth(object):


   def __init__(self):
       try:
           self.user_config_file = open('user_config.txt').readlines()
           self.token, self.secret = self.user_config_file[0].strip(), self.user_config_file[1].strip()
       except:
           self.token, self.secret = self.getAuth()
      '''
      The program initially tries to read the resource owner key and secret from the 
      'user_config.txt' file. If it is not present, it runs the getAuth method in 
      order to establish these credentials.
      '''

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
       try:
          self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=self.RESOURCE_OWNER_KEY, resource_owner_secret=self.RESOURCE_OWNER_SECRET, verifier=self.verifier)
          self.credentials = parse_qs(requests.post(url=ACCESS_TOKEN_URL, auth=self.oauth).text)
          self.token = self.credentials.get('oauth_token')[0]
          self.secret = self.credentials.get('oauth_token_secret')[0]
          try:
            with open('user_config.txt', 'w') as file:
               file.write(self.token+'\n'+self.secret)
          except:
            print('\nUnable to open the \'user_config.txt\' file, for some reason. \n')
            quit()
       except:
          print('Authentication is required to use this application,\nand you have failed to provide proper authentication.')
          quit()
       '''
       Retrieve the resource owner key and secret, and if they are valid, attempt writing 
       to the 'user_config.txt' file. If the pin provided is invalid, or the file in inaccessible, 
       raise the exception and kill the program.
       '''


       return self.token, self.secret
