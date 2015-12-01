from bs4 import BeautifulSoup
import cPickle as pickle

#*********************************************************
#       Function to make dictionary 
#*********************************************************
def make_dictionary(sentences):
    # uses three words as key
    dictionary = {}
    for sentence in sentences:
        sentence.append('.')
        N = len(sentence)
        if N > 0:
            for i, w in enumerate(sentence):
                if i <= N-2:
                    if i == 0:
                        key_to_insert = ('.', sentence[i], sentence[i+1])
                    else:
                        key_to_insert=(sentence[i-1],sentence[i],sentence[i+1])

                    if i == N-2:
                        value_to_insert = ('.', '')
                    elif i == N-3:
                        value_to_insert = (sentence[i+2], '.')
                    else:
                        value_to_insert = (sentence[i+2], sentence[i+3])

                    if key_to_insert not in dictionary:
                        dictionary[key_to_insert] = [[value_to_insert, 1]]
                    else:
                        list_of_values=[x[0] for x in dictionary[key_to_insert]]
                        if value_to_insert in list_of_values:
                            index = list_of_values.index(value_to_insert)
                            dictionary[key_to_insert][index][1] += 1
                        else:
                            dictionary[key_to_insert].append([value_to_insert, 1])

    return dictionary


#*********************************************************
#       Load Cleaned Data  
#*********************************************************
with open('data/Speeches/cleanSpeech.txt') as f:
    speeches = f.readlines()
    
with open('data/Tweets/clean_tweets.txt') as f:
    tweets = f.readlines()
    
with open('data/debates.txt') as f:
    debates = f.readlines()

tokenizer = nltk.data.load('file:english.pickle')

#*********************************************************
#   The following two functions take individual sentences in 
#   a tweet and return a list of list of words.
#   [["What", "a", "nice", "day", "!"], [...], ... ,[...]]
#*********************************************************

def tweet_to_sentences(tweet):
    tmpList = []
    raw_tweet = BeautifulSoup(tweet).get_text()
    raw_sentences = tokenizer.tokenize(raw_tweet.strip())

    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            tmpList.append(raw_sentence)
    return tmpList

sentences = []
def get_sentences_from_list(listx):
    for line in listx:
        tmp = tweet_to_sentences(line)
        for sentence in tmp:
            sentences.append(sentence.encode('ascii', 'ignore').split())           

# Each of these calls fills up the list "sentences".
get_sentences_from_list(tweets)
get_sentences_from_list(speeches)
get_sentences_from_list(debates)

#*********************************************************
#       Make Dictionaries
#*********************************************************

# Take sentences and make dictionary for forward direction:
donald_dict = make_dictionary(sentences)

# Reverse sentences and make dictionary for backward direction:
reversed_sentences = []
for sentence in sentences:
    sentence = [word for word in reversed(sentence)]
    reversed_sentences.append(sentence)
    
rev_donald_dict = make_dictionary(reversed_sentences)

#*********************************************************
#       Pickle both dictionaries:
#*********************************************************
with open('f_dict.pkl', 'wb') as f:
    pickle.dump(donald_dict, f)

with open('r_dict.pkl', 'wb') as f:
    pickle.dump(rev_donald_dict, f)
