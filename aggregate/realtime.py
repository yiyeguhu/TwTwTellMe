__author__ = 'tamao'

import sys
import time

import json

import redis

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour, unixtime_to_datetime

from stream.mongocollection import *

#r_server = redis.Redis(host='198.23.67.172', password='dupont')

if __name__ == '__main__':
    # [redis-hostname] [redis-pw]
    # '198.23.67.172' 'password'
    h = sys.argv[1]
    p = sys.argv[2]
    r = redis.Redis(host=h, password=p)

    while True:
        currenttime = int(time.time())
        starttime = get_start_of_hour(currenttime)

        hour_data = aggregate(prod_tweet, starttime, currenttime)
        r.set('test_'+str(starttime), json.dumps(hour_data))

        print currenttime
        print unixtime_to_datetime(currenttime)
        print unixtime_to_datetime(starttime)
        print starttime
        print hour_data
        print ""

        time.sleep(5)