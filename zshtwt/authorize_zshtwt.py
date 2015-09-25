
import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs

class auth_zshtwt(object):  

    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
    ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
    ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

    with open('config.txt') as file:
        file=file.read()
        CONSUMER_KEY = file[0]
        CONSUMER_SECRET = file[1]  
    
    
    def __init__(self):
        #Request client token
        REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
        ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

        CONSUMER_KEY = 'ZKaIyDmc4mR506aPjojktLsUN'
        CONSUMER_SECRET = '1t3oyb5oCqGx9ZiumazclQ5hCRjxkDS6BEK1WiSRTSO1S6p4Y9'
        
        self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
        req = requests.post(url=REQUEST_TOKEN_URL, auth=self.oauth)
        #Gather credentials
        self.credentials = parse_qs(req.text)
        self.RESOURCE_OWNER_KEY = self.credentials.get('oauth_token')[0]
        self.RESOURCE_OWNER_SECRET = self.credentials.get('oauth_token_secret')[0]
        #Authorize
        A_URL = AUTHORIZE_URL+self.RESOURCE_OWNER_KEY
        print("Please visit: ",A_URL," and record the pin for authorization.")
        self.verifier = str(input('Please enter the recorded pin: ')).strip()
        self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=self.RESOURCE_OWNER_KEY, resource_owner_secret=self.RESOURCE_OWNER_SECRET, verifier=self.verifier)
        req = requests.post(url=ACCESS_TOKEN_URL, auth=self.oauth)
        self.credentials = parse_qs(req.text)
        self.token = self.credentials.get('oauth_token')[0]
        self.secret = self.credentials.get('oauth_token_secret')[0]
        
    def get_oauth(self, OAUTH_TOKEN,OAUTH_TOKEN_SECRET):
        self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
        return self.oauth

