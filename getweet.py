# -*- coding: utf-8 -*-
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from tools import *
import argparse

# configure mongoDB
client = MongoClient("localhost:27017")
db=client.PineBanana
serverStatusResult=db.command("serverStatus")

def printServerStatus():
    pprint(serverStatusResult)


badWordList = []  # Experiment zum Löschen von Tweets in denen Keywords stehen
description = "Dieses Program lädt so viele Tweets eines Users herunter wie möglich und speichert sie in Rohform."
# initiate the argument parser
parser = argparse.ArgumentParser(description = description)
parser.add_argument("user", help="Der hinzuzufügende Twitter-Nutzer (ohne vorangestelltes @)", nargs='?', default="etiennetogo")

user = parser.parse_args().user

api = doAPI("twitter.auth")
#pprint(api) #Um zu gucken ob Auth grundsätzlich klappt

# uses the api to load all (available, usually about the last 3000) tweets of a user
# default user is me.
def getAllTweetsByUser(user="haqfleisch"):

    print("Getting tweets by", user)

    tweets = []

    result = api.user_timeline(user, count=200, tweet_mode="extended")

    tweets.extend(result)

    # newest tweet
    first = tweets[0].id

    # oldest tweet
    oldest = tweets[-1].id - 1


    while len(result) > 0:
        pprint("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        result = api.user_timeline(user,count=200, max_id=oldest, tweet_mode="extended")

        # save most recent tweets
        tweets.extend(result)

        # update the id of the oldest tweet less one
        oldest = tweets[-1].id - 1

        pprint("...%s tweets downloaded so far" % (len(tweets)))

    return tweets, oldest, first

# Funktion zum Laden der Tweets von Personen, die noch nicht in der Datenbank sind
def saveInitialBatchForUser(user="haqfleisch"):
    tweets, oldestId, newestId = getAllTweetsByUser(user)

    tweetIds = set()
    no_retweet_list = list()

    for status in tweets:
        pprint(len(tweets))
        
        # remove retweets
        if status._json['retweeted'] or status._json["full_text"].startswith("RT"):
            pprint(status._json["full_text"])
            pprint("Removed retweet %s" % status._json['id'])
        else:
            pprint("Saving Id")
            no_retweet_list.append(status._json)
            tweetIds.add(status.id)
            
    pprint(len(no_retweet_list))
    #pprint(list(tweetIds)) # for debugging

    try:
        tweetSaveResult = db.raw.insert_many(no_retweet_list, ordered=False)

        twitterUser = api.get_user(user)

        userSaveResult = db.users.insert_one(
            {
                "user": user.lower(),
                "user_id": twitterUser.id,
                "newestId": newestId,
                "oldestId": oldestId+1,
                "tweetIds": list(tweetIds),

            })

        print("Saved {} of {} Tweets".format(len(tweetSaveResult.inserted_ids), len(tweetIds)))
        print("Informationen erfolgreich gespeichert: ", userSaveResult.acknowledged)
    except BulkWriteError as bwe:
        print("There were some errors. If they are important and not just pointless duplicate-item warnings, they will be shown below.")

        # filter duplicate item errors
        panic = list(filter(lambda x: x['code'] != 11000, bwe.details['writeErrors']))

        if len(panic) > 0:
          pprint(panic)

    # we want tweet-id and users to be unique
    db.raw.create_index("id", unique=True)
    db.users.create_index("user", unique=True)
    

def saveNextBatchForUser(user="haqfleisch"):
    dbuser = db.users.find_one({"user": user})
    oldest = dbuser["oldestId"]
    first = dbuser["newestId"]
    tweetIds = dbuser["tweetIds"]
    
    print("Getting new tweets by", user)

    tweets = []

    result = api.user_timeline(user, count=200, since_id=first, tweet_mode="extended")

    tweets.extend(result)
    
    # if there are new tweets
    if len(tweets) > 0:
        first = tweets[0].id # update first tweet id
        last_of_new_batch = tweets[-1].id - 1
        
        # continue getting newest tweets
        while len(result) > 0:
            result = api.user_timeline(user, count=200, since_id=first, max_id=last_of_new_batch, tweet_mode="extended")
    
            tweets.extend(result)
            
            # new newest tweet
            first = tweets[0].id
            last_of_new_batch = tweets[-1].id - 1


    while len(result) > 0:
        pprint("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        result = api.user_timeline(user,count=200, max_id=oldest, tweet_mode="extended")

        # save most recent tweets
        tweets.extend(result)

        # update the id of the oldest tweet less one
        oldest = tweets[-1].id - 1

        pprint("...%s tweets downloaded so far" % (len(tweets)))


    tweetIds = set(tweetIds)
    no_retweet_list = list()

    for status in tweets:
        pprint(len(tweets))
        
        # remove retweets
        if status._json['retweeted'] or status._json["full_text"].startswith("RT"):
            pprint(status._json["full_text"])
            pprint("Removed retweet %s" % status._json['id'])
        else:
            pprint("Saving Id")
            no_retweet_list.append(status._json)
            tweetIds.add(status.id)
            
    pprint(len(no_retweet_list))
    #pprint(list(tweetIds)) # for debugging

    try:
        tweetSaveResult = db.raw.insert_many(no_retweet_list, ordered=False)

        twitterUser = api.get_user(user)

        userSaveResult = db.users.replace_one({"user": user},
            {
                "user": user.lower(),
                "user_id": twitterUser.id,
                "newestId": first,
                "oldestId": oldest+1,
                "tweetIds": list(tweetIds)
            })

        print("Saved {} of {} Tweets".format(len(tweetSaveResult.inserted_ids), len(tweetIds)))
        print("Informationen erfolgreich gespeichert: ", userSaveResult.acknowledged)
    except BulkWriteError as bwe:
        print("There were some errors. If they are important and not just pointless duplicate-item warnings, they will be shown below.")

        # filter duplicate item errors
        panic = list(filter(lambda x: x['code'] != 11000, bwe.details['writeErrors']))

        if len(panic) > 0:
          pprint(panic)

    # we want tweet-id and users to be unique
    db.raw.create_index("id", unique=True)
    db.users.create_index("user", unique=True)


if db.users.find_one({"user": user}):
    pprint("User already exists")
    saveNextBatchForUser(user)
else:
    saveInitialBatchForUser(user)

