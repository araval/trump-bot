import re
import numpy as np
from bs4 import BeautifulSoup
import cPickle as pickle
import nltk

EMPTY_STRING = ''

with open("stopwords.pkl", "rb") as f:
    stopwords = pickle.load(f)

with open('neighbours.pkl') as f:
    nbs_dict = pickle.load(f)


def get_two_words(word, dictionary, rev_key = None, gen_keylist = True, randomness = 1):

    words = []

    # Generate a list of possible keys, and pick one of them at random    
    if gen_keylist:
        key_list = []
        for key, value in dictionary.iteritems():
            if word.lower() == key[1].lower():
                key_list.append(key)

        if len(key_list) == 0:
            if gen_keylist:
        	return None, None

        #picks a random key from all possible keys
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

# For sentence construction, if the input does not contain a word present 
# in the dictionary, use one of the random sentences below. 
key_not_found_list = []
key_not_found_list.append("Look, I make a lot of money. I don't have time to think about ")
key_not_found_list.append("What?! I don't care about ")
key_not_found_list.append("Believe me, if I wanted to talk about it, I would. But I don't have time to talk about ")
key_not_found_list.append("You're such a lightweight, asking me about ")
key_not_found_list.append("Waste your energy someplace else. I don't want to talk about ")

key_not_found_list2 = []
key_not_found_list2.append("You're fired!")
key_not_found_list2.append("You're fired !!!")
key_not_found_list2.append("Don't waste my time. You're fired!")
key_not_found_list2.append("I don't like you. You're ugly.")
key_not_found_list2.append("You're ugly. Stop wasting my time, I make a lot of money.")


# When I have an input phrase, I randomly pick a word. However, the
# following words have higher priority
priority_list = ['hair', 'wig', 'obama', 'hillary', 'jeb', 'bush', 'war', \
                 'china', 'mexico', 'iran', 'iraq', 'wall',\
                 'immigration', 'climate', 'ugly', 'tax', 'taxes', \
                 'obamacare', 'president', 'putin', 'palin',\
                 'golf', 'israel', 'job', 'jobs', 'russia', 'germany',\
                 'india', 'canada', 'snowden', 'romney',\
                 'gun', 'guns', 'egypt', 'africa', 'oil', 'energy',\
                 'solar', 'wind', 'air', 'gas', 'peace', 'think']

def get_sentence(input_phrase, dictionary, rev_dictionary, randomness = 1):
 
    seed = EMPTY_STRING

    input_phrase = re.sub('\?', '', input_phrase)
    input_phrase = re.sub('\.', '', input_phrase)
    input_phrase = re.sub(',', '', input_phrase)
    input_phrase = re.sub('!', '', input_phrase)
    input_phrase = input_phrase.lower()

    word_list = input_phrase.split()
    # remove stopwords and if that results in a list with 
    # non-zero length, keep it. Else, keep the original list
    # with all the stopwords.
    if len(word_list) > 1:
        content = [w for w in word_list if w not in stopwords]
        if len(content) > 0:
            word_list = content

    #Need to check again, because word_list is not necessarily = content
    if len(word_list) > 0:
        found_key = False
        for tmp in word_list:
            if tmp.lower() in priority_list:
                seed = tmp
                found_key = True
                break
        if not found_key:
            possible_keys = []
            for tmp in word_list:
                for key, value in dictionary.iteritems():
                    if tmp.lower() == key[1].lower():
                        possible_keys.append(key)

            if len(possible_keys) > 0:
                seed = possible_keys[np.random.randint(0, len(possible_keys) )][1]
            else: 
                word_count = 0
                for tmp in word_list:
                    if tmp in nbs_dict:
                        word_count += 1
                        print tmp 

                        similar_word_list = nbs_dict[tmp] 
                        for similar_word in similar_word_list:
                            for key, value in dictionary.iteritems():
                                if similar_word.lower() == key[1].lower():
                                    possible_keys.append(key)

                if word_count == 0 :
                    return "You need to learn how to type. You're fired!"
                
                if len(possible_keys) > 0:
                    seed = possible_keys[np.random.randint(0,len(possible_keys) )][1]

    following_words, rev_key = get_two_words(seed, dictionary, randomness = 1) 

    if following_words == None:
        myrandnum = np.random.randint(0, 10)
        if myrandnum > 5 and seed != EMPTY_STRING:
            s = key_not_found_list[ np.random.randint(0, len(key_not_found_list) ) ] + seed + '!'
        else:
            s = key_not_found_list2[ np.random.randint(0, len(key_not_found_list2) ) ]
        return s

    previous_words = get_two_words(seed, rev_dictionary, rev_key = rev_key, gen_keylist=False, randomness=1)
    final_following_words = ' '.join(word for word in following_words if word != '.' )
    final_previous_words = ' '.join(word for word in reversed(previous_words) if word != '.' )

    s = final_previous_words + ' ' + seed + ' ' + final_following_words
   
    # Following steps make the sentence presentable:

    s = s.strip()
    s = re.sub('@', "", s)

    usToken = '7516fd43adaa5e0b8a65a672c39845d2'
    saudiArabiaToken = 'b835b521c29f399c78124c4b59341691'

    s = re.sub(usToken, 'US', s)
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
    if s[0] == "-":
        s = s[1:]

    s = s[0].upper() + s[1:]

    s = ' '.join(s.split()) 

    return s
