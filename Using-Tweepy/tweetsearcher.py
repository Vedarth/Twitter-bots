import urllib.request as ur, urllib.parse as up, urllib.error
import twurl
import ssl
import json
import re
import objectpath
import pytz
import sys

non_bmp = dict.fromkeys(range(0x1000, sys.maxunicode + 1), 0xfffd)
TWITTER_URL = 'https://api.twitter.com/1.1/search/tweets.json?'

ctx=ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    print('')
    query = input('Enter the query:')
    if len(query)<1:
        break
    url = twurl.augment(TWITTER_URL,
                        {'q':query, 'count':'100'})
    con = ur.urlopen(url, context = ctx)
    jas = json.loads(con.read().decode())
    tree_obj = objectpath.Tree(jas)
    tweets = list(tree_obj.execute('$..text'))
    for x in tweets:
        try:
            print(x)
        except:
            print(x.translate(non_bmp))
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
