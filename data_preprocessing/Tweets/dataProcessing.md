Using the Twitter API, one can get at most 3000 most recent tweets by
a particular user. greptweet.com has been storing tweets of users for 
a long time, and so using greptweet, I was able to get Trump's tweets 
all the way from 2012, which gave me a total of ~18000 tweets. 

Collected tweets from realdonaldtrump.txt to tweetsONLY.txt using awk.
    awk -F '|' '{print $3}' < realdonaldtrump.txt > tweetsONLY.txt

Cleaning:

1. I removed retweets by discarding ones starting with 'RT'. 

2. Usernames: 
I collected all the users tagged by Trump: these would be words that begin 
with '@' or '.@' or '"@' or '".@'. 

I scraped twitter for the user's real names, number of followers, and the 
number of people they follow.

Made two lists: a "white list" of 'well-known' users, and a 'throw-out-list' 
of 'not-so-well-known' users. The white list was determined by the following 
criterion: 

If (number of followers)/(number following) > 10
  add user to white_list 
else 
  add user to throw_out_list

There were present users whose accounts were either deleted or suspended, so 
I got either a 404 error or an "IndexError" for those users. I added them to 
errorList - and manually inspected the contents. I kept the users, whose names
I could recognize (such as 'vpbiden' or 'georgeclooney').   

I discarded tweets directed at users not in white list, as they were of 
a personal nature and uninteresting to everyone else.   
I also replaced the white listed usernames by the real names. 

3. Tweet completion:
Twitter has a limit of 140 characters for tweets. Longer tweets end 
in "(cont) http://link.to.twitlonger" 

I scraped these tweets from twitlonger.com, and then went through step 2. 

4. From tweets that contained links to websites, removed the link, and kept
the text around it (This is one case where Trump does a good job of describing
what's in the link. 

5. Finally, made substitutions for words that contain a period such as 
acronyms or titles, such as "U.S. or Jr.". Added spaces between words and 
punctuation. This step was required for making my model, which treats 
punctuation as another 'word', and also the sentence construction uses the 
period as a cue to stop moving forward along the Markov Chain.   



 
