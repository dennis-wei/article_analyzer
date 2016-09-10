import json
from settings import BASE_INDEX_FILE, RECENT_INDEX_FILE, BASE_VOCAB_SIZE

def get_base_index(vocab_size = current_app.config['BASE_VOCAB_SIZE']):
    brown_dist = nltk.FreqDist(w.lower() for w in brown.words())
    alpha_most_common = filter(lambda p: p[0].isalpha(), brown_dist.most_common(vocab_size+200))
    cut_most_common = alpha_most_common[:vocab_size]
    word_index = {p[0]: i for i, p in enumerate(cut_most_common)}
    return word_index

def store_base_index(vocab_size = current_app.config['BASE_VOCAB_SIZE']):
    word_index = get_base_index(vocab_size)
    with open(current_app.config['BASE_INDEX_FILE'], 'wb') as fp:
        json.dump(word_index, fp)

def restore_base_index():
    with open(BASE_INDEX_FILE, 'rb') as fp:
        base_index = json.load(fp)
        return base_index

def restore_recent_index():
    with open(RECENT_INDEX_FILE, 'rb') as fp:
        recent_index = json.load(fp)
        return recent_index
