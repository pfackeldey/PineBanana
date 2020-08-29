# -*- coding: utf-8 -*-
import re
import os
from pprint import pprint

import tweepy


def flattenList(listOfLists):
    """
    flatten 2D list
    return [1, 2, 3, 4, ...] for input [[1, 2], [3, 4, ...], ...]
    """
    return [item for subList in listOfLists for item in subList]


def matchingItem(regexItems, string):
    """
    find/return item in string list that matches the given regex
    returns None in case no matching item is found
    """
    for item in regexItems:
        if re.search(item, string) != None:
            return item
    return None


def get_folder_size(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_folder_size(itempath)
    return total_size


def doAPI(authfile):
    file = open(authfile, "r")
    auth = ["", "", "", ""]		# Kein Plan ob das eleganter geht
    i = 0				# ich hasse mein Leben
    for line in file:		#
        auth[i] = line.rstrip()  # Eleganz neu definiert
        i += 1			#

    oauth = tweepy.OAuthHandler(auth[0], auth[1])
    oauth.set_access_token(auth[2], auth[3])
    api = tweepy.API(oauth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # test authentication
    if (not api):
        pprint("Can't authenticate")
        
    return api


def deleteIfBadWord(api, tweet, words_inTweet, badWordList):
    print("Suche löschenswürdige Tweets...")
    for word in words_inTweet:
        if word in badWordList:
            print("Ich lösche für dich den folgenden Tweet:")
            pprint(tweet.text)
            api.DestroyStatus(tweet.id)
            os.system('clear')
    os.system('clear')

# Add more tools! Examples
