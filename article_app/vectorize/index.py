from flask import current_app
import json
from nltk.corpus import brown
import datetime
import re
from collections import Counter

from models.models import Content, IndexJSON, db

def restore_base_index():
    base_index_query = IndexJSON.query.filter_by(index_type='base').first()
    return base_index_query.index

def restore_recent_index():
    recent_index_query = IndexJSON.query.filter_by(index_type='recent').order_by(IndexJSON.date_fetched.desc()).first()
    if recent_index_query:
        return recent_index_query.index
    else:
        return {}

def get_base_index(vocab_size = 1500):
    brown_dist = Counter(filter(lambda w: w.isalpha(), [w.lower() for w in brown.words()]))
    most_common = brown_dist.most_common(vocab_size)
    word_index = {p[0]: i for i, p in enumerate(most_common)}
    return word_index

def store_base_index(vocab_size = 1500):
    base_exists = IndexJSON.query.filter_by(index_type='base').first()
    if base_exists:
        return
    word_index = get_base_index(vocab_size)
    json_dump = json.dumps(word_index)
    base_index = IndexJSON(word_index, index_type='base')
    db.session.add(base_index)
    db.session.commit()
