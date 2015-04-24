import pymongo
from algo.tweet_check import return_candidates, return_sentiment
from datetime import datetime
import time

client = pymongo.MongoClient()
for tweet in client.newdb.tweets.find():
    dt = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    client.processed.tweets.insert({
        'text': tweet['text'],
        'id': tweet['id'],
        'user_id': tweet['user']['id'],
        'user_name': tweet['user']['name'],
        'candidate': return_candidates(tweet['text']),
        'sentiment': return_sentiment(tweet['text']),
        'timestamp': time.mktime(dt.timetuple())
    })