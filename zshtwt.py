import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='

CONSUMER_KEY = 'ZKaIyDmc4mR506aPjojktLsUN'
CONSUMER_SECRET = '1t3oyb5oCqGx9ZiumazclQ5hCRjxkDS6BEK1WiSRTSO1S6p4Y9'

OAUTH_TOKEN = ''
OAUTH_SECRET = ''

def setup_oauth():
	#Request client token
	oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
	params = dict(oauth_callback='oob')
	req = requests.post(url=REQUEST_TOKEN_URL, auth=oauth, params=params)
	#Gather credentials
	credentials = parse_qs(req.text)
	RESOURCE_OWNER_KEY = credentials.get('oauth_token')[0]
	RESOURCE_OWNER_SECRET = credentials.get('oauth_token_secret')
	#Authorize
	AUTHORIZE_URL = AUTHORIZE_URL+RESOURCE_OWNER_KEY
	print("Please visit: ",AUTHORIZE_URL," and record the pin for authorization.")
	verifier = str(input('Please enter the recorded pin: ')).strip()
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=RESOURCE_OWNER_KEY,
                   resource_owner_secret=RESOURCE_OWNER_SECRET, verifier=verifier)
    req = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(req.text)
    OAUTH_TOKEN = credentials.get('oauth_token')[0]
    OAUTH_SECRET = credentials.get('oauth_token_secret')[0]
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
        return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        setup_oauth()
    else:
        oauth = get_oauth()
        req = 
	

