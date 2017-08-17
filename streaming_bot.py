import os
import tweepy
from time import sleep
import random
import json
import re
import bad
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
fh = open('keywords.txt')
keywords = fh.read().split()
class my_stream_listener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 20

    def on_data(self,raw_data):
        sleep(40)
        offend = False
        js = json.loads(raw_data)
        for word in js['text'].split():
            if word in bad.arrBad:
                offend = True
        if offend is True:
            print('I am offended')
        else:
            try:
                api.retweet(str(js['id']))
                self.counter += 1
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
            if self.counter < self.limit:
                return True
            else:
                my_stream.disconnect()
        sleep(25)

def unfollow():
    for friend in tweepy.Cursor(api.friends).items(1000):
        try:
            friend.unfollow()
            print('unfollowed',friend.screen_name)
            sleep(80)
        except tweepy.TweepError:
            print(e)
            sleep(15*60)

while True:
    q = random.choice(keywords)
    print(q)
    user = api.get_user('vedarthsharma')
    if user.friends_count > 4700:
        unfollow()
    else:
        pass
    my_stream_listen = my_stream_listener()
    my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listen)
    my_stream.filter(languages=["en"], track=[q])
    sleep(60) 
