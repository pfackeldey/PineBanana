import twitter

file=open("twitter.auth", "r")
auth=["","","",""]
i = 0
for line in file:
	print line
	auth[i] = line.rstrip()
	i+=1
#print auth

api = twitter.Api(consumer_key=auth[0],consumer_secret=auth[1],access_token_key=auth[2],access_token_secret=auth[3])

#print(api.VerifyCredentials())

#trump_tweets = twper.user_timeline("realDonaldTrump", count=100)
#for tweet in trump_tweets:
#	print tweet.
#	print tweet.text

trump_tweets = api.GetUserTimeline(screen_name="realDonaldTrump")
for tweet in trump_tweets:
	print tweet
	print ""
