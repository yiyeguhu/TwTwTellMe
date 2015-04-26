__author__ = 'Matt'

import json

def load_credentials(path='auth.json'):
    try:
        with open(path) as f:
            credentials = json.load(f)
    except:
        credentials=None
        print "Cannot load auth.json"
    return credentials