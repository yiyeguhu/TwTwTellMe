__author__ = 'tamao'

import sys
import time

import redis

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour, unixtime_to_datetime

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

        hour_data = aggregate(starttime, currenttime)
        r.set(str(starttime), hour_data)

        print currenttime
        unixtime_to_datetime(currenttime)
        unixtime_to_datetime(starttime)

        time.sleep(5)