from textblob import TextBlob
import re

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


# return_candidates
# input: string containing the text of an English-language tweet (tweetText)
# output: returns a list with 3 elements: a list of candidates associated with the tweet (empty list if none), sentiment of the tweet, subjectivity of the sentiment
# sentiment analysis uses TextBlob sentiment analysis function, with 1 being the most positive and -1 being the most negative, and 0 as neutral
    
def return_candidates(tweetText):
    
    text = clean_text(tweetText)
    
    keywords = ["candidate", "republican", "gop", "president", "campaign", "primary", "elect", "politic", "vote", "democrat", "caucus", "2016"]
    
    candidates = []
    comm_cand = ["bush", "christie", "cruz", "jindal", "huckabee", "paul", "perry", "rubio", "santorum", "walker"]
    cand_type = [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
    comm_cand_sub = []
    comm_cand_whole = []
    cand_themes = []

    # Jeb Bush

    comm_cand_sub.append(["jebbush", "righttorise", "govbush", "goveror"])
    comm_cand_whole.append(["jeb", "gov", "florida", "fl"])
    themes = []
    themes.append([1, ["righttorise"]])
    cand_themes.append(themes)

    # Chris Christie

    comm_cand_sub.append(["chrischristie", "leadership", "govchristie", "governor"])
    comm_cand_whole.append(["chris", "gov", "governor", "jersey", "nj"])
    themes = []
    themes.append([1, ["leadershipmattersforamerica"]])
    themes.append([3, ["leadership", "matters", "america"]])
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
    themes.append([3, ["pursuing", "americas", "greatness"]])
    cand_themes.append(themes)

    # Rand Paul

    comm_cand_sub.append(["randpaul", "senator", "standwithrand", "randpac"])
    comm_cand_whole.append(["rand", "sen"])
    themes.append([1, ["standwithrand", "randpac"]])
    themes.append([3, ["stand", "with", "rand"]])
    cand_themes.append(themes)

    # Rick Perry

    comm_cand_sub.append(["rickperry", "goveror", "rickpac"])
    comm_cand_whole.append(["rick", "gov"])
    themes = []
    themes.append([1, ["rickpac"]])
    cand_themes.append(themes)

    # Marco Rubio

    comm_cand_sub.append(["marcorubio", "senator", "reclaim", "reclaimamerica"])
    comm_cand_whole.append(["marco", "sen"])
    themes = []
    themes.append([1, ["reclaimamerica", "reclaimamericapac"]])
    themes.append([2, ["reclaim", "america"]])
    cand_themes.append(themes)

    # Rick Santorum

    # rare candidate - one instance of last name should be enough
    comm_cand_sub.append(["santorum"])
    comm_cand_whole.append([])
    themes = []
    themes.append([1, ["patriotvoices", "patriotvoicespac", "pvpac"]])
    themes.append([2, ["patriot", "voices"]])
    themes.append([2, ["pv", "pac"]])
    cand_themes.append(themes)

    # Scott Walker

    comm_cand_sub.append(["scottwalker", "governor", "ouramericanrevival"])
    comm_cand_whole.append(["walker", "gov"])
    themes = []
    themes.append([1, ["ouramericanrevival"]])
    cand_themes.append(themes)
    
    i = 0

    for cand in comm_cand:
        if check_candidates(text, form_cand(comm_cand[i], keywords, comm_cand_sub[i], [], comm_cand_whole[i])) is True:
            candidates.append(cand)
        elif check_theme(text, cand_themes[i]) is True:
            candidates.append(cand)
        i += 1
    
    return candidates

# return_sentiment
# input: string containing the text of an English-language tweet (tweetText)
# output: sentiment score of tweet, per TextBlob (float of 1 to -1, with 1 being positive, 0 being neutral, and -1 being negative)

def return_sentiment(tweetText):
    return TextBlob(tweetText).sentiment.polarity

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

    if len(themes) == 0:
        themes.append("None")
    
    return themes

def main():
    print return_candidates("Rubio's fish tacos")
    print return_candidates("Marco Rubio's fish tacos")
    print return_candidates("our american revival lol")
    print return_candidates("patriot values")
    print return_candidates("jindal huckabee santorum")
    print return_themes("homosexual netanyahu gun")
    
if __name__ == '__main__':
    main()