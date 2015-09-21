from flask import Flask, request, render_template
app = Flask(__name__)
#from trump_markov import get_two_words_3, get_sentence_3
from chain_builder import get_sentence

# Form page to submit text
@app.route('/')

def index():
    return render_template("index.html")

'''
def submission_page():
    return
        <form action="/section_classifier" method='POST' >
            <input type="text" name="user_input" />
            <input type="submit" />
        </form>

'''


# predict page
@app.route('/api/v0/')
def get_statement():

    word = request.args['q']
    sentence = get_sentence(word, f_dict, r_dict, randomness = 1)
    page = sentence
    return page
    
if __name__ == '__main__':

    import cPickle as pickle
    with open('f_dict.pkl') as f:
        f_dict = pickle.load(f)

    with open('r_dict.pkl') as f:
        r_dict = pickle.load(f)

    app.run(host='0.0.0.0', port=8080, debug=True)
