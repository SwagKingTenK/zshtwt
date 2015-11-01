#Colby Cox

import time
import requests
from requests_oauthlib import OAuth1
from cgi import parse_qs 
from tkinter import *

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

   
'''
The program tries to read from the 'config.txt' file. This file entails the 
consumer (app) key, as well as the consumer secret, which MUST be set in
order to utilize this interface. If the file cannot be accessed, or the key
and secret are not on the first and second line respectively, the program issues
the exception and quits.
'''


try:
    with open('config.txt') as file:#get our consumer credentials
        file=file.readlines()

        CONSUMER_KEY=file[0].strip()#get our consumer key
        CONSUMER_SECRET=file[1].strip()#get our consumer secret
except:
    errorWindow = Tk()
    Label(errorWindow, text="Set the consumer key and consumer secret in config.txt!").pack()
    errorWindow.mainloop()      

class Auth(object):

    def __init__(self, user_config_file="user_config.txt"):
        self.user_config_file = user_config_file#init our config file instance
        try:
            self.user_config_file_read = open(self.user_config_file).readlines()#try to read our lines
            self.token, self.secret = self.user_config_file_read[0].strip(), self.user_config_file_read[1].strip()#get the first line, which is our token, followed by our secret
            self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=self.token, resource_owner_secret=self.secret)#authorize those credentials
        except:#if there is no proper credentials or file of such
            self.oauth = self.getAuth()#refetch the auth




    def getAuth(self):
       self.auth_window = Tk()#initialize our authentication window
       
       #Request client token
       self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)#the initial ouath call to validate our token and secret
       
       #Gather credentials
       self.credentials = parse_qs(requests.post(url=REQUEST_TOKEN_URL, auth=self.oauth).text)#our credentials from which we get our client's key and secret
       self.RESOURCE_OWNER_KEY = self.credentials.get('oauth_token')[0]
       self.RESOURCE_OWNER_SECRET = self.credentials.get('oauth_token_secret')[0]
       
       #Authorize
       self.A_URL = AUTHORIZE_URL+self.RESOURCE_OWNER_KEY
       self.authEntryText = StringVar()
       self.authEntryText.set(self.A_URL)#Set the readonly entry to the value of our link
       self.auth_label_text= Label(self.auth_window, text="Visit the link below to retrieve the authorization code.").pack()#simple label to present the user the linl
       self.auth_link_entry = Entry(self.auth_window, state="readonly", textvariable=self.authEntryText).pack()#pack the readonly entry in order to show the link
       self.verifier = StringVar()#initialize the stringvar to read the user code
       self.authEntry = Entry(self.auth_window, textvariable=self.verifier).pack()#pack the entry
       self.alive = True
       def finishAuth():
          self.ver = self.verifier.get().strip()#the users verifier is stripped 
          try:
            self.oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET,resource_owner_key=self.RESOURCE_OWNER_KEY, resource_owner_secret=self.RESOURCE_OWNER_SECRET, verifier=self.ver)#try to confirm the identity and verify for auth
            self.credentials = parse_qs(requests.post(url=ACCESS_TOKEN_URL, auth=self.oauth).text)#retrieve our credentials
            self.token = self.credentials.get('oauth_token')[0]#get the token
            self.secret = self.credentials.get('oauth_token_secret')[0]#get the secret
            self.auth_window.destroy()#kill the window
            self.alive = False#kill the window and continue the program 
          except:#if the given key is bad
            self.failedLabel = Label(self.auth_window, text="Sorry, unable to validate either due to no connection or wrong key.", fg="red", bg="black").pack()#Tell the user that he or she entered the wrong key
       self.authButton = Button(self.auth_window, text="Verify", command=lambda:finishAuth()).pack()#the button to click upon filling in the code

       try:
          while self.alive:#while the screen is still alive and we have not got a successful token!
           self.auth_window.update()#keep the screen alive!
       except:
           pass
       try:
          with open(self.user_config_file, 'w') as file:#try to write the new token and secret
               file.write(self.token+'\n'+self.secret)
       except:
          print("Cannot write to the user configuration file.",self.user_config_file)#likely a permission error
       return OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=self.token, resource_owner_secret=self.secret)#return our new oauth

    

       '''
       Retrieve the resource owner key and secret, and if they are valid, attempt writing 
       to the 'user_config.txt' file. If the pin provided is invalid, or the file in inaccessible, 
       raise the exception and kill the program.
       '''


       
