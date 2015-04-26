import pymongo
from algo.tweet_check import return_candidates, return_sentiment, return_themes
from datetime import datetime, tzinfo
import time
import json
from os import environ

pwd = environ['MONGOPWD']

client = pymongo.MongoClient(host="198.11.194.181", port=27017)
# client.newdb.authenticate('TwTw', pwd)

for tweet in client.newdb.tweets.find()[0:50]:
    dt = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    print tweet['created_at'], dt
    ht = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    txt = tweet['text']
    txtht = txt + ', '.join(ht)
    processed = {
        'text': txt,
        'hashtags':ht,
        'id': tweet['id'],
        'user_id': tweet['user']['id'],
        'user_name': tweet['user']['name'],
        'screen_name': tweet['user']['screen_name'],
        'raw_location': tweet['user'].get('location', 'not specified'),
        'candidate': return_candidates(txtht),
        'sentiment': return_sentiment(txtht),
        'themes': return_themes(txtht),
        'timestamp': time.mktime(dt.timetuple())
    }


    # print processed
    # try:
    #     client.newdb.processed_tweets.insert(processed, continue_on_error=True)
    #     print 'inserted processed tweet'
    # except pymongo.errors.DuplicateKeyError:
    #     print 'duplicate key - skipping'
    #
    # tweet['processed'] = True
    # client.newdb.tweets.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)
    # print 'updated processed flag'


# with open('jsonout.json', 'w') as json_file:
#     json.dump([tweet for tweet in client.newdb.tweets.find()[0:50]], json_file)
#     json_file.close()
#


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
    print f