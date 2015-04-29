__author__ = 'tamao'

import sys

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

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour, unixtime_to_datetime

client1 = MongoClient('127.0.0.1', 27018) # new port 27018
collection1 = client1['prod']['tweet']

client2 = MongoClient('198.11.194.181', 27017)
collection2 = client2['prod']['tweet']

if __name__ == '__main__':
    # starttime endtime
    # 1430002054 1430281000
    starttime = sys.argv[1]
    endtime = sys.argv[2]

    while starttime < endtime:
        print starttime
        time2 = get_end_of_hour(starttime) if get_end_of_hour(starttime) < endtime else endtime

        results = collection1.find({'timestamp': {'$gt': starttime, '$lt': time2}}, {'_id':0})
        items = [item for item in results]

        collection2.insert(items)

        starttime = increase_by_hour(starttime)