__author__ = 'tamao'

USA = 'United States of America'
OtherCountry = "Other Country"
OtherState = "Other State"

states = [
        'Alaska',
        'Alabama',
        'Arkansas',
        'Arizona',
        'California',
        'Colorado',
        'Connecticut',
        'District of Columbia',
        'Delaware',
        'Florida',
        'Georgia',
        'Hawaii',
        'Iowa',
        'Idaho',
        'Illinois',
        'Indiana',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Massachusetts',
        'Maryland',
        'Maine',
        'Michigan',
        'Minnesota',
        'Missouri',
        'Mississippi',
        'Montana',
        'North Carolina',
        'North Dakota',
        'Nebraska',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'Nevada',
        'New York',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Virginia',
        'Vermont',
        'Washington',
        'Wisconsin',
        'West Virginia',
        'Wyoming'
]

from geopy.geocoders import Nominatim
geolocator = Nominatim()

def parse_address(addr):
    tokens = addr.split(', ')
    l = len(tokens)

    country = tokens[l-1]
    if tokens[l-2].isdigit():
        state = tokens[l-3]
    else:
        state = tokens[l-2]

    if state not in states:
        state = OtherState

    if country != USA:
        state = OtherState
        country = OtherCountry

    return state, country

def parse_location(loc):
    state, country = OtherState, OtherCountry

    stdloc = geolocator.geocode(loc, timeout=10)
    if stdloc is not None:
        state, country = parse_address(stdloc.address)

    return state, country

