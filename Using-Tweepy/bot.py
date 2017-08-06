import tweepy
from credentials import *
from time import sleep
import json
import todo
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

while True:
    print ('What do you want to do?')
    j = 0
    for i in todo.cando:
        print(j,')',i)
        j = j + 1
    q = input()
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
        sleep(10)

