import pymongo
from dateutil import parser
import calendar


if __name__ == '__main__':
    client = pymongo.MongoClient(host="198.11.194.181", port=27017)

    src_collection = client.newdb.tweets

    counter = 0
    for tweet in src_collection.find():
        try:
            if not tweet.get('timestamp', None):
                if tweet.get('timestamp_ms', None):
                    tweet['timestamp'] = int(tweet.get('timestamp_ms', None))/1000
                    counter += 1
                    src_collection.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)
                elif tweet.get('created_at', None):
                    dt = parser.parse(tweet.get('created_at', None))
                    tweet['timestamp'] = calendar.timegm(dt.timetuple())
                    counter += 1
                    src_collection.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)
                else:
                    pass
                if not counter % 100:
                    print counter
        except:
            print "error in post-processing"