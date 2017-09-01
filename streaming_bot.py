import os
import tweepy
from time import sleep
import random
import json
import re
import bad
import sqlite3
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
conn = sqlite3.connect('twitter_data.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Twitter(name TEXT, screen_name TEXT, bio TEXT, count INTEGER)')

class my_stream_listener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 27

    def on_data(self,raw_data):
        sleep(10)
        offend = False
        js = json.loads(raw_data)
        try:
            cur.execute('SELECT count FROM Twitter WHERE screen_name = ?',(js['user']['screen_name'],))
            count = int(cur.fetchone()[0])
            cur.execute('UPDATE Twitter SET count = ? WHERE screen_name = ?',(count+1,js['user']['screen_name']))
        except:
            cur.execute('INSERT INTO Twitter(name,screen_name,bio,count) VALUES (?,?,?,1)',(js['user']['name'],js['user']['screen_name'],js['user']['description']))
        conn.commit()
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
    for tweet in tweepy.Cursor(api.search, 'python').items(1000):
        try:
            tweet.retweet()
        except Exception as e:
            print('Could not retweet because',e)
            pass
        try:
            tweet.favorite()
        except:
            pass
        try:
            api.destroy_friendship(assholes[i])
            print('unfollowed',assholes[i])
            sleep(50)
        except tweepy.TweepError:
            print(e)
            sleep(15*60)
        curr_time()

def curr_time():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #Heroku is about 6:30 hrs behind IST.


action_decider = 0
while True:
    curr_time()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Twitter(name TEXT, screen_name TEXT, bio TEXT, count INTEGER)')
    if action_decider == 0:
        q = random.choice(keywords)
        print(q)
        action_decider=1
    else:
        #23424848
        trends_list = api.trends_place(1)
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
    cur.close()
    sleep(60)
