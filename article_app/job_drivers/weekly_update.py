import json
import datetime
from nltk import word_tokenize
from collections import Counter
import datetime as dt
from flask import current_app as app

from models.models import IndexJSON, db, Content, Vector
from vectorize.vectors import get_recent_vector
from vectorize.index import restore_base_index

def update_index_weekly(vocab_size = app.config['RECENT_VOCAB_SIZE']):
    index_exists = IndexJSON.query.filter_by(date_fetched=dt.date.today(), index_type='recent').first()
    if index_exists:
        return []
    base_words = restore_base_index()
    high = datetime.date.today()
    low = high - datetime.timedelta(days=7)
    query_rows = db.session.query(Content).filter(Content.date_scraped.between(low, high)).all()
    idx_rows = [(r.id, r.content) for r in query_rows]
    content_rows = [r[1] for r in idx_rows]
    if len(content_rows) == 0:
        word_index = {}
    else:
        all_content = " ".join(content_rows).encode('utf-8')
        tokens = word_tokenize(all_content)
        alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
        counts = Counter(alpha_tokens)
        most_common = counts.most_common(vocab_size + 100)
        cut_most_common = [m for m in most_common if m[0] not in base_words][:vocab_size]
        word_index = {p[0]: i for i, p in enumerate(cut_most_common)}
    new_index = IndexJSON(word_index, index_type='recent')
    db.session.add(new_index)
    db.session.commit()
    return idx_rows

def update_vectors_weekly():
    print "Running Weekly Update!"
    rows = update_index_weekly()
    for row in rows:
        _update_vector(row)
    db.session.commit()

def _update_vector(row):
    idx, content = row
    tokens = word_tokenize(content.encode('utf-8'))
    alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
    vector = get_recent_vector(alpha_tokens)
    vec = Vector.query.filter_by(id=idx).first()
    Vector.recent_vector = vector
