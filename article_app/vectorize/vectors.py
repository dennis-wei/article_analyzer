import numpy as np
from flask import current_app
from nltk import word_tokenize

from vectorize.index import restore_base_index, restore_recent_index

def count_words(tokens, word_dict, vocab_size):
    vec = np.zeros(vocab_size)
    for t in tokens:
        if t in word_dict:
            vec[word_dict[t]] += 1
    return vec

def get_base_vector(tokens):
    vocab_size = current_app.config['BASE_VOCAB_SIZE']
    word_dict = restore_base_index()
    return count_words(tokens, word_dict, vocab_size)

def get_recent_vector(tokens):
    vocab_size = current_app.config['RECENT_VOCAB_SIZE']
    word_dict = restore_recent_index()
    return count_words(tokens, word_dict, vocab_size)
