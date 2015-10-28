import requests
import json
from zshtwt import authorize_zshtwt

class User(object):
	
	def __init__(self, user_config_file='user_config_file.txt', followers_file_name='followers.csv', following_file_name='following.csv'):
		self.user_config_file = user_config_file
		self.followers_file_name = followers_file_name
		self.following_file_name = following_file_name
	def authUser(self):
		self.auth = authorize_zshtwt.Auth(self.user_config_file).oauth
		self.user_data = json.loads(requests.get('https://api.twitter.com/1.1/account/verify_credentials.json', auth=self.auth).text)
        try:
            if self.user_data:		
    		    self.name = self.user_data['name']
	    	    self.screen_name = self.user_data['screen_name']
		except:
			print("Please try re-running the program. If it fails again, you have maxed out your usage for five minutes.")
			quit()
	
	

		
		
