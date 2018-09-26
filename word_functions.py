from nltk.corpus import cmudict
import nltk
import random
from functools import reduce
import requests
import os
#
# nltk.download("cmudict")
import pickle


def get_unparsed():
    return cmudict.dict()


def nsyl(word):
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]


def convert_to_words_and_syllables(nltk_dict):
    counters = {}

    for word, weird_thing in nltk_dict.items():
        count = 0
        for item in weird_thing[0]:
            if item[-1].isdigit():
                count += 1

        if count not in counters:
            counters[count] = []

        counters[count].append(str(word.lower()))

    return counters


def cache_wrapper(cache_key):

    def actual_wrapper(fn):
        def wrap(*args, **kwargs):
            if os.path.isfile(cache_key):
                res = pickle.load(open(cache_key, 'rb'))
            else:
                res = fn(*args, **kwargs)
                pickle.dump(res, open(cache_key, 'wb'))

            return res

        return wrap

    return actual_wrapper

# uncomment to cache this stuff
#@cache_wrapper("/home/mgrinchenko/BiometricsHg/sandbox/mgrinchenko/haiku-writer/cache/words")
def pull_most_common_words():
    common_words = requests.get("https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt")

    common = common_words.content

    just_words = common.decode('utf-8').split('\n')

    return just_words


def filter_to_words(parsed_dict, common_word_list):
    common_word_set = set(common_word_list)

    new_dict = {}

    for key, words in parsed_dict.items():
        new_dict[key] = []

        for word in words:
            if word in common_word_set:
                new_dict[key].append(word)

    return new_dict


def filter_1_to_7(parsed_dict):
    keys = list(parsed_dict.keys())

    parsed_dict[1] += parsed_dict[0]

    for key in keys:
        if key not in range(1, 8):
            parsed_dict.pop(key)

    return parsed_dict


def get_combinations(max_number):
    current_number = max_number

    while current_number > 0:
        new_num = random.randint(1, current_number)
        current_number -= new_num

        yield new_num


def find_longest(haiku_dict):
    max_word_length = 0
    max_word = None
    for words in haiku_dict.values():

        for word in words:

            if len(word) > max_word_length:
                max_word_length = len(word)
                max_word = word

    return max_word_length, max_word


def get_word_count(haiku_dict):
    return reduce(lambda a, b: a + len(b), haiku_dict.values(), 0)


def get_unique_characters(haiku_dict):
    all_characters = set()
    for words in haiku_dict.values():
        for word in words:

           for char in word:
               all_characters.add(char)

    return all_characters


def get_random_word(haiku_dict, num_syl):
    return random.sample(haiku_dict[num_syl], 1)[0]


def make_haiku(haiku_dict):
    all_lines = []
    for total_syl in [5, 7, 5]:
        line = []
        for syl in get_combinations(total_syl):
            line.append(get_random_word(haiku_dict, syl))

        all_lines.append(' '.join(line))

    return '<br>'.join(all_lines)


if __name__ == '__main__':
    common = pull_most_common_words()
    parsed = convert_to_words_and_syllables(d)
    one_to_seven = filter_1_to_7(parsed)
    super_parsed = filter_to_words(one_to_seven, common)

    make_haiku(super_parsed)

