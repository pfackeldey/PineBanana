# -*- coding: utf-8 -*-
import sys
import twitter
import unicodedata
import json

from idna import unicode

from tools import *
from collections import *
from pprint import pprint

latestID = 0
lastID = 0
tweets = []
new_tweets = []
wordlist = [""]
filterlist = [" &amp;", '&amp;']  # Um z.B. "ich" oder "-" rauszuholen oder so
badWordList = []  # Experiment zum Löschen von Tweets in denen Keywords stehen
# Wessen Tweets lesen? Jetzt über das erste Argument der Konsole spezifiziert
target = sys.argv[1]

api = doAPI("twitter.auth")
# print(api.VerifyCredentials()) #Um zu gucken ob Auth grundsätzlich klappt


def getWords(tweet):
    tweet_wordlist = str.split(tweet.text.lower())
#	print tweet_wordlist
    for word in tweet_wordlist:
        if word not in filterlist:
            wordlist.append(word)
    return tweet_wordlist


def FileSave(filename, content):
    with open(filename, "a") as myfile:
        myfile.writelines(content)


def setBorders(filename):
    print("Setting borders...")
    global latestID  # ich bin genervt. Geht das nicht irgendwie sinnvoller?
    global lastID  # ich bin genervt. Geht das nicht irgendwie sinnvoller?
    try:
        with open(filename) as myfile:
            latestID = int(myfile.readline())
            # pprint(latestID)
        updateUpperBorder(latestID)
    except IOError:
        print("Borders.txt not found... Making up borders and Mexico will pay for it...")
        newestTweet = api.GetUserTimeline(
            screen_name=target, count=1, exclude_replies=1, include_rts=0)
        # pprint(newestTweet[0].text)
        # pprint(newestTweet[0].id)
        tweets.extend(newestTweet)
        lastID = newestTweet[0].id - 1
        latestID = newestTweet[0].id
        createTweetBase()


def saveBorders(filename, currlatestID):
    print("Saving borders...")
    with open(filename, "w") as myfile:
        myfile.writelines(currlatestID)


def updateUpperBorder(currlatestID):
    print("Updating upper border...")
    newestTweetCandidate = api.GetUserTimeline(
        screen_name=target, count=1, exclude_replies=1, include_rts=0)
    if newestTweetCandidate[0].id != currlatestID:
        print("Newest Tweet has ID:\t" + str(newestTweetCandidate[0].id))
        pprint(newestTweetCandidate[0].text)
        print("Older Tweet had ID:\t" + str(currlatestID))

        newlatestID = newestTweetCandidate[0].id
        updateTweetBase(newlatestID)


def createTweetBase():
    print("Creating Tweet Database...")
    global lastID
    new_tweets = api.GetUserTimeline(
        screen_name=target, max_id=lastID, count=200, exclude_replies=1, include_rts=0,)
    tweets.extend(new_tweets)

    while len(new_tweets) > 0:
        lastID = tweets[-1].id - 1

        print("Getting tweets before ", tweets[-1].created_at)
        new_tweets = api.GetUserTimeline(
            screen_name=target, max_id=lastID, count=200, exclude_replies=1, include_rts=0)
        tweets.extend(new_tweets)


def updateTweetBase(newlatestID):
    print("Updating Tweet Database...")
    global lastID
    global latestID
    lastID = newlatestID
    new_tweets = api.GetUserTimeline(
        screen_name=target, max_id=lastID, count=200, exclude_replies=1, include_rts=0)
    for tweet in new_tweets:
        if tweet.id != latestID:
            pprint(tweet.id)
            pprint(latestID)
            print("")
            tweets.append(tweet)
        else:
            return 0

    while len(new_tweets) > 0:
        lastID = tweets[-1].id - 1
        print("Getting tweets before ", tweets[-1].created_at)
        new_tweets = api.GetUserTimeline(
            screen_name=target, max_id=lastID, count=200, exclude_replies=1, include_rts=0)
        for tweet in new_tweets:
            if tweet.id != latestID:
                tweets.append(tweet)
            else:
                return 0

    latestID = newlatestID


setBorders("Borders.txt")
# print upperBorder

for tweet in tweets:
    words_inTweet = getWords(tweet)
    # pprint(tweet)							# Tweets aufschreiben
    # pprint("")							# und säuberlich trennen

    if(len(badWordList) > 0):
        deleteIfBadWord(api, tweet, words_inTweet, badWordList)
    # else:
    #	print "Keine badWordList angegeben, also keine Löschungen\n"

    # clean Tweet.text
    clean = tweet.text + "\n\n"
    while len(clean) <= 300:  # fill to 300 chars
        clean += "_"  # do it in the worst possible way ever

    FileSave("tweets.txt", clean)


# 50 häufigste Worte in allen tweets zusammen
counts = Counter(wordlist).most_common(50)
pprint(counts)  # pretty print the top ten
pprint(len(tweets))
saveBorders("Borders.txt", str(latestID))
