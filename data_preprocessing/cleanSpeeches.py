from bs4 import BeautifulSoup
from substitutions import *
import os
import requests

'''
I have six files with speeches in my directory. 
This part just cleans up the speeches. 
'''

speeches = []
for filename in os.listdir(os.getcwd()):
    if filename[-3:] == 'txt':
        print 'reading', filename
        with open(filename) as f:
            speeches.append(f.readlines())
            
cleanSpeech = []
for speech in speeches:
    for line in speech:
        soup = BeautifulSoup(line)
        line = soup.getText()
        line = line.encode('ascii', 'ignore')
        line = line.strip()
        if len(line.split()) > 0:
            line = deal_with_unicode(line)
            line = make_substitutions(line)
            cleanSpeech.append(line)

# Write cleaned Speeches to file
with open('cleanSpeech.txt', 'w') as f:
    for sentence in cleanSpeech:
        sentence = sentence+'\n'
        f.write(sentence)
