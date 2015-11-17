import re
import numpy as np
from bs4 import BeautifulSoup
import cPickle as pickle
import nltk

tokenizer = nltk.data.load('file:english.pickle')
with open("stopwords.pkl", "rb") as f:
    stopwords = pickle.load(f)

def tweet_to_sentences(tweet):
    #takes a tweet and returns a list of "sentences" which 
    #are in turn a list of words. 

    tmpList = []
    raw_tweet = BeautifulSoup(tweet).get_text()
    raw_sentences = tokenizer.tokenize(raw_tweet.strip())

    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            tmpList.append(raw_sentence)
    return tmpList


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



def get_two_words_3(word, dictionary, rev_key = None, gen_keylist = True, \
                      randomness = 0):
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


# For sentence construction, if the input does not contain a word present i
# in the dictionary, use one of the random sentences below. 

key_not_found_list = []
key_not_found_list.append("I don't think about ")
key_not_found_list.append("What?! I don't care about ")
key_not_found_list.append("If I wanted to talk about it, I would. But I don't have time to think about ")
key_not_found_list.append("You're such a lightweight, asking me about ")

def get_sentence(word, dictionary, rev_dictionary, randomness = 0):
  
    word = re.sub('\?', '', word)
    word = re.sub('\.', '', word)
    word = re.sub(',', '', word)
    word = re.sub('!', '', word)

    word = word.lower()
    pp = word.split()

    content = [w for w in pp if w not in stopwords]
    if len(content) > 0:
        pp = content

    if len(pp) > 0:
        # When I have an input phrase, I randomly pick a word. However, the 
        # following words have higher priority:
        priority_list = ['hair', 'obama', 'hillary', 'jeb', 'bush', 'war', \
                         'china', 'mexico', 'iran', 'iraq', 'wall',\
                         'immigration', 'climate', 'ugly', 'tax', 'taxes', \
                         'obamacare', 'president', 'putin', 'palin',\
                         'golf', 'israel', 'job', 'jobs', 'russia', 'germany',\
                         'india', 'canada', 'snowden', 'romney',\
                         'think', 'gun', 'egypt', 'africa', 'oil', 'energy',\
                         'solar', 'wind', 'air', 'gas', 'peace']
        found_key = False
        for tmp in pp:
            if tmp.lower() in priority_list:
                word = tmp
                found_key = True
                break
        if not found_key:
            possible_key = []
            for tmp in pp:
                for key, value in dictionary.iteritems():
                    if tmp.lower() == key[1].lower():
                        possible_key.append(key)

            if len(possible_key) > 0:
                word = possible_key[np.random.randint(0,len(possible_key) )][1]


    following_words, rev_key = get_two_words_3(word, dictionary, randomness = 1) 
    if following_words == None: 
    	s = key_not_found_list[ np.random.randint(0, len(key_not_found_list) ) ] + word + '!'
    	return s

    previous_words = get_two_words_3(word, rev_dictionary, rev_key = rev_key, gen_keylist=False, randomness=1)
    final_following_words = ' '.join(word for word in following_words if word != '.' )
    final_previous_words = ' '.join(word for word in reversed(previous_words) if word != '.' )

    s = final_previous_words + ' ' + word + ' ' + final_following_words
   
    # Following steps make the sentence presentable:

    s = s.strip()
    s = re.sub('@', "", s)

    usToken = '7516fd43adaa5e0b8a65a672c39845d2'
    saudiArabiaToken = 'b835b521c29f399c78124c4b59341691'

    s = re.sub(usToken, 'U.S.', s)
    s = re.sub(saudiArabiaToken, 'Saudi Arabia', s)
    s = re.sub('china', 'China', s)
    s = re.sub('iran', 'Iran', s)
    s = re.sub('india', 'India', s)
    s = re.sub('israel', 'Israel', s)
    s = re.sub('scotland', 'Scotland', s)
    s = re.sub('japan', 'Japan', s)
    s = re.sub('russia', 'Russia', s)

    s = re.sub('\( ', ' (', s)
    s = re.sub('  \)', ')', s)
    s = re.sub(' \)', ')', s)
    s = re.sub(' ; ', '; ', s)
    s = re.sub(' : ', ': ', s)
    s = re.sub(' , ', ', ', s)


    punc_set = ['?','!']
    if s[-1] not in punc_set:
        s = s + '.'
    else:
        if s[-1] == '?':
            s = re.sub(' \?', '?', s)
        elif s[-1] == '!':
            s = re.sub(' !', '!', s)

    if s[0] == "," or s[0] == ':' or s[0] == ';':
        s = s[2:]

    s = s[0].upper() + s[1:]

    s = ' '.join(s.split()) 

    return s
