import random
import datetime


def fake_generator(starttime, endtime, period):

    index = make_index(starttime, endtime, period)

    timeseries = {}
    for dt in index:
        all_states = gen_scores()
        dts = dt.strftime('%Y-%m-%d %H:%M:%S')
        timeseries[dts] = {
            "candidate_data": {
                "Ted Cruz": {
                    "All States": all_states
                }
            }
        }

    # my_blob = {
    #     "timeseries": {
    #         "2015-04-03T21:19:11+00:00": {
    #             "candidate_data": {
    #                 "Ted Cruz": {
    #                     "All States": {
    #                         "1": 5,
    #                         "2": 4,
    #                         "3": 4,
    #                         "4": 2,
    #                         "5": 3
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }
    return {"timeseries": timeseries}


def gen_scores():
    max_vol = 20
    return {"Strong Positive": random.randint(0, max_vol),
            "Weak Positive": random.randint(0, max_vol),
            "Neutral": random.randint(0, max_vol),
            "Weak Negative": random.randint(0, max_vol),
            "Strong Negative": random.randint(0, max_vol)
            }


def datetime_partition(start, end, duration):
    current = start
    while start == current or (end-current).days > 0 or ((end-current).days == 0 and (end-current).seconds > 0):
        yield current
        current = current + duration


def date_partition(start, end, period):
    return datetime_partition(start, end, datetime.timedelta(seconds=period))


def make_index(start, end, period=60):
    xsdDateFormat = '%Y-%m-%d %H:%M:%S'
    start = datetime.datetime.strptime(start, xsdDateFormat) # start date
    end = datetime.datetime.strptime(end, xsdDateFormat) # end date
    return date_partition(start, end, period)


# def put():
#     x=1
#     return {
#         "candidate_list": ["Ted Cruz", "Jeb Bush", "Scott Walker", "Chris Christie", "Mike Huckabee", "Marco Rubio",
#                           "Rand Paul", "Rick Santorum", "Rick Perry", "Bobby Jindal"],
#         "average": {
#             "Ted Cruz": {"NY": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]},
#                          "CA": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]}
#                          },
#             "Jeb Bush": {"NY": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]},
#                          "CA": {"1": [5, 3], "2": [5, 3], "3": [5, 3], "4": [5, 3], "5": [5, 3], "6": [5, 3]}
#                          }
#         },
#         "timeseries": {
#             "2015-04-03T21:19:11+00:00": {
#                 "candidate_data": {
#                           "Ted Cruz": {
#                               "All States": {
#                                   "1": 5,
#                                   "2": 4,
#                                   "3": 4,
#                                   "4": 2,
#                                   "5": 3,
#                                   "6": 3
#                               },
#                               "States": {
#                                   "NY": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   },
#                                   "CA": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   }
#                               }
#                           },
#                           "Jeb Bush": {
#                               "All States": {
#                                   "1": 5,
#                                   "2": 4,
#                                   "3": 4,
#                                   "4": 2,
#                                   "5": 3,
#                                   "6": 3
#                               },
#                               "States": {
#                                   "NY": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   },
#                                   "CA": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   }
#                               }
#                           }
#                       },
#                       },
#             "00002": {"timestamp": "2015-04-03T21:19:11+00:00",
#                       "candidate_data": {
#                           "Ted Cruz": {
#                               "All States": {
#                                   "1": 5,
#                                   "2": 4,
#                                   "3": 4,
#                                   "4": 2,
#                                   "5": 3,
#                                   "6": 3
#                               },
#                               "States": {
#                                   "NY": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   },
#                                   "CA": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   }
#                               }
#                           },
#                           "Jeb Bush": {
#                               "All States": {
#                                   "1": 5,
#                                   "2": 4,
#                                   "3": 4,
#                                   "4": 2,
#                                   "5": 3,
#                                   "6": 3
#                               },
#                               "States": {
#                                   "NY": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   },
#                                   "CA": {
#                                       "1": 5,
#                                       "2": 4,
#                                       "3": 4,
#                                       "4": 2,
#                                       "5": 3,
#                                       "6": 3
#                                   }
#                               }
#                           }
#                       },
#                       }
#         }
#     }