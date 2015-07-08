# For aspect mining from tweets using method described in 'Aspect-Based Twitter Sentiment Classification' by Hui Lek et al. 

import util

def parse_but(pos_tweets) :
	for pos_tweet in pos_tweets :
		for pos_token in pos_tweet :
			if pos_token[0]=="but" :
				pos_tweet=pos_tweet[pos_tweet.index(pos_token)+1:]
	return pos_tweets

def get_aspect(pos_tweets) :
	pos_tweets=parse_but(pos_tweets)
	aspects_list=[]
	for pos_tweet in pos_tweets :
		aspect_tweet=[]
		for pos_token in pos_tweet :
			if pos_token[1]=='^' or pos_token[1]=='@' or pos_token[1]=='Z' or pos_token[1]=='M' or pos_token[1]=='N':
				aspect_tweet.append(str(pos_token[0]))		
		aspects_list.append(aspect_tweet)
	return aspects_list
