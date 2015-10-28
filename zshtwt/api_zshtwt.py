import requests, json
from zshtwt import User
import csv
from virtualenv import writefile
from html5lib.constants import DataLossWarning
API_URL = 'https://api.twitter.com/1.1/'

def get_followers(screen_name=User.screen_name, count=200):
	URL=API_URL+'followers/list.json'
	followers = []
	try:
		data = json.loads(requests.get(URL, auth=User.auth, params=dict(screen_name=User.screen_name, count=count)).text)
		#Retrieve our first set of followers
		while data: #while there is still a set of data to be processsed
			for x in range(len(data['users'])): #For each user json object
				followers.append(data['users'][x]['screen_name']) #Add the user json object's screen name attribute to the list of followers 
			if data['next_cursor'] != 0:#If there is another page of followers to retrieve
				data = json.loads(requests.get(URL, auth=User.auth, params=dict(screen_name=User.screen_name, count=count, cursor=data['next_cursor'])).text)
				#Reset data to the next page
			else:
				data = None #if there are no more followers, then set data to null in order to break the loop
	except:
		print(data) #if there is an error, which is likely due to a api max call lockout, simpy print the data
	return followers #return the array of followers

def get_following(screen_name=User.screen_name):
	URL=API_URL+'friends/list.json'
	following = []
	try:
		data = json.loads(requests.get(URL, auth=User.auth, params=dict(screen_name=User.screen_name,  cursor=-1, count=5000)).text)#retrieve the first page of followings, up to five thousand per request
		while data:#while there is a set of data
			for x in range(len(data['users'])):#for each user being followed, shown within the json object
				following.append(data['users'][x]['screen_name'])#add each users screen name to the following array
			if data['next_cursor']!=0:#if there is another page of followers
				data = json.loads(requests.get(URL, auth=User.auth, params=dict(screen_name=User.screen_name,  cursor=data['next_cursor'])).text) #reset data var to equal the new set of data
			else:
				data = None#if there is no next page, set the data var to null in order to break the loop`
	except:
		print(data)#print api error
	return following#return the array of those who the user is following

def get_rate_status():
	URL = API_URL+'application/rate_limit_status.json?resources=friends,followers'
	data = json.loads(requests.get(url=URL, auth=User.auth).text)
	return data

def deposit(file, data):
	try:
		 #Choose a file to write the contents to (csv)
			file = csv.writer(open(file,'w'))
			for each in data:#Iterate over the array 
				file.writerow([each])#Write a row for each screen name 
	except:#if the file cannot be opened or wrote to 
		print("Can't write in this directory for some reason.")

def compare(followers_file_name=User.followers_file_name,following_file_name=User.following_file_name):
	
	try:
		followers_file_i, following_file_i = open(followers_file_name, 'r'), open(following_file_name, 'r') #open each file in an instance. did this in order to be able to close the file to save memory. 
		followers_file, following_file = csv.reader(followers_file_i), csv.reader(following_file_i)# open csv reader objects of each of the file instances
		follower_list, following_list = list( follower for follower in followers_file),   list(follow for follow in following_file)#create lists of each of the files
		followers_file_i.close()
		following_file_i.close()
	except:
		print('You have supplied an invalid file name or format. \n*Error creating an array from these files: \n*', following_file_name, followers_file_name) #if the callled file cant be read fromm
		quit()
	#Open each file and  create an array from each
	user_not_following_back, not_following_user_back = [], []
	for follower in follower_list:
		if follower not in following_list:
			user_not_following_back.append(follower)
	for following in following_list: 
		if following not in follower_list:
			not_following_user_back.append(following)
	
	return user_not_following_back, not_following_user_back 
	#RETURNS TWO ARRAYS, THE FIRST BEING WHO THE CLIENT IS NOT FOLLOWING BACK, THE SECOND WHO HESHE DOESNT FOLLOW BACK 
def refresh(followers_file_name=User.followers_file_name, following_file_name=User.following_file_name, screen_name=User.screen_name):
	try:	
		deposit(following_file_name, get_following(screen_name))
		deposit(followers_file_name, get_followers(screen_name))
	except:
		print('Failed to refresh.')
		quit()
		
def unfollow(data, screen_name=User.screen_name):
	URL = API_URL+'friendships/destroy.json'
	for each_to_uf in data:
		requests.post(URL, auth=User.auth, params=dict(screen_name=each_to_uf))
	refresh_cache_file(data, User.following_file_name)

def follow(data, screen_name=User.screen_name):
	URL = API_URL+'friendships/create.json'
	try:
		for each_to_f in data:
			requests.post(URL, auth=User.auth, params=dict(screen_name=each_to_f)) 
			refresh_cache_file(data,User.followers_file_name)
	except:
		refresh_cache_file(data,User.followers_file_name)
	
	
def refresh_cache_file(data, file):
	fixed_parsed_data = []
	for each in data:
		fixed_parsed_data.append(str(each)[2:-2])#parse the data out of the arrays and make an array of just the str data 
	current_data  = []
	readfile =csv.reader(open(file, "r"))
	#writefile = csv.writer(open(file, "w"))
	for each_line in readfile:
		current_data.append(str(each_line)[2:-2])
	for each_data in fixed_parsed_data:
		if each_data in current_data:
			current_data.remove(each_data)
	deposit(file, current_data)

		
	
			
				
	