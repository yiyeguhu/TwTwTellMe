__author__ = 'tamao'

from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler

import argparse

import us

from bson.son import SON

import sys

from time import time, ctime, mktime

import simplejson as json

from pymongo import MongoClient

import os

from pprint import pprint

from langdetect import detect

from math import ceil

from datetime import datetime

# from own packages
from schema.python.tweet_pb2 import Tweet
from protobufjson.protobuf_json import pb2json, json2pb
from algo.geoparser import parse_location, OtherCountry, OtherState, states
from algo.dataminer import find_candidates, OtherCandidate
from algo.tweet_check import return_candidates, return_sentiment
from stream.utils import load_credentials, tweepy_auth

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

print candidates

state_map = us.states.mapping('name', 'abbr')

client = MongoClient('127.0.0.1', 27018) # new port 27018
# collection = client['test']['testData']
collection = client['prod']['tweet']

def get_start_of_hour(timestamp):
    #return timestamp/3600*3600
    return datetime_to_unixtime(unixtime_to_datetime(timestamp).replace(minute=0, second=0))

def get_end_of_hour(timestamp):
    return get_start_of_hour(timestamp) + 3600 - 1

def increase_by_hour(timestamp):
    return get_start_of_hour(timestamp) + 3600

def unixtime_to_datetime(unixtime):
    return datetime.fromtimestamp(unixtime)

def datetime_to_unixtime(dt):
    return int(mktime(dt.timetuple()))

def get_hashtag_stats_for_candidate(cand, starttime, endtime):

    try:
        hashtag_stats = []

        filter_for_candidate  = {'$match': { 'candidate' : cand, 'timestamp' : { '$gt': starttime, '$lt': endtime } } }
        unwind = {"$unwind": "$hashtags"}
        stats = {"$group": {"_id": {"hashtag" : "$hashtags"}, "count": {"$sum": 1} } }
        sorting = {"$sort": SON([("count", -1), ("_id", -1)])}

        pipeline = [filter_for_candidate, unwind, stats, sorting]
        ret = collection.aggregate(pipeline)

        if ret['ok'] == 1.0:
            sorted_result = ret['result']
            for item in sorted_result:
                hashtag_stats.append({item['_id']['hashtag'].encode('ascii','ignore') : item['count']})

        print '\nhashtag_stats'
        print hashtag_stats

        return hashtag_stats

    except:
        return hashtag_stats

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

def _init_sentiment_buckets():
    return {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0}

def get_sentiment_stats_by_state_for_candidate(cand, starttime, endtime):

    try:
        state_buckets = _init_sentiment_buckets_by_state()

        filter_for_candidate  = {'$match': { 'candidate' : cand, 'timestamp' : { '$gt': starttime, '$lt': endtime } } }
        stats = {"$group": {"_id": {"sentiment_int" : "$sentiment_int", "state" : "$state"}, "count": {"$sum": 1} } }

        pipeline = [filter_for_candidate, stats]
        ret = collection.aggregate(pipeline)

        if ret['ok'] == 1.0:
            buckets = ret['result']
            for bucket in buckets:
                if 'sentiment_int' in bucket['_id'] and 'state' in bucket['_id']:
                    state = bucket['_id']['state']
                    sentiment_int = bucket['_id']['sentiment_int']
                    count = bucket['count']

                    state_buckets[state_map[state]][str(sentiment_int)] = count

        return state_buckets
    except:
        return _init_sentiment_buckets_by_state()

def _init_sentiment_buckets_by_state():
    state_buckets = {}
    for state in states:
        state_buckets[state_map[state]] = _init_sentiment_buckets()

    return state_buckets

def get_aggregate_for_candidate(cand, starttime, endtime):
    cand_info = {"tweets":{}, "sentiment_scores": {}}

    # tweets

    # sentiment:
     # (1)all states
    all_states = get_sentiment_stats_for_candidate(cand, starttime, endtime)
    cand_info['sentiment_scores']['All States'] = all_states

    # (2) by state
    # sentiment_by_state = get_sentiment_stats_by_state_for_candidate(cand, starttime, endtime)
    #
    # print sentiment_by_state
    # cand_info['sentiment_scores']['States'] = sentiment_by_state

    # hashtag stats
    hashtag_stats = get_hashtag_stats_for_candidate(cand, starttime, endtime)
    cand_info['hashtags'] = hashtag_stats

    return cand_info

def aggregate(starttime, endtime):
    result = {'candidate_data':{}}

    try:
        for cand in candidates:
            result['candidate_data'][cand.encode('ascii','ignore')] = get_aggregate_for_candidate(cand, starttime, endtime)

        return result
    except:
        return {'candidate_data':{}}

if __name__ == '__main__':
    rough_start_time = int(sys.argv[1])
    print rough_start_time

    start_time = get_start_of_hour(rough_start_time)
    endtime = get_end_of_hour(start_time)

    print aggregate(start_time, endtime)