# Trump Bot

This is a bot built on Donald Trump’s vocabulary, i.e. text from his tweets, speeches, essays and debates. 
It utters Trump-like sentences, given a particular word or phrase. It enjoys   [tweeting](https://twitter.com/surrealTrumpBot). Mention it in your tweet and it will respond. It also has a lonely existence [here](http://whatwouldtrumpsay.elasticbeanstalk.com/).  


## Data Pre-processing

### Tweets

Using the Twitter API, one can get at most 3000 most recent tweets by
a particular user. greptweet.com has been storing tweets of users for 
a long time, and so using greptweet, I was able to get Trump's tweets 
all the way from 2012, which gave me a total of ~18000 tweets. 

I collected tweets from realdonaldtrump.txt to tweetsONLY.txt using awk.
```
    awk -F '|' '{print $3}' < realdonaldtrump.txt > tweetsONLY.txt
```
Tweet Cleaning:

1. I removed retweets by discarding ones starting with 'RT'. 

2. Usernames: I collected all the users tagged by Trump - these would be words that begin 
with one of '@' or '.@' or '"@' or '".@'. 

    I scraped Twitter for the users' real names, number of followers, and the 
    number of people they follow. I then made two lists: a "white list" of 'well-known' 
    users, and a 'throw-out-list' of 'not-so-well-known' users. The white list was 
    determined by the following criterion: 
    
    ```
    if (number of followers)/(number following) > 10
      add user to white_list 
    else 
      add user to throw_out_list
    ```
    
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
Using this Trump's corpus which consists of ~250,000 words (14,000 unique), I built a 
bi-gram Markov Model, where the probability of a word depends on the bigram preceding it. 

Here's an example of a sentence generated by the bot, with the seed "hair": 
<img src="https://github.com/araval/trump-bot/blob/master/images/hair.png" alt="hair response" width = "400px"> 
<img src="https://github.com/araval/trump-bot/blob/master/images/markovChain.png" alt="markov chain example" width = "600px"> 

I first look for a tuple which has "hair" at position '0'. Then I randomly select a 
word from the list in the value. The list contains words as they occur - i.e. "not" 
may appear in the list multiple times. So if the list contained 5 "not" and 10 "be", 
then P(not| (hair, may)) = 1/3. Therefore, random sampling from this list is actually 
sampling according to frequency in the corpus. 

For the initial part of the sentence, I constructed another dictionary, with reversed 
sentences. Traversing this chain in the forward direction gives us the initial sentence 
in reverse. Reversing this reversed sentence and combining with the forward piece gives 
the complete sentence. 

#### What about words not in the Vocbulary?
The model requires a *seed* to generate a sentence. If the input does not contain a word 
present in the vocabulary, then this model will not be able to generate a sentence. 
We can try to find words similar to the words in the input and see if they are present in 
the vocabulary. If they are, then we generate a sentence and we are done. We can get similar
words easily with the help of *Word Vectors*! 

I downloaded 400,000 50-dimensional pre-trained word vectors from ![Stanford's NLP project](http://nlp.stanford.edu/projects/glove/). I wrote a C++ program to find 10 
most similar words for all the 400,000 words. Here's an example of similar words from my program: 

<img src="https://github.com/araval/trump-bot/blob/master/images/words.png" alt="similar words" width = "500px">

If none of the similar words are in the vocabulary, then model utters a sentence from a set of canned responses, such as "Don't waste my time. You're fired!". 

## Examples
<img src="https://github.com/araval/trump-bot/blob/master/images/golf.png" alt="Donald plays golf" width = "700px">

<img src="https://github.com/araval/trump-bot/blob/master/images/obama.png" alt="Obama Apprentice" width = "700px">

## Trump's Favorite Words
Excluding stopwords, here are Trump's most frequently used words in his speeches and essays: 

![Donald Trump's favorite words](https://github.com/araval/trump-bot/blob/master/images/trump_favorite_words_speeches.png)


For comparision, here are the most frequent words for an 'average US president'. 

![average US president's most used words](https://github.com/araval/trump-bot/blob/master/images/avg_president.png)

These are the words in speech transcripts of all US presidents from Washington to Obama (from [here](http://millercenter.org/president/speeches)).
