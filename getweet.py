# coding=utf-8
import sys
import twitter
import unicodedata
import json
from twitterutils import *
from collections import *
from pprint import pprint

wordlist = [""]
filterlist = [] #Um z.B. "ich" oder "-" rauszuholen oder so
badWordList = [] #Experiment zum Löschen von Tweets in denen Keywords stehen
target = sys.argv[1] #Wessen Tweets lesen? Jetzt über das erste Argument der Konsole spezifiziert

def getWords(tweet):
	tweet_wordlist = str.split(unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore').lower()) #Falls möglich zusätzliche Befehle anhängen. Definitiv nicht unübersichtlich genug
#	print tweet_wordlist
	for word in tweet_wordlist:
		if word not in filterlist:
			wordlist.append(word)
	return tweet_wordlist
	
api = doAPI("twitter.auth")


#print(api.VerifyCredentials()) #Um zu gucken ob Auth grundsätzlich klappt

tweets = []

new_tweets = api.GetUserTimeline(screen_name=target, count=200, exclude_replies=1, include_rts=0,)

tweets.extend(new_tweets)

lastID = tweets[-1].id - 1

while len(new_tweets) > 0:
	print "Getting tweets before ", tweets[-1].created_at
	
	new_tweets = api.GetUserTimeline(screen_name=target, max_id=lastID, count=200, exclude_replies=1, include_rts=0,)
	
	tweets.extend(new_tweets)
	
	lastID = tweets[-1].id - 1

for tweet in tweets:    		
	words_inTweet = getWords(tweet)
	pprint(tweet)							# Tweets aufschreiben
	pprint("")							# und säuberlich trennen
	
	if(len(badWordList) > 0):
		deleteIfBadWord(api, tweet, words_inTweet, badWordList)
	else:
		print "Keine badWordList angegeben, also keine Löschungen"
	

counts = Counter(wordlist).most_common(50)				#50 häufigste Worte in allen tweets zusammen
pprint(counts)								#pretty print the top ten
	 

