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
        self.limit = 60

    def on_data(self,raw_data):
        sleep(10)
        offend = False
        js = json.loads(raw_data)
        if str(js['user']['screen_name']) == 'vedarthsharma' or js['retweeted']=='True':
            offend=True
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
        self.counter += 1
        sleep(55)

def unfollow():
    for friend in tweepy.Cursor(api.friends).items(1100):
        print (friend.screen_name,friend.following)
        if friend.following:
            print(friend.screen_name,'follows you!')
            sleep(31)
            continue
        else:
            pass
        try:
            friend.unfollow()
            print('unfollowed',friend.screen_name)
            sleep(80)
        except tweepy.TweepError:
            print(e)
            sleep(15*60)

action_decider = 1
while True:
    if action_decider == 0:
        q = random.choice(keywords)
        print(q)
        action_decider=1
    else:
        trends_list = api.trends_place(23424848)
        trends_dict = trends_list[0]
        trend_words = trends_dict['trends']
        trendwords = [trend_word['name'] for trend_word in trend_words]
        q = random.choice(trendwords)
        print(trendwords)
        action_decider=0
    user = api.get_user('vedarthsharma')
    if user.friends_count > 4900:
        unfollow()
    else:
        pass
    my_stream_listen = my_stream_listener()
    my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listen)
    my_stream.filter(languages=["en"], track=[q])
    sleep(60) 
