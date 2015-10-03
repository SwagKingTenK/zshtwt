import requests, json

API_URL = 'https://api.twitter.com/1.1/'

def home_timeline(auth, count=20):
	URL = API_URL+'statuses/home_timeline.json'
	request = requests.get(URL, auth=auth)
	data = json.loads(request.text)
	for x in range(len(data)):
		print(data[x]['user']['name']+' : '+data[x]['text'])