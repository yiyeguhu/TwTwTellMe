#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import glob
import json
import sys
from dateutil import parser
import calendar
from mongocollection import cluster_client



def list_tweet_files(file_pattern="tweet_*_*.json"):
    return glob.glob(file_pattern)


def modify_tweets(line):
    tweet = json.loads(line)
    dt = parser.parse(tweet['created_at'])
    tweet['timestamp'] = calendar.timegm(dt.timetuple())
    return tweet

def tweets(tweet_files=list_tweet_files()):
    for tweet_file in tweet_files:
        print "reading '%s'" % tweet_file
        with open(tweet_file, 'r') as tweet_reader:
            for line in tweet_reader:
                if len(line) > 2:
                    if line[-2] == ',':
                        line = line[:-2]
                    else:
                        line = line[:-1]
                    yield modify_tweets(line)


def ingest(ingest_tweets=tweets(), db="newdb", collection="tweets"):
    client = cluster_client
    try:
        collection = client[db][collection]
        try:
            collection.insert(ingest_tweets, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError:
            pass
    finally:
        client.close()


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:
        ingest_tweets = tweets(list_tweet_files(sys.argv[1]))
    else:
        ingest_tweets = tweets()
    ingest(ingest_tweets)
