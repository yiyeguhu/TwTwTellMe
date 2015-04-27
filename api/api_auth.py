__author__ = 'Matt'

import json

def load_credentials(key,path='auth.json'):
    try:
        with open(path) as f:
            credentials = json.load(f)
        return credentials[key]
    except:
        print "Cannot load auth.json"


if __name__ == "__main__":
    print load_credentials('redis')['password']