__author__ = 'tamao'

import simplejson as json
import os

OtherCandidate = 'Other Candidate'

filename = os.path.dirname(os.path.realpath(__file__)) + "/../resources/candidates.json"
with open(filename) as f:
    candidates = json.load(f)

def find_candidates(text):
    lower_text = text.lower()
    res = set()

    for cand in candidates:
        for term in candidates[cand]:
            t = term.lower()
            if t in lower_text:
                res.add(cand)

    return list(res)
