__author__ = 'tamao'

import sys
import time

from aggregate.utils import aggregate, get_start_of_hour, get_end_of_hour, increase_by_hour

if __name__ == '__main__':
    rough_start_time = int(sys.argv[1]) # 1429985000
    print rough_start_time
    start_time = get_start_of_hour(rough_start_time)

    while start_time < int(time.time()):
        print aggregate(start_time, get_end_of_hour(start_time))
        start_time = increase_by_hour(start_time)