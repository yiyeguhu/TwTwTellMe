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

from twitter_stream import online_process, collection0, collection2

# collection0 -> ETL -> collection2

if __name__ == '__main__':
    # starttime endtime
    # 1429828939 1429999571
    starttime = int(sys.argv[1])
    endtime = int(sys.argv[2])

    while starttime < endtime:
        print starttime
        time2 = get_end_of_hour(starttime) if get_end_of_hour(starttime) < endtime else endtime

        inserts = []

        returns = collection0.find({'timestamp_ms': {'$gt': str(starttime*1000), '$lt': str(time2*1000)}}, {'_id':0})
        for item in returns:
            ret = online_process(item)
            inserts.extend(ret)

        starttime = increase_by_hour(starttime)