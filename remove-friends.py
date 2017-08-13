import os
import tweepy
from time import sleep
import random
import json
try:
    from credentials import *
except ModuleNotFoundError:
    consumer_secret = os.environ['consumer_secret']
    consumer_key = os.environ['consumer_key']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
for friend in tweepy.Cursor(api.friends).items(1000):
	#following.append((friend.followers_count,friend.screen_name))
        try:
            friend.unfollow()
            print('unfollowed',friend.screen_name)
            sleep(75)
        except tweepy.TweepError as e:
            print(e)
            sleep(15*60)

#following.sort(reverse = True)
#print (following)
