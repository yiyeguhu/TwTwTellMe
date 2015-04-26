import pymongo
from algo.tweet_check import return_candidates, return_sentiment, return_themes
from dateutil import parser
import time
import calendar
from datetime import datetime
import json
from math import floor, ceil
from os import environ

# Convert (-1,1) sentiment: (-1,-.5] -> 1, (.5,0] -> 2, 0 -> 3, [0,.5) -> 4, [.5,1) -> 5
def convert_sent(f):
    f = 2*f + 3
    if f < 3:
        f = floor(f)
    elif f > 3:
        f = ceil(f)
    if f < 1:
        f = 1
    elif f > 5:
        f = 5
    return int(f)

pwd = environ['MONGOPWD']

client = pymongo.MongoClient(host="198.11.194.181", port=27017)

counter = 0
for tweet in client.newdb.tweets.find()[0:50]:
    dt = parser.parse(tweet['created_at'])
    ht = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    txt = tweet['text']
    txtht = txt + ', '.join(ht)
    sent = return_sentiment(txtht)
    processed = {
        'text': txt,
        'hashtags':ht,
        'id': tweet['id'],
        'user_id': tweet['user']['id'],
        'user_name': tweet['user']['name'],
        'screen_name': tweet['user']['screen_name'],
        'raw_location': tweet['user'].get('location', 'not specified'),
        'candidate': return_candidates(txtht),
        'sentiment': sent,
        'sentiment_int': convert_sent(sent),
        'themes': return_themes(txtht),
        'timestamp': calendar.timegm(dt.timetuple())
    }
    try:
        client.newdb.processed_tweets.insert(processed, continue_on_error=True)
        counter += 1
        if not counter % 100:
            print counter
    except pymongo.errors.DuplicateKeyError:
        print 'duplicate key - skipping'

    tweet['processed'] = True
    client.newdb.tweets.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)

