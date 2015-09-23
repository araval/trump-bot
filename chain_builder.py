import pandas as pd
import re
import numpy as np
from bs4 import BeautifulSoup
import cPickle as pickle

import nltk

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def text_to_sentences(text):
    # text is a list of tweets etc 
    
    sen_list = []
    for line in text:
        if line[0] != '@' and not line.startswith('RT') and not line.startswith('Via') and not line.startswith('"') :

            line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)

            line = re.sub('U.S.', 'UScont', line)
            line = re.sub('U.S.A.', 'UScont', line)

            line = re.sub('Saudi Arabia', 'saudi', line)
            line = re.sub('saudi arabia', 'saudi', line)
            line = re.sub('China', 'china', line)
            line = re.sub('Iran', 'iran', line)
            line = re.sub('Israel', 'israel', line)
            line = re.sub('Scotland', 'scotland', line)

            line = re.sub('&amp;', 'and', line)
            line = re.sub('#', '', line)
            line = re.sub('.@', ' ', line)
            line = re.sub('@', ' ', line)
            line = re.sub('"', '', line)

            line = re.sub('\.', ' . ', line)
            line = re.sub('\?', ' ? ', line)
            line = re.sub('!', ' ! ', line)
            line = re.sub('\(', ' ( ', line)
            line = re.sub('\)', ' ) ', line)
            line = re.sub(':', ' : ', line)
            line = re.sub(';', ' ; ', line)
            line = line.encode("ascii", "ignore")

            line = re.sub('BarackObama', 'Barack Obama', line)
            line = re.sub('HillaryClinton', 'Hillary Clinton', line)
            line = re.sub('[Hh]illary [Cc]linton', 'Hillary Clinton', line)
            line = re.sub('MittRomney', 'Mitt Romney', line)
            line = re.sub('PaulRyan', 'Paul Ryan', line)
            line = re.sub('JebBush', 'Jeb Bush', line)
            line = re.sub('AlexSalmond', 'Alex Salmond', line)
 
            if " Donald Trump" or "Trump :" not in line:
                if '( cont )' not in line:
                    if 'Watch my' or 'watch my' not in line:
                        if ('My' or 'my') and 'interview' not in line:
                            if 'tonight' or 'Tonight' not in line: 
                                if 'via' or 'Via' not in line: 
                                    sen_list.append(line.strip())

    return sen_list


def tweet_to_wordlist(raw_sentence):
    raw_sentence = BeautifulSoup(raw_sentence).get_text()
    #letters_only = re.sub("[^a-zA-Z0-9]", " ", raw_sentence)
    words = raw_sentence.split()
    return words

def tweet_to_sentences(raw_tweet, tokenizer):

    #Splits into sentences instead of words:
   
    raw_tweet = BeautifulSoup(raw_tweet).get_text()    
    raw_sentences = tokenizer.tokenize(raw_tweet.strip())
    
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append( tweet_to_wordlist(raw_sentence) )
            
    return sentences


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

        if len(key_list) == 0:
        	if gen_keylist:
        		return None, None

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

        while nextkey[1] <> '.' and nextkey[0] <> '.':
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

key_not_found_list = []
key_not_found_list.append("I don't think about ")
key_not_found_list.append("What?! I don't care about ")
key_not_found_list.append("If I wanted to talk about it, I would. But I don't have time to think about ")
key_not_found_list.append("You're such a lightweight, asking me about ")

more_words = []
more_words.append("I ask for one word, and you input two?! You're fired!")
more_words.append("You aren't very bright, are you? Go back and enter one word.")
more_words.append("You're such a lightweight. Go back and enter one word, so I can speak my mind.")
more_words.append("Look, I'm very smart. I am asking you to input a word, don't try more than that.")
more_words.append("You're a lightweight. I refuse to tell you my thoughts unless you enter a single word.")


def get_sentence(word, dictionary, rev_dictionary, randomness = 0):
    
    if len(word.split()) > 1:
	s = more_words[ np.random.randint(0, len(more_words) ) ] 
	return s


    following_words, rev_key = get_two_words_3(word, dictionary, randomness = 1) 
    if following_words == None: 
    	s = key_not_found_list[ np.random.randint(0, len(key_not_found_list) ) ] + word + '!'
    	return s

    previous_words = get_two_words_3(word, rev_dictionary, rev_key = rev_key, gen_keylist=False, randomness=1)
    final_following_words = ' '.join(word for word in following_words if word != '.' )
    final_previous_words = ' '.join(word for word in reversed(previous_words) if word != '.' )

    s = final_previous_words + ' ' + word + ' ' + final_following_words
    
    s = s.strip()

    s = re.sub('@', "", s)
    s = re.sub('UScont', "U.S.", s)
    s = re.sub('saudi', 'Saudi Arabia', s)
    s = re.sub('china', 'China', s)
    s = re.sub('iran', 'Iran', s)
    s = re.sub('israel', 'Israel', s)
    s = re.sub('scotland', 'Scotland', s)

    s = re.sub('\( ', ' (', s)
    s = re.sub('  \)', ')', s)
    s = re.sub(' \)', ')', s)

    punc_set = ['?','!']
    if s[-1] not in punc_set:
        s = s + '.'
    else:
        if s[-1] == '?':
            s = re.sub(' \?', '\?', s)
        elif s[-1] == '!':
            s = re.sub(' !', '!', s)

    return s

'''
if __name__ == '__main__': 

    # Loading data and cleaning:


    # First set of tweets:
    train = pd.read_csv('asciiTrumpTweets.txt', delimiter='|', error_bad_lines=False, header = 0)
    train.columns = ['id','date', 'tweet']
    tweet_list = text_to_sentences(train['tweet'])
    tweet_list = pd.Series(tweet_list)

    sentences = []
    for i, tweet in enumerate(tweet_list):
	sentences += tweet_to_sentences(tweet, tokenizer)


    #Second set of tweets:
    with open('tweets_sep20') as f:
    	sep20_tweets = f.readlines()

    tmp = []
    for s in sep20_tweets:
	tmp.append( s.decode('utf-8', 'ignore'))

    more_tweets = text_to_sentences(tmp)

    for i, tweet in enumerate(more_tweets):
	sentences += tweet_to_sentences(tweet, tokenizer)


    # Complete tweets (obtained from scraping twitLonger)
    with open('complete_tweets.txt') as f:
 	complete_tweets = f.readlines()

    comp_tweets = text_to_sentences(complete_tweets)

    for i, tweet in enumerate(comp_tweets):
        if (i+1)%1000 == 0:
            print i+1
        sentences += tweet_to_sentences(tweet, tokenizer)  

	
    # Speeches and 'Positions' 


    with open('Speeches/alabama_speech.txt') as f:
        al_speech = f.readlines()
	    
    with open('Speeches/nashville_tennessee_Aug29.txt') as f:
        nashville_speech = f.readlines()
	    
    with open('Speeches/Texas_mexico_border_July23.txt') as f:
        texas_speech = f.readlines()

    with open('Speeches/new_york_sep_3.txt') as f:
        ny_speech = f.readlines()
	    
    with open('Speeches/phoenix_arizona_july_11.txt') as f:
        az_speech = f.readlines()
	    
    with open('Speeches/presidential_bid.txt') as f:
        presi_speech = f.readlines()
	    
    with open('Speeches/south_carolina_speech.txt') as f:
        sc_speech = f.readlines()

    with open('positions') as f:
        positions = f.readlines()
    

    lines = []
    for s in al_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in nashville_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in ny_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in az_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in presi_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in sc_speech:
        lines.append( s.decode('utf-8', 'ignore'))
	    
    for s in texas_speech:
        lines.append( s.decode('utf-8', 'ignore'))

    for s in positions:
        lines.append( s.decode('utf-8', 'ignore'))

    speech_text = text_to_sentences(lines)

    for i, tweet in enumerate(speech_text):
	sentences += tweet_to_sentences(tweet, tokenizer)


    #Make dictionaries:

    donald_dict = make_dictionary(sentences)

    reversed_sentences = []
    for sentence in sentences:
        sentence = [word for word in reversed(sentence)]
        reversed_sentences.append(sentence)
	    
    rev_donald_dict = make_dictionary(reversed_sentences)  


    with open('f_dict.pkl', 'wb') as f:
        pickle.dump(donald_dict, f)

    with open('r_dict.pkl', 'wb') as f:
        pickle.dump(rev_donald_dict, f)

'''
