import sys

reload(sys)  
sys.setdefaultencoding('utf8')


def remove_repetition(tweets):
	tweets=[tweet.lstrip("rt:\t") for tweet in tweets]
	tweets=list(set(tweets))
	return tweets

def if_not_topic(tweets,topic) :
	tweets=[tweet for tweet in tweets if topic in tweet ]
	return tweets	

def if_only_url(pos_tweets) :
	ind=[]
	for i in range(0,len(pos_tweets)) :
		pos_tokens=pos_tweets[i]
		for pos_tok in pos_tokens :
			if pos_tok[1]=="U" or pos_tok[1]=="@" or pos_tok[1]=="~" :
				pos_tokens.remove(pos_tok)
		if len(pos_tokens)==0 :
			ind.append(i)
	return ind				

def make_lowercase(tweets):
	tweets=[tweet.lower() for tweet in tweets]
	return tweets

def remove_newline(tweets) :
	tweets=[tweet.replace("\n"," ") for tweet in tweets]
	return tweets	

def url_removed(pos_tweet):
	tweet=" "
	url=" "
	for tok in pos_tweet :
		if tok[1]=="U" :
			url=url+" "+tok[0]
		else :
			tweet=tweet+" "+tok[0]
	y=[]
	y.append(tweet.lstrip(" "))
	y.append(url)
	return y

def common_except_url(pos_tweets):
	tweets=[ url_removed(pos_tweet) for pos_tweet in pos_tweets]
	final_tweets=[]
	final_urls=[]
	for tweet in tweets :
		if tweet[0] in final_tweets :
			i=final_tweets.index(tweet[0])
			final_urls[i]=final_urls[i]+" "+tweet[1]
		else :
			final_tweets.append(tweet[0])
			final_urls.append(tweet[1])
	for i in range(0,len(final_tweets)) :
		final_tweets[i]=final_tweets[i]+" "+final_urls[i]
	return final_tweets			
