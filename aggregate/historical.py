__author__ = 'tamao'

import sys
import time

import redis

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour, unixtime_to_datetime

#r_server = redis.Redis(host='198.23.67.172', password='dupont')

if __name__ == '__main__':
    # '198.23.67.172' 'password' 1429985000->1430002054
    h = sys.argv[1]
    p = sys.argv[2]

    rough_start_time = int(sys.argv[3])
    print rough_start_time
    start_time = get_start_of_hour(rough_start_time)

    r = redis.Redis(host=h, password=p)

    while start_time < int(time.time()):
        print ""
        print start_time
        unixtime_to_datetime(start_time)
        hour_data = aggregate(start_time, get_end_of_hour(start_time))

        print hour_data
        r.set(str(start_time), hour_data)

        start_time = increase_by_hour(start_time)