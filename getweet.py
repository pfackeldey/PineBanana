# coding=utf-8
import twitter
import unicodedata
from collections import *
from pprint import pprint

wordlist = [""]

def getWords(tweet):
	tweet_wordlist = str.split(unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore'))
	print tweet_wordlist
	for word in tweet_wordlist:
		wordlist.append(word)

file=open("twitter.auth", "r")
auth=["","","",""]		# Kein Plan ob das eleganter geht
i = 0				# ich hasse mein Leben
for line in file:		#
	auth[i] = line.rstrip()	# Eleganz neu definiert
	i+=1			#

api = twitter.Api(consumer_key=auth[0],consumer_secret=auth[1],access_token_key=auth[2],access_token_secret=auth[3])	# I HAVE A AUTHENTICATION https://www.youtube.com/watch?v=3vDWWy4CMhE

#print(api.VerifyCredentials()) #Um zu gucken ob Auth grundsätzlich klappt

trump_tweets = api.GetUserTimeline(screen_name="realDonaldTrump", count=200, exclude_replies=1) #first TWT since_id 822501803615014918

for tweet in trump_tweets:
	getWords(tweet)
	pprint(tweet)							# Tweets aufschreiben
	pprint("")							# und säuberlich trennen

counts = Counter(wordlist).most_common(50)				#10 häufigste worte in allen tweets zusammen (top ten)
pprint(counts)								#pretty print the top ten
	 

