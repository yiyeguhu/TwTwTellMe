__author__ = 'tamao'

from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler

import argparse

from schema.python.tweet_pb2 import Tweet

from time import time, ctime

import simplejson as json

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        #print(data)
        ob = json.loads(data)
        if "created_at" in ob:
            tw = Tweet()
            tw.text = ob['text']
            tw.timestamp = int(time())
            s = tw.__str__()
            print s
        return True

    def on_error(self, error):
        print error

def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer_key', help='Consumer key')
    parser.add_argument('--consumer_secret', help='Consumer secret')
    parser.add_argument('--access_token', help='Access token')
    parser.add_argument('--access_token_secret', help='Access token secret')

    args = parser.parse_args()
    return args

def setup_streaming(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    l = StdOutListener()
    stream = Stream(auth, l)
    stream.sample()

if __name__ == '__main__':
    args = _parse_arguments()
    setup_streaming(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret)