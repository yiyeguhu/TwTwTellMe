__author__ = 'tamao'

from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler

import argparse

from schema.python.tweet_pb2 import Tweet
from protobufjson.protobuf_json import pb2json, json2pb

from time import time, ctime

import simplejson as json

from pymongo import MongoClient

import os

from pprint import pprint

client = MongoClient()
collection = client['test']['testData']

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, tracks):
        self.tracks = tracks

    def on_data(self, data):
        ob = json.loads(data)

        if "created_at" in ob:
            hit = False
            text = ob['text']

            for track in self.tracks:
                if track in text:
                    hit = True

            if hit:
                tw = Tweet()
                tw.text = text
                tw.timestamp = int(time())

                pprint(tw.SerializeToString())

                json_obj = pb2json(tw)
                pprint(json_obj)

                collection.insert(json_obj)
                # print tw

        return True

    def on_error(self, error):
        pass
        # print error

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

def setup_streaming(consumer_key, consumer_secret, access_token, access_token_secret, tracks):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    l = StdOutListener(tracks)
    stream = Stream(auth, l)
    stream.filter(track=tracks, languages=['en'])

if __name__ == '__main__':
    args = _parse_arguments()
    candidate_names = _get_candidate_names()
    setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret, candidate_names)