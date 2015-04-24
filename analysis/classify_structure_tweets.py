import pymongo
from algo.tweet_check import return_candidates, return_sentiment
from datetime import datetime
import time
import json

# client = pymongo.MongoClient()
#
# for tweet in client.newdb.tweets.find():
#     dt = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#     client.processed.tweets.insert({
#         'text': tweet['text'],
#         'id': tweet['id'],
#         'user_id': tweet['user']['id'],
#         'user_name': tweet['user']['name'],
#         'candidate': return_candidates(tweet['text']),
#         'sentiment': return_sentiment(tweet['text']),
#         'timestamp': time.mktime(dt.timetuple())
#     })


with open('../stream/search/tweet_0_2015-04-22.0.json','r') as f:
    data = json.load(f)

for tweet in data:
    dt = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    print ({
        'text': tweet['text'],
        'id': tweet['id'],
        'user_id': tweet['user']['id'],
        'user_name': tweet['user']['name'],
        'candidate': return_candidates(tweet['text']),
        'sentiment': return_sentiment(tweet['text']),
        'timestamp': time.mktime(dt.timetuple())
    })