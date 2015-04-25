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
from algo.tweet_check import return_candidates, return_sentiment
from stream.utils import load_credentials, tweepy_auth

client = MongoClient('127.0.0.1', 27018) # new port 27018
# collection = client['test']['testData']
collection = client['prod']['tweet']

def get_start_of_hour(timestamp):
    return timestamp/3600*3600

def get_sentiment_stats_for_candidate(cand, starttime, endtime):

    try:
        result = _init_sentiment_buckets()

        filter_for_candidate  = {'$match': { 'candidate' : cand, 'timestamp' : { '$gt': starttime, '$lt': endtime } } }
        stats = {"$group": {"_id": {"sentiment_int" : "$sentiment_int"}, "count": {"$sum": 1} } }
        pipeline = [filter_for_candidate, stats]
        ret = collection.aggregate(pipeline)


        if ret['ok'] == 1.0:
            buckets = ret['result']
            for bucket in buckets:
                result[str(bucket['_id']['sentiment_int'])] = bucket['count']

        return result
    except:
        return _init_sentiment_buckets()

def get_aggregate_for_candidate(cand, starttime, endtime):
    cand_info = {"tweets":{}, "sentiment_scores": {}}

    # tweets

    # sentiment:
    # (1)all states
    all_states = get_sentiment_stats_for_candidate(cand, starttime, endtime)
    cand_info['sentiment_scores']['All States'] = all_states

    # by state

    return cand_info

def _init_sentiment_buckets():
    return {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0}

def get_sentiment_stats_by_state_for_candidate():
    pass

