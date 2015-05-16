__author__ = 'tamao'

from pymongo import MongoClient

# mongo
client = MongoClient('127.0.0.1', 27018) # new port 27018

test_tweet = client['test']['tweet']

prod_tweet = client['prod']['tweet']

# cluster
cluster_client = MongoClient('198.11.194.188')

cluster_prod_tweet = cluster_client['prod']['tweet']
cluster_prod_processed = cluster_client['prod']['processed']

cluster_newdb_tweets = cluster_client['newdb']['tweets']