import requests, json
from zshtwt import User, Auth
import time

API_URL = 'https://api.twitter.com/1.1/'

def home_timeline(count=20):
	URL = API_URL+'statuses/home_timeline.json'
	data = json.loads(requests.get(URL, auth=Auth).text)
	for x in range(len(data)):
		print(data[x]['user']['name']+' : '+data[x]['text'])

def user_timeline(count=20, screen_name=User.screen_name):
	URL = API_URL+'statuses/user_timeline.json'
	data = json.loads(requests.get(URL, auth=Auth, params=dict(count=count, screen_name=screen_name)).text)
	for x in range(len(data)):
		print(data[x]['user']['name']+' : '+data[x]['text'])

def tweet(status='Tweeting from @zshtwt at: '+str(time.time()), in_reply_to=None):
	URL = API_URL+'statuses/update.json'
	requests.post(url=URL, auth=Auth, params=dict(status=status, in_reply_to=in_reply_to))
	return  
def get_followers(screen_name=User.screen_name, count=50):
	URL=API_URL+'followers/list.json'
	data = json.loads(requests.get(URL, auth=Auth, params=dict(screen_name=User.screen_name, count=count)).text)
	x=0
	try:
		while data['next_cursor'] != 0:
			for x in range(len(data['users'])):
				print(data['users'][x]['screen_name'])
				x+=1
			data = json.loads(requests.get(URL, auth=Auth, params=dict(screen_name=User.screen_name, count=count, cursor=data['next_cursor'])).text)
		print(x)
	except:
		pass
def get_following(screen_name=User.screen_name, count=50):
	URL=API_URL+'friends/list.json'
	data = json.loads(requests.get(URL, auth=Auth, params=dict(screen_name=User.screen_name, count=count)).text)
	x=0
	try:
		while data['next_cursor'] != 0:
			for x in range(len(data['users'])):
				print(data['users'][x]['screen_name'])
				x+=1
			data = json.loads(requests.get(URL, auth=Auth, params=dict(screen_name=User.screen_name, count=count, cursor=data['next_cursor'])).text)
		print(x)
	except:
		pass

