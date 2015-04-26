from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.runner import Runner
import fake_generator
import datetime
import time
import redis
import numpy as np
from api_auth import load_credentials
import json

app = Flask(__name__)
runner = Runner(app)
api = Api(app)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class Viz(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('timestamp', type=str, required=True)
    parser.add_argument('timestamp_end', type=str, required=False)

    def put(self):
        args = self.parser.parse_args(strict=True)
        timeseries = fake_generator.fake_generator(args['timestamp'], args['timestamp_end'], 60)["timeseries"]
        candidate_list = ["Ted Cruz", "Jeb Bush", "Scott Walker", "Chris Christie", "Mike Huckabee", "Marco Rubio",
                          "Rand Paul", "Rick Santorum", "Rick Perry", "Bobby Jindal"]

        response = [
            {"key": "Strong Positive", "values": []},
            {"key": "Weak Positive", "values": []},
            {"key": "Neutral", "values": []},
            {"key": "Weak Negative", "values": []},
            {"key": "Strong Negative", "values": []}
        ]

        for k, v in sorted(timeseries.iteritems()):
            candidate = candidate_list[0]
            for sent_dict in response:
                dt = datetime.datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
                dt = time.mktime(dt.timetuple())
                sent_dict['values'].append([dt, v['candidate_data'][candidate]['All States'][sent_dict['key']]])
        return response


class Tweets(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index', type=int, required=True)
    parser.add_argument('candidate', type=str, required=True)

    def put(self):
        args = self.parser.parse_args(strict=True)
        return [
            {"user_name": "User Name",
             "user_state": "State",
             "tweet_text": "Tweet text here",
             "sentiment_score": 6},
            {"user_name": "User Name",
             "user_state": "State",
             "tweet_text": "Tweet text here",
             "sentiment_score": 6}
        ]

class RedisInfo(Resource):
    r_server = redis.Redis(host=load_credentials('redis')['host'], password=load_credentials('redis')['password'])
    keys_we_have = r_server.keys()
    min_ts = int(min(keys_we_have))
    max_ts = int(max(keys_we_have))

    def get(self):
        return [self.min_ts, self.max_ts]

class RedisProd(Resource):
    r_server = redis.Redis(host=load_credentials('redis')['host'], password=load_credentials('redis')['password'])

    def get(self, start_ts, end_ts):
        sec_incr = 3600
        real_start = start_ts-start_ts % sec_incr
        keys_to_get = list(np.arange(real_start, end_ts+1, sec_incr))
        #print keys_to_get
        data = self.r_server.mget(keys_to_get)

        data = data[0].replace("'", "\"")
        #print json.loads(data[0].replace("'", "\""))

        return data

        #data = self.r_server.get(posixtime)
        #return {'success': data}

class RedisTest(Resource):
    r_server = redis.Redis(host='198.23.67.172', password='dupont')
    def put(self, posixtime):
        my_blob = {
                "candidate_data": {
                  "Ted Cruz": {
                    "tweets": [
                      {
                        "user_name": "User Name",
                        "user_state": "State",
                        "tweet_text": "Tweet text here",
                        "sentiment_score": 6
                      },
                      {
                        "user_name": "User Name",
                        "user_state": "State",
                        "tweet_text": "Tweet text here",
                        "sentiment_score": 6
                      }
                    ],
                    "sentiment_scores": {
                      "All States": {
                        "1": 5,
                        "2": 4,
                        "3": 4,
                        "4": 2,
                        "5": 3
                      },
                      "States": {
                        "NY": {
                          "1": 5,
                          "2": 4,
                          "3": 4,
                          "4": 2,
                          "5": 3
                        },
                        "CA": {
                          "1": 5,
                          "2": 4,
                          "3": 4,
                          "4": 2,
                          "5": 3
                        }
                      }
                    }
                  },
                  "Jeb Bush": {
                    "tweets": [
                      {
                        "user_name": "User Name",
                        "user_state": "State",
                        "tweet_text": "Tweet text here",
                        "sentiment_score": 6
                      },
                      {
                        "user_name": "User Name",
                        "user_state": "State",
                        "tweet_text": "Tweet text here",
                        "sentiment_score": 6
                      }
                    ],
                    "sentiment_scores": {
                      "All States": {
                        "1": 5,
                        "2": 4,
                        "3": 4,
                        "4": 2,
                        "5": 3
                      },
                      "States": {
                        "NY": {
                          "1": 5,
                          "2": 4,
                          "3": 4,
                          "4": 2,
                          "5": 3,
                          "6": 3
                        },
                        "CA": {
                          "1": 5,
                          "2": 4,
                          "3": 4,
                          "4": 2,
                          "5": 3
                        }
                      }
                    }
                  }
                }
              }

        self.r_server.set(posixtime, my_blob)
        return {'success': 'success'}

    def get(self, posixtime):
        data = self.r_server.get(posixtime)
        return {'success': data}

# API ROUTING
api.add_resource(Viz, '/viz')
api.add_resource(Tweets, '/tweets')
api.add_resource(RedisTest, '/redis-test/<float:posixtime>')
api.add_resource(RedisInfo, '/redis-info/')
api.add_resource(RedisProd, '/redis-prod/<int:start_ts>&<int:end_ts>')

if __name__ == "__main__":
    runner.run()
