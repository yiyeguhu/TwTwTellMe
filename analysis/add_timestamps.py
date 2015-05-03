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
                dt = parser.parse(tweet['created_at'])
                tweet['timestamp'] = calendar.timegm(dt.timetuple())
                src_collection.update({'_id': tweet['_id']}, {"$set": tweet}, upsert=False)
                counter += 1
            if not counter % 100:
                print counter
        except:
            print "error in post-processing"

