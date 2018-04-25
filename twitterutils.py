# -*- coding: utf-8 -*-
import twitter
import unicodedata
import os
from collections import *
from pprint import pprint

def doAPI(authfile):
	file=open(authfile, "r")
	auth=["","","",""]		# Kein Plan ob das eleganter geht
	i = 0				# ich hasse mein Leben
	for line in file:		#
		auth[i] = line.rstrip()	# Eleganz neu definiert
		i+=1			#

	api = twitter.Api(consumer_key=auth[0],consumer_secret=auth[1],access_token_key=auth[2],access_token_secret=auth[3])	# I HAVE A AUTHENTICATION https://www.youtube.com/watch?v=3vDWWy4CMhE
	return api

def deleteIfBadWord(api, tweet, words_inTweet, badWordList):
	print ("Suche löschenswürdige Tweets...")
	for word in words_inTweet:
		if word in badWordList:
			print ("Ich lösche für dich den folgenden Tweet:")
			pprint(tweet.text)
			api.DestroyStatus(tweet.id)
			os.system('clear')
	os.system('clear')
