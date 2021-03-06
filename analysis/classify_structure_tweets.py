import pymongo
from algo.tweet_check import return_candidates, return_sentiment, return_themes
from dateutil import parser
import time
import calendar
from datetime import datetime
import json
from math import floor, ceil

import os

from stream.mongocollection import *

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

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

if __name__ == '__main__':
    # client = pymongo.MongoClient(host="198.11.194.181", port=27017)

    # src_collection = client.newdb.tweets
    # dest_collection = client.prod.processed

    src_collection = cluster_newdb_tweets
    dest_collection = cluster_prod_processed

    dest_collection.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True)

    counter = 0
    # for tweet in src_collection.find():
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430247600, '$lt': 1430301600}}):
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430410447}}):
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430301600, '$lt': 1430312400}}):
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430413200, '$lt': 1430409600}}):

    # for tweet in src_collection.find({'timestamp': {'$gte': 1430440140}}):
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430410447}}):
    # for tweet in src_collection.find({'timestamp': {'$gte': 1430733120}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1430837691}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1430860304}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1430866800}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1430985409}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1430866800, '$lt': 1430956800}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431010800, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431014400, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431018000, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431025200, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431028800, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431036000, '$lt': 1431050400}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431457200, '$lt': 1431496800}}):
    # for tweet in src_collection.find({'timestamp': {'$gt': 1431594000, '$lt': 1431630000}}):
    for tweet in src_collection.find({'timestamp': {'$gt': 1431705600, '$lt': 1431756000}}):
        try:
            dt = parser.parse(tweet['created_at'])

            ht = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
            um = [user_mention['screen_name']+', '+user_mention['name'] for user_mention in tweet['entities']['user_mentions']]
            txt = tweet['text']

            extxt = txt + ', ' + ', '.join(ht)
            extxt = extxt + ', ' + ', '.join(um)

            sent = return_sentiment(extxt)

            processed = {
                'text': txt,
                'hashtags':ht,
                'id': tweet['id'],
                'user_id': tweet['user']['id'],
                'user_name': tweet['user']['name'],
                'screen_name': tweet['user']['screen_name'],
                'raw_location': tweet['user'].get('location', 'not specified'),
                # 'candidate': return_candidates(extxt),
                'sentiment': sent,
                'sentiment_int': convert_sent(sent),
                'themes': return_themes(extxt),
                'timestamp': calendar.timegm(dt.timetuple())
            }

            cands = [cand for cand in return_candidates(extxt) if cand in candidates]

            inserted = []
            for cand in cands:
                processed['candidate'] = cand
                inserted.append(processed.copy())

            if inserted:
                try:
                    dest_collection.insert(inserted, continue_on_error=True)
                except pymongo.errors.DuplicateKeyError:
                    print 'duplicate key - skipping'

            counter += 1
            if not counter % 100:
                print ""
                print calendar.timegm(dt.timetuple())
                print counter

            # tweet['processed'] = True
            # src_collection.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)
        except:
            print "error in post-processing"

