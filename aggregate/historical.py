__author__ = 'tamao'

import sys
import time

import redis

import json

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour, unixtime_to_datetime

from stream.mongocollection import *

#r_server = redis.Redis(host='198.23.67.172', password='dupont')

if __name__ == '__main__':
    # [redis-hostname] [redis-pw] [starttime]
    # '198.23.67.172' 'password'
    # starttime: 1429985000->1430002054(hashtags)->142999784(ETL from Mongo Cluster)
    # endtime:
    h = sys.argv[1]
    p = sys.argv[2]
    r = redis.Redis(host=h, password=p)

    rough_start_time = int(sys.argv[3])
    print rough_start_time
    start_time = get_start_of_hour(rough_start_time)

    end_time = int(sys.argv[4])

    # while start_time < int(time.time()):
    while start_time < end_time:
        # unixtime_to_datetime(start_time)
        hour_data = aggregate(cluster_prod_processed, start_time, get_end_of_hour(start_time))

        r.set(str(start_time), json.dumps(hour_data))

        print start_time
        print hour_data

        start_time = increase_by_hour(start_time)