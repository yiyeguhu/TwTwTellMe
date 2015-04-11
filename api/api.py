from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.runner import Runner
import fake_generator
import datetime
import time

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


# API ROUTING
api.add_resource(Viz, '/viz')
api.add_resource(Tweets, '/tweets')

if __name__ == "__main__":
    runner.run()