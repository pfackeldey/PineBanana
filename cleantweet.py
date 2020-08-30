# local imports
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import BulkWriteError
import pandas as pd

# DB Import
# configure mongoDB TODO: MongoConfig auslagern
client = MongoClient("localhost:27017")
db=client.PineBanana
serverStatusResult=db.command("serverStatus")
raw = db.raw.find().sort("id", -1)

def getText(tweet):
    text = ""

    # please improve me
    try:
        text = tweet['full_text']
    except KeyError:
        text = tweet['text']

    return text

# returns the given list of tweets in a more clear format


def getCleanTweets(tweets):
    cleaned = []
    ids = []
    counter = 1
    for element in tweets:
        print("\rParsing element {} of {}".format(counter, tweets.count()), end="",
              flush=True)  # cursor.count() is deprecated but still the most useful

        isProcessed = False

        try:
            isProcessed = element["processed"]
        except KeyError:
            isProcessed = False
        finally:
            if not isProcessed:
                tweet = {
                    'id': str(element['id']),
                    'by': element['user']['screen_name'],
                    'text': getText(element),
                    'favorite_count': element['favorited'],
                    'retweet_count': element['retweeted'],
                    'lang': element['lang'],
                }
                cleaned.append(tweet)
                # collect all raw object ids that will be deleted
                ids.append(element['id'])
                counter += 1
        print("\nCleaned {} tweets".format(len(ids)))
    return cleaned, ids


clean, ids_to_delete = getCleanTweets(raw)

# add new tweets only if they exist
if len(clean) > 0:
    print("Creating a dataframe...")
    df = pd.DataFrame(clean)
else:
    print("Huch?!?\n No entries to create dataframe from.")


try:
    print("Attempting to save...")
    df_dict = df.T.to_dict().values()
    db.clean.insert_many(df_dict)
    db.clean.create_index("id", unique=True)
    # delete all raw data that has been processed
    result = db.raw.delete_many({"id": {"$in": ids_to_delete}})
except BulkWriteError as bwe:
    print("There were some errors. If they are important and not just pointless duplicate-item warnings, they will be shown below.")

    # filter duplicate item errors
    panic = list(filter(lambda x: x['code'] !=
                        11000, bwe.details['writeErrors']))

    if len(panic) > 0:
        pprint(panic)

print("Saved {} entries".format(result.deleted_count))
