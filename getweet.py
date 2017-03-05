import twitter

file=open("twitter.auth", "r")
auth=["","","",""]		# Kein Plan ob das eleganter geht
i = 0				# ich hasse mein Leben
for line in file:		#
	auth[i] = line.rstrip()	# Eleganz neu definiert
	i+=1			#

api = twitter.Api(consumer_key=auth[0],consumer_secret=auth[1],access_token_key=auth[2],access_token_secret=auth[3])	# I HAVE A AUTHENTICATION https://www.youtube.com/watch?v=3vDWWy4CMhE

#print(api.VerifyCredentials()) #Um zu gucken ob Auth grundsätzlich klappt

trump_tweets = api.GetUserTimeline(screen_name="realDonaldTrump")	# keep calm & api.getUserTimeline
for tweet in trump_tweets:						#
	print tweet							# Tweets aufschreiben
	print ""							# und säuberlich trennen
