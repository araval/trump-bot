'''
This script takes a tweet, cleans it and appends it to the file 
either 'cleaned_tweets.txt' or 'incomplete_tweets.txt' 
depending on whether the tweet was shorter than twitter's limit 
of 140 characters, or longer than the limit, in which case the 
tweet ends with "(cont) http://some-link-to-tweet". 
'''

import re
import cPickle as pickle
from bs4 import BeautifulSoup
from substitutions import *
import string

# This is a list of all the users tagged by Mr. Trump
with open('userScreenNames.pkl') as f:
    users = pickle.load(f)

# This is a dictionary of all the users whose number of 
# followers exceed the number they are following by a 
# factor of 10. (This marks them as 'important'
with open('white_list.pkl') as f:
    white_list = pickle.load(f)

# This is a list of users whose information could not 
# be obtained either because they deleted their account, 
# or their account was suspended.
with open('errorList.pkl') as f:
    error_list = pickle.load(f)

# I had two kinds of errors, I had prefixed 404 errors with 
# "404", removing that now. 
for i, user in enumerate(error_list):
    if user[:3] == '404':
        error_list[i] = user[3:]

def clean_up_tweet(tweet):

    # Do nothing if tweet is a retweet. 
    if tweet.startswith('RT'):
        return 

    # Clean up unicode
    tweet = deal_with_unicode(tweet)

    # The following lines remove tweets which are not interesting. 
    # For example ones that contain announcement about his interviews
    # or appearances or any other event, and congratulations/condolences
    # to other twitter users. 
    for word in remove_list:
        if word in tweet.lower():
            return 

    # This checks for long tweets and writes them to file. 
    if "(cont)" in tweet.split():
        with open('incomplete_tweets.txt', 'a') as f:
            f.write(tweet.encode('ascii', 'ignore'))
        return 

    if len(tweet.split()) > 0:

        #Takes care of users tagged at the end of the tweet.
        #While the last word of tweet starts with @, keep removing it.
	while tweet.split()[-1].startswith('@') and len(tweet.split()) > 1:
	    tweet = ' '.join(s for s in tweet.split()[:-1])

        #Consider a single tweet, if any word in the tweet is a username,
        #and if the username is not in the white_list, replace it by space.
        #If the username is in the white_list, replace it by the value i.e.
        #the real name of the person as scraped from twitter. 
        wordlist = tweet.split()
        for i, word in enumerate(wordlist):
            tmp_word = word.lower()

            if '@' in tmp_word:
                index = tmp_word.index('@')
                tmp_word = tmp_word[index:]

                while tmp_word[-1] in string.punctuation and len(tmp_word) > 1:
                    tmp_word = tmp_word[:-1]

                if tmp_word in users:
                    if tmp_word not in white_list:
                        wordlist[i] = ' '
                    else:
                        wordlist[i] = white_list[tmp_word]

                elif tmp_word in error_list:
                    wordlist[i] = ""

        #Combine the words back to tweet
        tweet = ' '.join(word for word in wordlist)

        # Make substitutions, that will allow making the dictionary for 
        # the Markov Chain.
        tweet = make_substitutions(tweet)
        tweet = tweet + "\n"

        with open('cleaned_tweets.txt', 'a') as f:
    	    f.write(tweet.encode('ascii', 'ignore'))

    return
