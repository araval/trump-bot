import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import cPickle as pickle

import nltk

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def tweet_to_wordlist(raw_sentence):
    raw_sentence = BeautifulSoup(raw_sentence).get_text()
    letters_only = re.sub("[^a-zA-Z0-9]", " ", raw_sentence)
    words = letters_only.split()
    return words

def tweet_to_sentences(raw_tweet, tokenizer):
  
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    raw_tweet = BeautifulSoup(raw_tweet).get_text()    
    raw_sentences = tokenizer.tokenize(raw_tweet.strip())
    
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append( tweet_to_wordlist(raw_sentence) )
            
    return sentences

def make_dictionary_3wordkeys(sentences):
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
                        key_to_insert = (sentence[i-1], sentence[i], sentence[i+1])
                        
                    if i == N-2:
                        value_to_insert = ('.', '')
                    elif i == N-3:
                        value_to_insert = (sentence[i+2], '.')
                    else:
                        value_to_insert = (sentence[i+2], sentence[i+3])

                    if key_to_insert not in dictionary:
                        dictionary[key_to_insert] = [[value_to_insert, 1]]
                    else: 
                        list_of_values = [x[0] for x in dictionary[key_to_insert]]
                        if value_to_insert in list_of_values:
                            index = list_of_values.index(value_to_insert)
                            dictionary[key_to_insert][index][1] += 1
                        else: 
                            dictionary[key_to_insert].append([value_to_insert, 1])
                        
    return dictionary

def get_two_words_3(word, dictionary, rev_key = None, gen_keylist = True, randomness = 0):
    words = []
    
    if gen_keylist:
        key_list = []
        for key, value in dictionary.iteritems():
            if word.lower() == key[1].lower():
                key_list.append(key)

        key = key_list[np.random.randint(0, len(key_list))]
        reversed_key = (key[2], key[1], key[0])
    
    else:
        key = rev_key

    words.append(key[2])
    value = dictionary[key]
   
    tmp = [x[1] for x in value]
    index = np.argmax(tmp)

    if value[index][0][0] != '.':

        words.append(value[index][0][0])
        words.append(value[index][0][1])

        nextkey = (key[2], value[index][0][0], value[index][0][1])

        while (nextkey[1] <> ".") & (nextkey[0] <> "."):
            value = dictionary[nextkey]
            
            if randomness == 1:
                index = np.random.randint(0, len(value))
            else:
                tmp = [x[1] for x in value]
                index = np.argmax(tmp)

            words.append(value[index][0][0])
            words.append(value[index][0][1])
        
            nextkey = (nextkey[2], value[index][0][0], value[index][0][1])
            
    if gen_keylist:
        return words, reversed_key
    else:
        return words

def get_sentence_3(word, forward_dict, backward_dict, randomness = 0):
    
    following_words, rev_key = get_two_words_3(word, forward_dict, randomness = 0) 
    previous_words = get_two_words_3(word, backward_dict, rev_key = rev_key, gen_keylist=False, randomness = 0)

    final_following_words = ' '.join(word for word in following_words if word != '.' )
    final_previous_words = ' '.join(word for word in reversed(previous_words) if word != '.' )

    s = final_previous_words + ' ' + word + ' ' + final_following_words
    s = s.strip()
    s = re.sub("did not", "didn't", s)
    s = re.sub("do not", "don't", s)
    s = re.sub('is not', "isn't", s)
    s = re.sub('does not', "doesn't", s)
    s = re.sub('has not', "hasn't", s)
    s = re.sub('can not', "can't", s)
    s = re.sub('could not', "couldn't", s)
    s = re.sub('would not', "wouldn't", s)
    s = re.sub('UScont', "U.S.", s)
    s = re.sub("I am", "I'm", s)
            
   
    return s + '.'


if __name__ == '__main__': 

    # Loading data and cleaning. 

    train = pd.read_csv('asciiTrumpTweets.txt', delimiter='|', error_bad_lines=False, header = 0)
    train.columns = ['id', 'date', 'tweet']

    tweet_list = []
    for tweet in train['tweet']:
        if tweet[0] != '@' and not tweet.startswith('RT'):
            tweet = re.sub("didn't", 'did not', tweet)
            tweet = re.sub("didn't", 'did not', tweet)
            tweet = re.sub("isn't", 'is not', tweet)
            tweet = re.sub("doesn't", 'does not', tweet)
            tweet = re.sub("don't", 'do not', tweet)
            tweet = re.sub("hasn't", 'has not', tweet)
            tweet = re.sub("couldn't", 'could not', tweet)
            tweet = re.sub("wouldn't", 'would not', tweet)
            tweet = re.sub("can't", 'can not', tweet)
            tweet = re.sub("U.S.", 'UScont', tweet)
            tweet = re.sub("I'm", 'I am', tweet)
            
            tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)
            tweet = re.sub('#', '', tweet)
            tweet = re.sub('&amp;', 'and', tweet)

            tweet_list.append(tweet.strip())
            
    tweet_list = pd.Series(tweet_list)

    sentences = []
    for i, tweet in enumerate(tweet_list):
        sentences += tweet_to_sentences(tweet, tokenizer)


    donald_dict3 = make_dictionary_3wordkeys(sentences)

    reversed_sentences = []
    for sentence in sentences:
        sentence = [word for word in reversed(sentence)]
        reversed_sentences.append(sentence)
        
    rev_donald_dict3 = make_dictionary_3wordkeys(reversed_sentences)   

    with open('f_dict.pkl', 'wb') as f:
        pickle.dump(donald_dict3, f)

    with open('r_dict.pkl', 'wb') as f:
        pickle.dump(rev_donald_dict3, f)
     
    '''
    while True:
        print 'Ask Donald Trump about:'
        word = raw_input()
        print get_sentence_3(word, donald_dict3, rev_donald_dict3)  
        print '' 

    '''                 
