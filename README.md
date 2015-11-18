# Trump Bot

This is bot built on Donald Trump’s vocabulary, i.e. text from his tweets, speeches, essays and debates. 
It utters Trump-like sentences, given a particular word or phrase. When given a phrase, it randomly selects a 
word and utters a sentence. Click [here](http://whatwouldtrumpsay.elasticbeanstalk.com/) to play with the app.  


## Data Pre-processing

### Tweets

Using the Twitter API, one can get at most 3000 most recent tweets by
a particular user. greptweet.com has been storing tweets of users for 
a long time, and so using greptweet, I was able to get Trump's tweets 
all the way from 2012, which gave me a total of ~18000 tweets. 

I collected tweets from realdonaldtrump.txt to tweetsONLY.txt using awk.
    awk -F '|' '{print $3}' < realdonaldtrump.txt > tweetsONLY.txt

Tweet Cleaning:

1. I removed retweets by discarding ones starting with 'RT'. 

2. Usernames: I collected all the users tagged by Trump - these would be words that begin 
with one of '@' or '.@' or '"@' or '".@'. 

    I scraped Twitter for the users' real names, number of followers, and the 
    number of people they follow. I then made two lists: a "white list" of 'well-known' 
    users, and a 'throw-out-list' of 'not-so-well-known' users. The white list was 
    determined by the following criterion: 
    
        if (number of followers)/(number following) > 10
          add user to white_list 
        else 
          add user to throw_out_list
    
    
    There were present users whose accounts were either deleted or suspended, so 
    I got either a 404 error or an "IndexError" for those users. I added them to 
    errorList - and manually inspected the contents. I kept the users, whose names
    I could recognize (such as 'vpbiden' or 'georgeclooney').   
    
    I discarded tweets directed at users not in white list, as they were of 
    a personal nature and uninteresting to anyone else.  
    I replaced the white-listed usernames by the real names. 

3. Tweet completion: Twitter has a limit of 140 characters for tweets. Longer 
tweets end in "(cont) some.link.to.twitlonger". I scraped these tweets 
from twitlonger.com, and then went through step 2. 

4. From tweets that contained links to websites, I removed the link, and kept
the text around it (this is one case where Trump does a good job of describing
what's in the link). 

5. Finally, made substitutions for words that contain a period such as 
acronyms or titles, such as "U.S. or Jr.". Added spaces between words and 
punctuation. This step was required for making my model, which treats 
punctuation as another 'word', and also the sentence construction uses the 
period as a cue to stop moving forward along the Markov Chain.   
All scripts for this step are in the data_processing/Tweets

### Debates
I scraped Times.com and nytimes.com for the transcripts of the four republican 
debates. These were reasonably clean, and required only step 5 listed above. 
The script for this is in data_processing/

### Speeches and essays
I downloaded speeches from several different websites, and essays from Trump's 
official website. Both of these were processed using step 5 of the tweet-cleaning
process. 

## The Model
Using this collection of sentences, I built a Markov Model, which contains three 
continuous words as keys and a list of all possible words that follow as value. 
Given a word, I choose following words by randomly selecting one of the following 
values in the list, and then using that word and the words around it as key. I stop 
the chain when the function hits a period. For the initial part of the sentence, I 
construct another dictionary, with reversed sentences. Traversing this chain in the 
forward direction gives us the initial sentence in reverse. Reversing this reversed
sentence and combining with the forward piece gives the complete sentence. 

When the input word in not present in the dictionary, I use word2vec to find the 
closest word, and return a sentence. 

## Examples
![Donald plays Golf](https://github.com/araval/trump-bot/blob/master/images/golf.png)
![Obama](https://github.com/araval/trump-bot/blob/master/images/obama.png)

## Trump's Favorite Words
Excluding stopwords, these are Trump's most frequently used words:
![WordCloud](https://github.com/araval/trump-bot/blob/master/images/trump_favorite_words.png)

These are the most frequent words for an 'average US president'. These are the words in 
speech transcripts of all US presidents as obtained from http://millercenter.org/president/speeches:

![average US president](https://github.com/araval/trump-bot/blob/master/images/avg_president.png)
