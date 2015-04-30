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
from copy import deepcopy
from ast import literal_eval

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



class ChartData(Resource):
    r_server = redis.Redis(host=load_credentials('redis')['host'], password=load_credentials('redis')['password'])

    def get(self, start_ts, end_ts):
        sec_incr = 3600
        real_start = start_ts-start_ts % sec_incr
        keys_to_get = np.arange(real_start, end_ts+1, sec_incr)
        category_keys = np.char.mod('%d', keys_to_get)
        keys_to_get = list(keys_to_get)
        #print keys_to_get
        data = self.r_server.mget(keys_to_get)

        chart_template = {
            'series':[
                {'name': 'Strongly Negative',
                 'data': []},
                {'name': 'Moderately Negative',
                 'data': []},
                {'name': 'Neutral',
                 'data': []},
                {'name': 'Moderately Positive',
                 'data': []},
                {'name': 'Strongly Positive',
                 'data': []}
            ],
            'categories': list(category_keys),
            'title': {'text': ''}}

        data_dict = {}
        charts = []
        for i, d in enumerate(data):
            time_data = json.loads(d)
            data_dict[str(i)] = time_data
            candidate_data = time_data['candidate_data']
            for j, candidate in enumerate(candidate_data.keys()):
                scores = candidate_data[candidate]['sentiment_scores']['All States']
                if i == 0:
                    charts.append(deepcopy(chart_template))
                    charts[j]['title']['text'] = candidate
                for k, series in enumerate(charts[j]['series']):
                    series['data'].append(scores[str(k+1)])

        return {'response': charts}



# API ROUTING
api.add_resource(Tweets, '/tweets')
api.add_resource(RedisInfo, '/redis-info/')
api.add_resource(ChartData, '/chart-data/<int:start_ts>&<int:end_ts>')

if __name__ == "__main__":
    runner.run()
