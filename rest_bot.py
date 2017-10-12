import os
import tweepy
from time import sleep
import random
import json
import re
import bad
from urllib.parse import urlparse
from datetime import datetime
try:
    from credentials import *
except ModuleNotFoundError:
    consumer_secret = os.environ['consumer_secret']
    consumer_key = os.environ['consumer_key']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
fh = open('keywords.txt')
keywords = fh.read().split()

class my_stream_listener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 39

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
        curr_time()

def unfollow(followers_list, friends_list):
    assholes, i = [friend for friend in friends_list if friend not in followers_list], 0
    to_follow = int(len(followers_list)-(len(friends_list)-len(assholes)))
    to_follow_list = [follower for follower in followers_list if follower not in friends_list]
    k=0
    for tweet in tweepy.Cursor(api.search, 'python').items(1000):
        try:
            api.destroy_friendship(assholes[i-1000])
            print('unfollowed',assholes[i])
            sleep(30)
            i += 1
        except tweepy.TweepError as e:
            print(e)
            sleep(15*60)
        for word in tweet.text.split():
            if word in bad.arrBad:
                sleep(5)
                print('I am rest offended')
                continue
        try:
            tweet.retweet()
            sleep(20)
        except Exception as e:
            print('Could not retweet because',e)
            pass
        try:
            tweet.favorite()
        except:
            print('could not favorite')
        try:
            api.create_friendship(tofollow[k++])
            sleep(10)
        except:
            pass
        curr_time()
            

def curr_time():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #Heroku is about 6:30 hrs behind IST.


action_decider = 0
while True:
    if action_decider == 0:
        q = random.choice(keywords)
        print(q)
        action_decider=1
    else:
        #23424848
        trends_list = api.trends_place(23424848)
        trends_dict = trends_list[0]
        trend_words = trends_dict['trends']
        trendwords = [trend_word['name'] for trend_word in trend_words]
        q = random.choice(trendwords)
        print(q)
        action_decider=0
    user = api.get_user('vedarthsharma')
    if user.friends_count > 4900:
        unfollow(api.followers_ids('vedarthsharma'), api.friends_ids('vedarthsharma'))
    else:
        pass
    my_stream_listen = my_stream_listener()
    my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listen)
    my_stream.filter(languages=["en"],track=[q])
    sleep(60)
