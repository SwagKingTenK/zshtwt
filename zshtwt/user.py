import requests
import json
from zshtwt import authorize_zshtwt
from tkinter import *
class User(object):
    
    def __init__(self, user_config_file='user_config.txt', followers_file_name='followers.csv', following_file_name='following.csv'):
        self.auth = authorize_zshtwt.Auth(user_config_file).oauth #setup an authorization instance with the user config file
        self.user_config_file = user_config_file 
        self.followers_file_name = followers_file_name
        self.following_file_name = following_file_name
        self.user_data = self.userAuth()
        self.screen_name = self.user_data["screen_name"]
        self.name = self.user_data["name"]
    def userAuth(self):
        self.user_data = json.loads(requests.get('https://api.twitter.com/1.1/account/verify_credentials.json', auth=self.auth).text)#get user data 
        return self.user_data
