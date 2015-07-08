#Script to extract tweets on different topics using Tweepy library for Python. 
#Topics are extracted from a .txt file containing topics which is provided as an arguement
#For eg :python extract.py topics.txt where topics.txt contains list of topics(each on a new line)
#To obtain API Keys and secret tokens for authorization, create a twitter developer account on https://apps.twitter.com/
#The extracted tweets are saved to data/raw_data/X.csv file where X is the topic name.
#There is a Rate limit restriction on extraction of tweets which limits the number of tweets to be extracted in 15-minute window using REST API.For more details, read https://dev.twitter.com/rest/public/rate-limiting. 
#I noticed Rate Limit Error occured after around 3k tweets had been extracted and hence I used time.sleep() to wait for 16 mins after every 2.5k tweets were extracted

import tweepy
import time
import csv
import sys
import os
import util

DIR_PATH='data/raw_data'

#Create a twitter developer a/c to get the API keys,tokens
API_KEY='OVj52mJfEkTvcomECqsN3JXuU'
API_SECRET='DYZ0K1v87AAvNzQ9hMBW76RCiXvDmXinaYl9u3x9WnJq58YSRz'
ACCESS_TOKEN='3266999198-sqUpbWwe4RBAJGaK2pqTYvHhoP35Befy3mqAorh'
ACCESS_TOKEN_SECRET='0PiTFa6pa8i4ogUD5G8ADq0lGaTzU6VBJDBeZkonqxP4R'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,proxy="http://u.padalkar:13908117@202.141.80.20:3128/") #if using proxy based server,add an argument proxy="http://username:pswrd@host:port/"

topic="Beyonce"
if not os.path.exists(DIR_PATH):
  	os.makedirs(DIR_PATH)
file_name=topic+'2.csv'
file_path=DIR_PATH+'/'+file_name
for j in range(0,100) :
	tweets=tweepy.Cursor(api.search, q=topic,lang='en').items(500)
	try:
		for tweet in tweets : 
				dataStrip = []		
				dataStrip.append(tweet.text.encode('utf-8'))
				with open(file_path, "a+") as fp :
					print("w")
				     	writeFile = csv.writer(fp)
			      		writeFile.writerow(dataStrip)
				fp.close()
	except tweepy.error.TweepError :	
		print("Waiting for 15 mins : Rate Limit Restriction ") 
		print j
	 	time.sleep(60*15) # Rate Limit Restriction on no. of tweets extracted in one 15-min window


