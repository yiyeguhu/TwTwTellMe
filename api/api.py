from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.runner import Runner

app = Flask(__name__)
runner = Runner(app)
api = Api(app)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class Viz(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index', type=int, required=True)
    parser.add_argument('init', type=bool, required=True)


    def put(self):
        args = self.parser.parse_args(strict=True)

        return {
            "candidate_list": ["Ted Cruz", "Jeb Bush", "Scott Walker", "Chris Christie", "Mike Huckabee", "Marco Rubio",
                              "Rand Paul", "Rick Santorum", "Rick Perry", "Bobby Jindal"],
            "average": {
                "Ted Cruz": {"NY": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]},
                             "CA": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]}
                             },
                "Jeb Bush": {"NY": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]},
                             "CA": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]}
                             }
            },
            "timeseries": {
                "00001": {"timestamp": "2015-04-03T21:19:11+00:00",
                          "candidate_data": {
                              "Ted Cruz": {
                                  "All States": {
                                      "1": 5,
                                      "2": 4,
                                      "3": 4,
                                      "4": 2,
                                      "5": 3,
                                      "6": 3
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
                                          "5": 3,
                                          "6": 3
                                      }
                                  }
                              },
                              "Jeb Bush": {
                                  "All States": {
                                      "1": 5,
                                      "2": 4,
                                      "3": 4,
                                      "4": 2,
                                      "5": 3,
                                      "6": 3
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
                                          "5": 3,
                                          "6": 3
                                      }
                                  }
                              }
                          },
                          }
                "00002": {"timestamp": "2015-04-03T21:19:11+00:00",
                          "candidate_data": {
                              "Ted Cruz": {
                                  "All States": {
                                      "1": 5,
                                      "2": 4,
                                      "3": 4,
                                      "4": 2,
                                      "5": 3,
                                      "6": 3
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
                                          "5": 3,
                                          "6": 3
                                      }
                                  }
                              },
                              "Jeb Bush": {
                                  "All States": {
                                      "1": 5,
                                      "2": 4,
                                      "3": 4,
                                      "4": 2,
                                      "5": 3,
                                      "6": 3
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
                                          "5": 3,
                                          "6": 3
                                      }
                                  }
                              }
                          },
                          }
            }
        }


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