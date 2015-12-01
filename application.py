from flask import Flask, request, render_template
from chain_builder import get_sentence
import cPickle as pickle
from itertools import count

application = Flask(__name__)
application.debug = True

with open('f_dict.pkl') as f:
    f_dict = pickle.load(f)

with open('r_dict.pkl') as f:
    r_dict = pickle.load(f)

# Ideally this should be implemented as a
# redis dB or something that persists, but
# a simpler workaround is to use itertools'
# thread-safe iterators and write a file 
# to disk every 1,000 views
with open('count.pkl') as f:
    counter = count(pickle.load(f))

# Main page
@application.route('/')
def index():
    return render_template("index.html")

# Counter
@application.route('/counter')
def visitCounter():
    numVisitors = counter.next()
    if numVisitors % 10 is 0 :
        with open('count.pkl', 'wb') as f:
            pickle.dump(numVisitors, f)
    return "{:,} views".format(numVisitors) #str(numVisitors)

# predict page
@application.route('/api/v0/')
def get_statement():

    word = request.args['q']
    sentence = get_sentence(word, f_dict, r_dict, randomness = 1)
    page = sentence
    return page
    
if __name__ == '__main__':
    application.run()
