from textblob import TextBlob
import re
from bs4 import BeautifulSoup
import urllib2

from math import ceil

# internal function to remove punctuation from text and turn all characters lowercase

def clean_text(text):
    remove_punctuation = '[!?.,:()\*+-<>=/^_`{}|~#"]' # punctuation to remove from tweets
    return re.sub(remove_punctuation, '', text).lower()

# internal function to check text for a list of terms (substring)
# input: text, lists of terms to check for
# output: true if all lists have at least one term within the text, false if at least one of the lists of terms is entirely not represented in text

def check_text(text, chk):
    for item in chk:
        curFlag = False
        for i in item:
            if i in text:
                curFlag = True
        if curFlag is False:
            return False
    return True

# internal function to check text for a list of terms (whole words)
# input: text, lists of terms to check for in the format of [X, lists] where X is the # of terms in the list that need to be matched in text for success
# output: true if at least one list has a match, false if no lists have matches

def check_theme(text, chk):
    stext = text.split()
    for item in chk:
        curFlag = False
        target_count = item[0]
        target_phrase = item[1]
        found_count = 0
        for word in stext:
            for phrase in target_phrase:
                if word == phrase:
                    found_count += 1
                    if found_count >= target_count:
                        return True
    return False

# internal function to form a candidate listing to pass to check_candidates

def form_cand(cand, subwords, addsubwords, wholewords, addwholewords):
    chk = []
    cand_sub = []
    cand_whole = []
    for word in subwords:
        cand_sub.append(word)
    for word in addsubwords:
        cand_sub.append(word)
    for word in wholewords:
        cand_whole.append(word)
    for word in addwholewords:
        cand_whole.append(word)
    chk.append(cand)
    chk.append(cand_sub)
    chk.append(cand_whole)
    return chk

# internal function to check text for a list of terms (both substrings and whole words)
# input: text, lists of terms to check for in the format of [cand, list1, list2] where cand is the candidate's last name, list1 is substring matched terms, list2 is whole-word matched terms
# output: true if at least one list has a match, false if no lists have matches

def check_candidates(text, chk):
    if chk[0] not in text:
        return False
    curFlag = False
    for i in chk[1]:
        if i in text:
            return True
    stext = text.split()
    for word in stext:
        for term in chk[2]:
            if word == term:
                return True
    return False


# return_candidates_logic
# input: string containing English-language text (tweetText)
# output: returns a list of candidates detected in the text
    
def return_candidates_logic(tweetText):
    
    text = clean_text(tweetText)
    
    keywords = ["candidate", "republican", "gop", "president", "campaign", "primary", "elect", "politic", "vote", "democrat", "caucus", "2016"]
    
    candidates = []
    comm_cand = ["bush", "christie", "cruz", "jindal", "huckabee", "paul", "perry", "rubio", "santorum", "walker"]
    cand_form = ["Jeb Bush", "Chris Christie", "Ted Cruz", "Bobby Jindal", "Mike Huckabee", "Rand Paul", "Rick Perry", "Marco Rubio", "Rick Santorum", "Scott Walker"]
    cand_type = [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
    comm_cand_sub = []
    comm_cand_whole = []
    cand_themes = []

    # Jeb Bush

    comm_cand_sub.append(["jebbush", "righttorise", "govbush", "goveror", "right to rise"])
    comm_cand_whole.append(["jeb", "gov", "florida", "fl"])
    themes = []
    themes.append([1, ["righttorise"]])
    cand_themes.append(themes)

    # Chris Christie

    comm_cand_sub.append(["chrischristie", "leadershipmattersforamerica", "govchristie", "governor", "leadership matters for america"])
    comm_cand_whole.append(["chris", "gov", "governor", "jersey", "nj"])
    themes = []
    themes.append([1, ["leadershipmattersforamerica"]])
    cand_themes.append(themes)

    # Ted Cruz

    comm_cand_sub.append(["tedcruz", "4principle", "senator"])
    comm_cand_whole.append(["ted", "sen"])
    themes = []
    themes.append([1, ["4principle"]])
    cand_themes.append(themes)

    # Bobby Jindal

    # rare candidate - one instance of last name should be enough
    comm_cand_sub.append(["jindal"])
    comm_cand_whole.append([])
    themes = []
    cand_themes.append(themes)

    # Mike Huckabee

    # rare candidate - one instance of last name should be enough
    comm_cand_sub.append(["huckabee"])
    comm_cand_whole.append([])
    themes = []
    themes.append([1, ["pursuingamericasgreatness"]])
    cand_themes.append(themes)

    # Rand Paul

    comm_cand_sub.append(["randpaul", "senator", "standwithrand", "randpac", "stand with rand"])
    comm_cand_whole.append(["rand", "sen"])
    themes.append([1, ["standwithrand", "randpac"]])
    cand_themes.append(themes)

    # Rick Perry

    comm_cand_sub.append(["rickperry", "goveror", "rickpac", "rick pac"])
    comm_cand_whole.append(["rick", "gov"])
    themes = []
    themes.append([1, ["rickpac"]])
    cand_themes.append(themes)

    # Marco Rubio

    comm_cand_sub.append(["marcorubio", "senator", "reclaim", "reclaimamerica", "reclaim america"])
    comm_cand_whole.append(["marco", "sen"])
    themes = []
    themes.append([1, ["reclaimamerica", "reclaimamericapac"]])
    cand_themes.append(themes)

    # Rick Santorum

    # rare candidate - one instance of last name should be enough
    comm_cand_sub.append(["santorum"])
    comm_cand_whole.append([])
    themes = []
    themes.append([1, ["patriotvoices", "patriotvoicespac", "pvpac"]])
    themes.append([2, ["pv", "pac"]])
    cand_themes.append(themes)

    # Scott Walker

    comm_cand_sub.append(["scottwalker", "governor", "ouramericanrevival", "our american revival"])
    comm_cand_whole.append(["scott", "gov"])
    themes = []
    themes.append([1, ["ouramericanrevival"]])
    cand_themes.append(themes)
    
    i = 0

    for cand in comm_cand:
        if check_candidates(text, form_cand(comm_cand[i], keywords, comm_cand_sub[i], [], comm_cand_whole[i])) is True:
            candidates.append(cand_form[i])
        elif check_theme(text, cand_themes[i]) is True:
            candidates.append(cand_form[i])
        i += 1
    
    return candidates

# return_candidates_from_link
# input: URL
# output: returns a list of candidates detected in the text contained within the URL
    
def return_candidates_from_link(tweetText):
    url = re.search("(?P<url>https?://[^\s]+)", tweetText).group("url")
    cand = return_candidates_logic(BeautifulSoup(urllib2.urlopen(url)).get_text())
    return cand

# return_sentiment
# input: string containing the text of an English-language tweet (tweetText)
# output: sentiment score of tweet, per TextBlob (float of 1 to -1, with 1 being positive, 0 being neutral, and -1 being negative)

def return_sentiment(tweetText):
    return TextBlob(tweetText).sentiment.polarity

# return_sentiment_from_link
# input: tweet text
# output: returns sentiment score of URL content detected within tweet, per TextBlob
    
def return_sentiment_from_link(tweetText):
    url = re.search("(?P<url>https?://[^\s]+)", tweetText).group("url")
    return TextBlob(BeautifulSoup(urllib2.urlopen(url)).get_text()).sentiment.polarity

def convert_sentiment(f): # float in [-1, 1] -> [1-5]
    f = f + 1 # float in [0, 2]
    f = f * 2.5 # float in [0, 5]
    f = ceil(f)
    if f < 1:
        f = 1
    elif f > 5:
        f = 5
    return int(f)


# return_themes
# input: string containing the text of an English-language tweet (tweetText)
# output: returns a list of pre-defined themes associated with that tweet (empty list if none)

def return_themes(tweetText):
    text = clean_text(tweetText)
    themes = []
    
    # abortion
    
    theme = []
    theme.append([1, ["abortion", "antiabortion", "fetus", "prochoice", "prolife", "righttochoose", "righttolife"]])
    theme.append([2, ["right", "life", "choose"]])
    if check_theme(text, theme) is True:
        themes.append("abortion")
    
    # climate change
    
    theme = []
    theme.append([1, ["manmade", "capandtrade", "carbon", "emissions", "environment", "environmental", "greenhouse", "epa"]])
    theme.append([2, ["global", "warming"]])
    theme.append([2, ["climate", "change"]])
    if check_theme(text, theme) is True:
        themes.append("climate change")
    
    # economy
    
    theme = []
    theme.append([1, ["deficit", "irs", "tax", "taxes", "taxation", "fiscal", "economy", "economic", "spending", "budget", "forecast", "unemployment", "jobless", "inflation"]])
    theme.append([2, ["federal", "reserve"]])
    theme.append([2, ["social", "security"]])
    if check_theme(text, theme) is True:
        themes.append("economy")
    
    # healthcare
    
    theme = []
    theme.append([1, ["healthcare", "obamacare", "aca", "medicare", "medicaid"]])
    theme.append([2, ["health", "insurance"]])
    theme.append([3, ["affordable", "care", "act"]])
    if check_theme(text, theme) is True:
        themes.append("healthcare")
    
    # gay marriage
    
    theme = []
    theme.append([1, ["homosexual", "gay", "lesbian", "lgbt"]])
    theme.append([2, ["gay", "gays", "marry", "marriage"]])
    theme.append([2, ["religious", "freedom"]])
    if check_theme(text, theme) is True:
        themes.append("gay marriage")
    
    # gun control
    
    theme = []
    theme.append([1, ["nra", "gun", "guns", "rifle", "rifles", "pistol", "pistols", "handgun", "handguns"]])
    theme.append([2, ["second", "2nd", "amendment"]])
    theme.append([2, ["assault", "weapon", "weapons"]])
    theme.append([3, ["right", "bear", "arms"]])
    if check_theme(text, theme) is True:
        themes.append("gun control")
    
    # international policy
    
    theme = []
    theme.append([1, ["israel", "iran", "iraq", "isis", "alqaeda", "netanyahu", "aipac"]])
    theme.append([2, ["middle", "east"]])
    if check_theme(text, theme) is True:
        themes.append("international policy")
        
    # immigration
    
    theme = []
    theme.append([1, ["immigration", "amnesty", "illegals", "border", "deport", "migrant", "immigrant", "deportation", "immigrants", "borders"]])
    theme.append([2, ["dream", "act"]])
    theme.append([2, ["illegal", "immigrant", "immigration", "illegals", "immigrants"]])
    if check_theme(text, theme) is True:
        themes.append("immigration")

    if len(themes) == 0:
        themes.append("None")
    
    return themes


# return_themes_from_link
# input: tweet text
# output: returns a list of themes detected in URLs detected within the tweet
    
def return_candidates_from_link(tweetText):
    url = re.search("(?P<url>https?://[^\s]+)", tweetText).group("url")
    return return_themes(BeautifulSoup(urllib2.urlopen(url)).get_text())


# return_candidates
# input: string containing the text of an English-language tweet (tweetText)
# output: returns a list of candidates detected in the tweet or the first URL in the tweet

def return_candidates(tweetText):
    cand = []
    cand = return_candidates_logic(tweetText)
    if cand == []:
        try:
            url = re.search("(?P<url>https?://[^\s]+)", tweetText).group("url")
            cand = return_candidates_from_link(url)
        except:
            pass
    return cand


def main():
    print return_candidates("Rubio's fish tacos")
    print return_candidates("Marco Rubio's fish tacos")
    print return_candidates("our american revival lol")
    print return_candidates("patriot values")
    print return_candidates("jindal huckabee santorum")
    print return_themes("homosexual netanyahu gun")
    print return_candidates("rt @JebBush blah blah blah")
    print return_candidates("right to rise bush")
    print return_candidates("hi my name is what http://fakeurl.com")
    print return_candidates("hi my name is what http://bit.ly/1aVF8mT")
    # with the master one/url checker
    #print return_candidates_master("i love jindal")
    #print return_candidates_master("i love gin")
    #print return_candidates_master("i love gin http://www.fakeurl.com")
    #print return_candidates_master("i love gin http://bit.ly/1aVF8mT")

if __name__ == '__main__':
    main()