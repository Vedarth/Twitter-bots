import os
import tweepy
from time import sleep
import random
import json
import re
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
user = api.get_user('vedarthsharma')
fh = open('keywords.txt')
keywords = fh.read().split()
class my_stream_listener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 20

    def on_data(self,raw_data):
        sleep(20)
        js = json.loads(raw_data)
        try:
            api.retweet(str(js['id']))
            self.counter += 1
            print(str(js['text']))
            sleep(5)
        except tweepy.TweepError as e:
            print(e)
            sleep(5)
        try:
            api.create_favorite(str(js['id']))
            self.counter += 1
            sleep(5)
        except tweepy.TweepError as e:
            print(e)
            sleep(5)
        try:
            api.create_friendship(js['user']['screen_name'])
            print(js['user']['screen_name'])
            self.counter += 1
            sleep(5)
        except tweepy.TweepError as e:
            print(e)
            sleep(5)
        if user.friends_count > 4900:
            unfollow()
        else:
            pass
        if self.counter < self.limit:
            return True
        else:
            my_stream.disconnect()
        sleep(10)

def unfollow():
    for friend in tweepy.Cursor(api.friends).items(200):
	#following.append((friend.followers_count,friend.screen_name))
        try:
            friend.unfollow()
            print('unfollowed',friend.screen_name)
            sleep(50)
        except:
            pass

while True:
    q = random.choice(keywords)
    my_stream_listen = my_stream_listener()
    my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listen)
    my_stream.filter(languages=["en"], track=[q], async=True)
