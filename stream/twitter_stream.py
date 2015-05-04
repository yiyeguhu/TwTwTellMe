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

from math import ceil

# from own packages
from schema.python.tweet_pb2 import Tweet
from protobufjson.protobuf_json import pb2json, json2pb
from algo.geoparser import parse_location, OtherCountry, OtherState
from algo.dataminer import find_candidates, OtherCandidate
from algo.tweet_check import return_candidates, return_sentiment, return_themes, convert_sentiment
from utils import load_credentials, tweepy_auth
from analysis.classify_structure_tweets import convert_sent

from mongocollection import *

# client0 = MongoClient('127.0.0.1')
# client0.the_database.authenticate('admin', 'QS6TnHlb', source='admin')
# collection0 = client0['newdb']['tweets']

# client1 = MongoClient('127.0.0.1', 27018) # new port 27018
# # collection = client['test']['testData']
# collection1 = client1['prod']['tweet']
#
# client2 = MongoClient('198.11.194.181')
# collection2 = client2['prod']['tweet']
# collection3 = client2['newdb']['tweets']

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        try:
            ob = json.loads(data)
            print ob
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

def online_process(ob):
    if "created_at" in ob and 'text' in ob:

        text = ob['text']

        if detect(text) == 'en':
            if 'entities' in ob and 'hashtags' in ob['entities']:
                ht = [hashtag['text'] for hashtag in ob['entities']['hashtags']]
            else:
                ht = []
            um = [user_mention['screen_name']+', '+user_mention['name'] for user_mention in ob['entities']['user_mentions']]

            extxt = text + ', ' + ', '.join(ht)
            extxt = extxt + ', ' + ', '.join(um)

            cands = [cand for cand in return_candidates(extxt) if cand in candidates]

            if cands:
                tw = Tweet()

                # required fields
                tw.text = text
                # tw.timestamp = int(time())
                tw.timestamp = int(time())

                tw.sentiment = return_sentiment(extxt)
                tw.sentiment_int = convert_sent(tw.sentiment)
                # tw.sentiment_int = convert_sentiment(tw.sentiment)

                # optional
                if 'user' in ob:
                    if 'name' in ob['user']:
                        tw.user_name = ob['user']['name']

                    # try:
                    #     if 'location' in ob['user']:
                    #         state_name, country_name = parse_location(ob['user']['location'])
                    #         if state_name != OtherState:
                    #             tw.state = state_name
                    #         if country_name != OtherCountry:
                    #             tw.country = country_name
                    # except:
                    #     print "Geocoder exception"

                detected_themes = return_themes(extxt)
                for theme in detected_themes:
                    tw.themes.append(theme)

                tw.hashtags = ht
                # if 'entities' in ob and 'hashtags' in ob['entities']:
                #     tags = ob['entities']['hashtags']
                #     for tag in tags:
                #         if 'text' in tag:
                #             tw.hashtags.append(tag['text'])

                for cand in cands:
                    tw.candidate = cand
                    json_ob = pb2json(tw)
                    # print json_ob
                    test_tweet.insert(json_ob, continue_on_error=True)
                    # collection2.insert(json_ob, continue_on_error=True)

# def setup_streaming(consumer_key, consumer_secret, access_token, access_token_secret, tracks):
def setup_streaming(tracks):

    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)

    # print os.path.dirname(os.path.realpath(__file__)) + "/../stream/candidates.json"
    credentials = load_credentials(True, os.path.dirname(os.path.realpath(__file__)) + "/credentials0.json")
    auth = tweepy_auth(credentials, user=True)

    l = StdOutListener()
    stream = Stream(auth, l)
    # stream.filter(track=tracks, languages=['en'])
    # stream.filter(languages=['en'])

    # filename1 = os.path.dirname(os.path.realpath(__file__)) + "/../stream/search/candidates.json"
    # with open(filename1) as f:
    #     candidate_dict = json.load(f)
    #
    # track_terms = []
    # for candidate in candidate_dict.keys():
    #     for term in candidate_dict[candidate]:
    #         track_terms.append(term)
    # print track_terms

    stream.filter(track=tracks)
    # stream.filter(track=track_terms)
    # stream.sample()

if __name__ == '__main__':
    # args = _parse_arguments()

    candidate_names = _get_candidate_names()

    setup_streaming(candidate_names)
    # setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret, candidate_names)

    # setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret)