# coding=utf-8
import twitter
import unicodedata
import json
from collections import *
from pprint import pprint

filterlist=["",""] #könnte nützlich werden
wordlist = [""]
target = "haqfleisch" #Wessen Tweets lesen?

def getWords(tweet):
	tweet_wordlist = str.split(unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore').lower()) #Falls möglich zusätzliche Befehle anhängen. Definitiv nicht unübersichtlich genug
#	print tweet_wordlist
	for word in tweet_wordlist:
		if word not in filterlist:
			wordlist.append(word)

file=open("twitter.auth", "r")
auth=["","","",""]		# Kein Plan ob das eleganter geht
i = 0				# ich hasse mein Leben
for line in file:		#
	auth[i] = line.rstrip()	# Eleganz neu definiert
	i+=1			#

api = twitter.Api(consumer_key=auth[0],consumer_secret=auth[1],access_token_key=auth[2],access_token_secret=auth[3])	# I HAVE A AUTHENTICATION https://www.youtube.com/watch?v=3vDWWy4CMhE

#print(api.VerifyCredentials()) #Um zu gucken ob Auth grundsätzlich klappt

l = 0
firstrun = 1
lastID = 822501803615014918
while l <= 50000: #50k Tweets sollten reichen
	if firstrun==1:
		print "Running for the first time"
		tweets = api.GetUserTimeline(screen_name=target, since_id=lastID, count=200, exclude_replies=1, include_rts=0,) #first TWT since_id 822501803615014918
		firstrun = firstrun + 1
	else:
		print "Running for ", firstrun, " times."
		tweets.extend(api.GetUserTimeline(screen_name=target, since_id=lastID, count=200, exclude_replies=1, include_rts=0,))
		firstrun = firstrun + 1

	l = len(tweets)
	if lastID == tweets[l-1].id:
		print "Ich habe alles gesehen..."
		break
	lastID = tweets[l-1].id
	print l, " Tweets in Tweets"
	print "Grabbing tweets from lastID: ", lastID

for tweet in tweets:    		
	getWords(tweet)
	pprint(tweet)							# Tweets aufschreiben
	pprint("")							# und säuberlich trennen

counts = Counter(wordlist).most_common(50)				#50 häufigste Worte in allen tweets zusammen
pprint(counts)								#pretty print the top ten
	 

