# PineBanana
Trying to train a NN to tweet like Donald J. Trump (or any other Twitter user that has a certain "style"). 

# Authenticating
Put a file named twitter.auth next to getweet.py wich contains the following in this exact order, each in a new line:
* `consumer_key`
* `consumer_secret`
* `access_token_key`
* `access_token_secret`


# Usage
Start listing tweets: `python getweet.py <Twitter handle>`, where `<Twitter handle>` is the Twitter handle of the person you want the NN to try to imitate.

Start training: `python lstmTextGenerator.py`, simple as that. 

# Known issues
* it just isn't there yet
* code commenting is mostly in german and not very helpful. sorry 'bout that.
