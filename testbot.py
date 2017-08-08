import os
import tweepy
from time import sleep
import random
class my_stream_listener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
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

q = input()
my_stream_listen = my_stream_listener()
my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listen)
my_stream.filter(track=[q])
