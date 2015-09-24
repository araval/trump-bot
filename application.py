from flask import Flask, request, render_template
from chain_builder import get_sentence
import cPickle as pickle

application = Flask(__name__)
application.debug = True

with open('f_dict.pkl') as f:
    f_dict = pickle.load(f)

with open('r_dict.pkl') as f:
    r_dict = pickle.load(f)

# Main page
@application.route('/')
def index():
    return render_template("index.html")

# predict page
@application.route('/api/v0/')
def get_statement():

    word = request.args['q']
    sentence = get_sentence(word, f_dict, r_dict, randomness = 1)
    page = sentence
    return page
    

if __name__ == '__main__':
    application.run()
