from flask import Flask
from word_functions import *

app = Flask(__name__)

unparsed = get_unparsed()
common = pull_most_common_words()
parsed = convert_to_words_and_syllables(unparsed)
one_to_seven = filter_1_to_7(parsed)
super_parsed = filter_to_words(one_to_seven, common)


@app.route('/')
def hello_world():
    return make_haiku(super_parsed)


if __name__ == '__main__':
    app.run("0.0.0.0", port=4500)