import requests
import json

class User(object):
	def __init__(self, auth):
		self.auth = auth
		self.user_data = json.loads(requests.get('https://api.twitter.com/1.1/account/verify_credentials.json', auth=self.auth).text)
		self.name = self.user_data['name']
		self.screen_name = self.user_data['screen_name']

