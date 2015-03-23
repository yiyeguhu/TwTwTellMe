#!/usr/bin/env python

__author__ = 'tamao'

import sys, time
from daemon import Daemon

from stream.twitter_stream import setup_streaming


class TwitterStreamDaemon(Daemon):
    def run(self):
        while True:
            setup_streaming("TykeFo4CGm0DnBsZA9I49ZEpJ", \
                            "6xgIRO2dBdI6y2x3EBy4hQmZ72c7FZY94MInTeY6YdFTQqFlag", \
                            "261382181-xG3JYfACNcbjyDKyf2imWVeW9X6ZSsJCWwKThwjC", \
                            "AApXzGmbysvrc810Wb8RU4qZPjd6ze3EDVd4U0Riuh4D9")

if __name__ == "__main__":
    daemon = TwitterStreamDaemon('/root/project/stream/twitter_stream.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)