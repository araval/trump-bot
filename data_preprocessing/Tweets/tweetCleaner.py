from clean_single_tweet import *
import re
import requests

with open('tweetsONLY.txt') as f:
    orig_tweets = f.readlines()

# I recorded error for checking purposes, I don't write them 
# out anywhere. 
error = []
for tweet in orig_tweets:
    try:
        clean_up_tweet(tweet)
    except UnicodeDecodeError :
        error.append(tweet)

# At the end of this loop above there are two files on disk:
# cleaned_tweets.txt and incomplete_tweets.txt


# Open incomplete_tweets and complete the tweets by scraping
# twitlonger.com: 
with open('incomplete_tweets.txt') as f:
    incomp_tweets = f.readlines()

complete_tweets = []
for i, tweet in enumerate(incomp_tweets):
    soup = BeautifulSoup(tweet)
    s = soup.get_text()
    link_index = s.index('http')
    url = s[link_index:-1].encode('ascii','ignore')
    
    r = requests.get(url)
    if r.status_code != 404 :
        tmp = BeautifulSoup(r.text, 'html.parser')
        tweet = tmp.find("p", {"id": "posttext"}).text + '\n'
        complete_tweets.append( tweet )

# Write complete tweets to file (just for record).
with open('complete_tweets.txt', 'w') as f:
    for item in complete_tweets:
        f.write(item.encode('ascii', 'ignore'))

# Now clean the completed tweets:
for tweet in complete_tweets:
    try:
        clean_up_tweet(tweet)
    except UnicodeDecodeError :
        error.append(tweet)

