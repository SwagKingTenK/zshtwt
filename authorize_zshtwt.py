import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = 'ZKaIyDmc4mR506aPjojktLsUN'
CONSUMER_SECRET = '1t3oyb5oCqGx9ZiumazclQ5hCRjxkDS6BEK1WiSRTSO1S6p4Y9'

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""



def setup_oauth():
    #Request client token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    req = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    #Gather credentials
    credentials = parse_qs(req.text)
    RESOURCE_OWNER_KEY = credentials.get('oauth_token')[0]
    RESOURCE_OWNER_SECRET = credentials.get('oauth_token_secret')[0]
    #Authorize
    A_URL = AUTHORIZE_URL+RESOURCE_OWNER_KEY
    print("Please visit: ",A_URL," and record the pin for authorization.")
    verifier = str(input('Please enter the recorded pin: ')).strip()
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=RESOURCE_OWNER_KEY, resource_owner_secret=RESOURCE_OWNER_SECRET, verifier=verifier)
    req = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(req.text)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]
    return token, secret

def get_oauth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET):
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        get_oauth(token, secret)
