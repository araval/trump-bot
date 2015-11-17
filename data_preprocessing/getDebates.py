from bs4 import BeautifulSoup
from substitutions import *
import requests

#*********************************************************
#    Scrape for debates, clean them, and output to file
#*********************************************************
'''
The first three debates are all scraped from the same website, 
therefore this function helps the process:
'''

def get_debate(url):
    r = requests.get(url)
    tmp = BeautifulSoup(r.text, 'html.parser')

    debate = []
    check = []
    trump_flag = False

    for t in tmp.select('div p'):
        line = t.text
        soup = BeautifulSoup(line)
        line = soup.getText()
        line = line.encode('utf-8', 'ignore')
        line = deal_with_unicode(line)
         
        if line.startswith('TRUMP') :
            trump_flag = True
            line = ' '.join(line.split()[1:])
            line.strip()
            if not line.startswith("...") and len(line.split()) > 4 :
                debate.append(line)
        elif line.split()[0].isupper() and line.split()[0] <> "(APPLAUSE)":
            trump_flag = False
        elif trump_flag:
            line.strip()
            if len(line.split()) > 4:
                debate.append(line)
        else:
            check.append(line) 

    return debate


url1 = "http://time.com/3988276/republican-debate-primetime-transcript-full-text/"
url2 = "http://time.com/4037239/second-republican-debate-transcript-cnn/"
url3 = "http://time.com/4091301/republican-debate-transcript-cnbc-boulder/"

debate1 = get_debate(url1)
debate2 = get_debate(url2)
debate3 = get_debate(url3)

'''
The fourth debate is from a different website, so the scraping is a bit 
different
'''

url = "http://www.nytimes.com/2015/11/11/us/politics/ \
       transcript-republican-presidential-debate.html?_r=0"
r = requests.get(url)
tmp = BeautifulSoup(r.text, 'html.parser')

debate4 = []
check = []
trump_flag = False
for t in tmp.select('div p'):
    soup = BeautifulSoup(t.text)
    line = soup.getText()
    line = line.encode('utf-8', 'ignore')
    line = deal_with_unicode(line)

    if line <> 'Advertisement':
        if line.startswith('TRUMP') :
            trump_flag = True
            line = ' '.join(line.split()[1:])
            line.strip()
            if not line.startswith("...") and len(line.split()) > 3 :
                debate4.append(line)
        elif line.split()[0].isupper():
            trump_flag = False
        elif trump_flag:
            line.strip()
            debate4.append(str(trump_flag) + ' ' + line)
        else:
            check.append(line)

#********************************************
# Write debates to file:
#********************************************

with open('debates.txt', 'w') as f:
    for line in debate1:
        line = make_substitutions(line)
        line = line + '\n'
        f.write(line)
                
    for line in debate2:
        line = make_substitutions(line)
        line = line + '\n'
        f.write(line)
                
    for line in debate3:
        line = make_substitutions(line)
        line = line + '\n'
        f.write(line)

    for line in debate4:
        line = make_substitutions(line)
        line = line + '\n'
        f.write(line)

#********************************************
#  DONE
#********************************************
