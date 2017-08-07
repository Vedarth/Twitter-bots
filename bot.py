import os
import tweepy
from time import sleep
import json
import random
try:
    from credentials import *
except ModuleNotFoundError:
    consumer_secret = os.environ['consumer_secret']
    consumer_key = os.environ['consumer_key']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
#except Exception as e:
#    print('Failed',e)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
with open('keywords.txt') as f:
    keywords = f.readlines()
while True:
    print ('What do you want to do?')
    j = 0
    q = random.choice(keywords).strip()    
    if q=='quit':
        break
    
    for tweet in tweepy.Cursor(api.search, q).items(100):
        try:
            tweet.retweet()
            tweet.favorite()
            tweet.user.follow()
            print('followed',tweet.user.screen_name)
        except:
            continue
        sleep(20)

