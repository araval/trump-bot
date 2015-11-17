'''
This script contains functions and lists to aid cleaning tweets.
It is imported in clean_tweets.py
'''

import re

# Uninteresting words:
remove_list = ['tonight', 'yesterday', 'today', 'tomorrow','morning', 'thank you', 'thanks', \
               ' son', ' daughter', 'wife', 'birthday', 'you', 'condolences', \
               ' a.m.', ' am.', ' p.m.', ' pm.', 'watch','sen', \
               'realdonaldtrump', 'thx', ' dad', 'tuned' \
               'Trump :', 'watch my', 'via', 'congratulations',  \
               'interview', 'trump', 'congrats', 'i will be']

def deal_with_unicode(line):

    line = re.sub('\xe2\x80\x99', "'", line)
    line = re.sub('\xe2\x80\xa6', "...", line)
    line = re.sub("\xc2\xb4", "'", line)
    line = re.sub('\xe2\x80\x9d', '"', line)
    line = re.sub('\xe2\x80\x94', '-', line)
    line = re.sub("\xe2\x80\x9c", '"', line)
    line = re.sub("\xe2\x80\x93", '-', line)
    line = re.sub("\xe2\x80\x95", '-', line)
    line = re.sub("\xe2\x80\x98", "'", line)
    line = re.sub("\xc2\xa0", "", line) # not sure what this is, looks like white space
    line = re.sub("\xe2\x80\x8e", "", line)
    line = re.sub("\xe2\x80\x8f", "", line)
    line = re.sub("\xc2\xba", "symbolDEGREES", line)
    line = re.sub("\xc2\xa3", 'symbolPOUNDS', line)
    line = re.sub("\xe2\x82\xac", 'symbolEURO', line)
    line = re.sub(' @ ', ' at ', line)

    return line

def make_substitutions(line):

    line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)

    # Using The following tokens based on md5sums of the token name
    usToken = ' 7516fd43adaa5e0b8a65a672c39845d2'
    saudiArabiaToken = 'b835b521c29f399c78124c4b59341691'

    line = re.sub(' US', usToken, line)
    line = re.sub(' U\.S\.', usToken, line)
    line = re.sub(' U\.S\.A\.', usToken, line)
    line = re.sub(' USA', usToken, line)

    line = re.sub('Saudi Arabia', saudiArabiaToken, line)
    line = re.sub('saudi arabia', saudiArabiaToken, line)
    line = re.sub('China', 'china', line)
    line = re.sub('Iran', 'iran', line)
    line = re.sub('Israel', 'israel', line)
    line = re.sub('Scotland', 'scotland', line)
    line = re.sub('India', 'india', line)
    line = re.sub('Japan', 'japan', line)

    line = re.sub('Mr\.', 'Mr', line)
    line = re.sub('Sr\.', 'Sr', line)
    line = re.sub('Ms\.', 'Ms', line)
    line = re.sub('Mrs\.', 'Mrs', line)
    line = re.sub('Jr\.', 'Jr', line)

    line = re.sub('.@', ' ', line)
    line = re.sub('@', ' ', line)
    line = re.sub(',', ' ,', line)
    line = re.sub("'s", " 's ", line)

    line = re.sub('&amp;', 'and', line)
    line = re.sub('#', '', line)
    line = re.sub('"', '', line)

    line = re.sub('\.', ' . ', line)
    line = re.sub('\?', ' ? ', line)
    line = re.sub('!', ' ! ', line)
    line = re.sub('\(', ' ( ', line)
    line = re.sub('\)', ' ) ', line)
    line = re.sub(':', ' : ', line)
    line = re.sub(';', ' ; ', line)
    line = line.encode("ascii", "ignore")

    line = re.sub(" 's", "'s ", line)

    return line
