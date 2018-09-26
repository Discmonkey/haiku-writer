import tensorflow as tf
import word_functions as w

MAX_WORD_LENGTH = 10

target_list = [char for char in 'abcdefghijklmnopqrstuvwxyz,']
d = w.get_unparsed()

parsed = w.filter_1_to_7(w.convert_to_words_and_syallables(d))

print(w.find_longest(parsed))
print(target_list)


def get_word_layer(seed, previous_word, previous_sentence_last_word, syllables_node):
    with tf.variable_scope("zack", reuse=tf.AUTO_REUSE):
        really_input = tf.concat([seed, previous_word, previous_sentence_last_word, syllables_node], axis=0)

        return tf.layers.dense(really_input, MAX_WORD_LENGTH, activation=tf.nn.relu)

def get_line_layer(seed, previous_word, previous_sentence_last_word, max_number_of_words):
    previous_word_node = tf.zeros([MAX_WORD_LENGTH])



def get_model():
    pass
