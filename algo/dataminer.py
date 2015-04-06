__author__ = 'tamao'

import simplejson as json
import os

OtherCandidate = 'Other Candidate'

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

def find_candidate(text):
    res = OtherCandidate

    for cand in candidates:
        for term in candidates[cand]:
            if term in text:
                res = cand

    return res
