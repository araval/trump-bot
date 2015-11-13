'''
This scripts get users tagged with '@___", goes to the corresponding 
twitter account and scrapes their real name, number of followers and
number of following. If number of followers is greater than the number
following by a factor of 10, then I consider them important enough 
to be added to "white_list". The others I will ignore - that is remove
tweets which are replies to them. 
'''

from bs4 import BeautifulSoup
import requests
import re
import cPickle as pickle
import string

with open('tweetsONLY.txt') as f:
    orig_tweets = f.readlines()

tweets_without_RT = []
for line in orig_tweets:
    if not line.startswith('RT'):
        line = re.sub('\xe2\x80\x99', "'", line)
        line = re.sub('\xe2\x80\x9d', '"', line)
        line = re.sub('\xe2\x80\x94', '-', line)
        line = re.sub(' @ ', ' at ', line)
        tweets_without_RT.append(line)

userList = []
for tweet in tweets_without_RT: 
    for word in tweet.split():
        if word.startswith('@') or word.startswith('.@') \
           or word.startswith('"@') or word.startswith('".@'):
                if word[0] == '"' or word[0] == '.':
                    word = word[1:]  
                
                word = re.sub("'s", "", word)
                word = word.split("-")[0]
                word = word.split(",")[0]
                word = word.split("(")[0]
                word = word.split(".")[0]
                word = word.split(":")[0]
             
                if len(word) > 0:        
                    while word[-1] in string.punctuation:
                        word = word[:-1]

                if len(word) > 0:
                    userList.append(word.lower())


userSet = set(userList)
userList = list(userSet)

def convert_to_float(mystring):
    if mystring[-1] == 'M':
        num = float(mystring[:-1])*1000000
    elif mystring[-1] == 'K':
        num = float(mystring[:-1])*1000
    elif "," in mystring:
        num = ''.join(mystring.split(","))
        num = float(num)
    else:
        num = float(mystring)
    return num


userScreenNames = {}
white_list = {}
throw_out_list = {}
errorList = []
for i, user in enumerate(userList[5000:]):
    if(i%100 == 0):
        print i
    url = "https://twitter.com/" + user[1:]
    r = requests.get(url)
    if r.status_code != 404 :
        tmp = BeautifulSoup(r.text, 'html.parser')
        try:
            name = tmp.select('h1.ProfileHeaderCard-name')[0].a.text
            
            #Get the number of followers
            n_followers = ((tmp.select('li.ProfileNav-item--followers')[0].a).select('span.ProfileNav-value')[0]).text
            
            #Get the number following
            n_following = ((tmp.select('li.ProfileNav-item--following')[0].a).select('span.ProfileNav-value')[0]).text 
           
            n_followers = convert_to_float(n_followers)
            n_following = convert_to_float(n_following)
                        
            #if more followers than following, then add to white_list
            #I will throw out users who are not in the list for they are not interesting. 
            #But for now add to throw_out_list, to examine the contents. 
            
            if n_following == 0:
                n_following = 1.0
                
            if n_followers/n_following > 10:
                white_list[user] = name
            else:
                throw_out_list[user] = name
                
            userScreenNames[user] = name
                
        except IndexError:
            errorList.append(user)
    else:
        tmp = '404'+user
        errorList.append(tmp)

'''
Following is a list of users I added by hand, where Trump added them 
errorneously (i.e. spelling errors or name-clash), or when the account
was suspended (which would be users who were using celeb-names). 
'''

white_list['@georgeclooney'] = 'George Clooney'
white_list['@newyorktimes'] = 'New York Times'
white_list['@larry_kudrow'] = 'Larry Kudlow'
white_list['@dannydanon'] = 'Danny Dannon'
white_list['@georgewillf'] = "George F Will"
white_list['@stephenbaldwin'] = 'Stephen Baldwin'
white_list['@michaeljackson'] = 'Michael Jackson'
white_list['@theapprentice'] = 'The Apprentice'
white_list['@dalailama'] = 'Dalai Lama'
white_list['@paulryanvp'] = 'Paul Ryan'
white_list['@paulryan'] = 'Paul Ryan'
white_list['@mayorbloomberg'] = 'Michael Bloomberg'
white_list['@nygiants'] = 'New York Giants'
white_list['@hilaryclinton'] = 'Hillary Clinton'
white_list['@rushlimbaugh'] = 'Rush Limbaugh'
white_list['@limbaugh'] = 'Rush Limbaugh'
white_list['@axlrose'] = 'Axl Rose'
white_list['@billoreilly'] = 'Bill Oreilly'
white_list['@teddyschleifer'] = 'Teddy Schleifer'
white_list['@macys'] = "Macy's"
white_list["@macy's"] = "Macy's"
white_list['@macy'] = "Macy's"
white_list["@warrenbuffett"] = 'Warren Buffett'
white_list["@zacharyquinto"] = 'Zachary Quinto'
white_list["@dailybeast"] = 'The Daily Beast'
white_list["@derekjeter"] = 'Derek Jeter'
white_list["@mitt"] = 'Mitt Romney'
white_list["@timewarner"] = 'Time Warner'
white_list["@apple"] = 'Apple'


#output to files:
with open('white_list.pkl', 'wb') as f:
    pickle.dump(white_list, f)

with open('throw_out_list.pkl', 'wb') as f:
    pickle.dump(throw_out_list, f)

with open('userScreenNames.pkl', 'wb') as f:
    pickle.dump(userScreenNames, f)

with open('errorList.pkl', 'wb') as f:
    pickle.dump(errorList, f)
