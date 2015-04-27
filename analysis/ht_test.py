import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient(host="198.11.194.181", port=27017)
    dest_collection = client.newdb.processed
    dest_collection.create_index(
                [("id", pymongo.ASCENDING)],
                unique=True)
    in_text = 0
    not_in_text = 0
    for tweet in client.newdb.tweets.find()[0:10000]:
        txt = tweet['text']
        for ht in tweet['entities']['hashtags']:
            if ht['text'] in txt:
                in_text += 1
            else:
                not_in_text += 1

        print 'in text: %d, not in text: %d' % (in_text, not_in_text)