from flask import current_app
import json
from nltk.corpus import brown
import nltk
import datetime
import re
from collections import Counter

from models.models import Content

def restore_base_index():
    with open(current_app.config['BASE_INDEX_FILE'], 'rb') as fp:
        base_index = json.load(fp)
        return base_index

def restore_recent_index():
    with open(current_app.config['RECENT_INDEX_FILE'], 'rb') as fp:
        recent_index = json.load(fp)
        return recent_index
