__author__ = 'tamao'

from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler

import argparse

from time import time, ctime

import simplejson as json

from pymongo import MongoClient

import os

from pprint import pprint

from langdetect import detect

from math import ceil, floor

import calendar

# from own packages
from schema.python.tweet_pb2 import Tweet
from protobufjson.protobuf_json import pb2json, json2pb
from algo.geoparser import parse_location, OtherCountry, OtherState
from algo.dataminer import find_candidates, OtherCandidate
from algo.tweet_check import return_candidates, return_sentiment, return_themes, convert_sentiment
from utils import load_credentials, tweepy_auth

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

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

client0 = MongoClient('127.0.0.1')
client0.the_database.authenticate('admin', 'QS6TnHlb', source='admin')
collection0 = client0['newdb']['tweets']

client1 = MongoClient('127.0.0.1', 27018) # new port 27018
# collection = client['test']['testData']
collection1 = client1['prod']['tweet']

client2 = MongoClient('198.11.194.181')
collection2 = client2['prod']['tweet']
collection3 = client2['newdb']['tweets']
collection4 = client2['prod']['processed']

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        try:
            ob = json.loads(data)
            online_process(ob)
        except:
            pass

        return True

    def on_error(self, error):
        print(error)
        return True

    def on_timeout(self):
        return True

def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer_key', help='Consumer key')
    parser.add_argument('--consumer_secret', help='Consumer secret')
    parser.add_argument('--access_token', help='Access token')
    parser.add_argument('--access_token_secret', help='Access token secret')

    args = parser.parse_args()
    return args

def _get_candidate_names():
    filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
    with open(filename) as f:
        candidates = json.load(f)

    pprint(candidates)

    candidate_names = []
    for candidate in candidates:
        names = candidates[candidate]
        for name in names:
            candidate_names.append(name)

    print(candidate_names)

    return candidate_names

def online_process(tweet):
    if "created_at" in tweet and 'text' in tweet and detect(tweet['text']) == 'en':

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
                'sentiment': sent,
                'sentiment_int': convert_sent(sent),
                'themes': return_themes(extxt),
                'timestamp': int(time())
        }

        cands = return_candidates(extxt)
        for cand in cands:
            if cand in candidates:
                processed['candidate'] = cand
                collection4.insert(processed, continue_on_error=True)

# def setup_streaming(consumer_key, consumer_secret, access_token, access_token_secret, tracks):
def setup_streaming(tracks):

    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)

    # print os.path.dirname(os.path.realpath(__file__)) + "/../stream/candidates.json"
    credentials = load_credentials(True, os.path.dirname(os.path.realpath(__file__)) + "/credentials.json")
    auth = tweepy_auth(credentials, user=True)

    l = StdOutListener()
    stream = Stream(auth, l)
    # stream.filter(track=tracks, languages=['en'])
    # stream.filter(languages=['en'])
    stream.filter(track=tracks)
    # stream.sample()

if __name__ == '__main__':
    # args = _parse_arguments()

    candidate_names = _get_candidate_names()

    setup_streaming(candidate_names)
    # setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret, candidate_names)

    # setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret)