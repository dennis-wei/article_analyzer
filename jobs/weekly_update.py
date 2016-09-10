from psycopg2 import connect
import json
import datetime
from nltk import word_tokenize
from collections import Counter

from settings import DATABASE_URI, RECENT_VOCAB_SIZE, BASE_INDEX_FILE, RECENT_INDEX_FILE
from vectorize.vectors import get_recent_vector

def restore_base_index():
    with open(BASE_INDEX_FILE, 'rb') as fp:
        base_index = json.load(fp)
        return base_index

def update_index_weekly(cur, vocab_size = RECENT_VOCAB_SIZE):
    base_words = restore_base_index()
    high = datetime.date.today()
    low = high - datetime.timedelta(days=7)
    query = """
        select id, content from content
        where date_scraped between %(l)s and %(h)s
    """
    cur.execute(query, dict(h=high, l=low))
    content_rows = cur.fetchall()
    rows = [c[1] for c in content_rows]
    if len(rows) == 0:
        word_index = {}
    else:
        all_content = " ".join(rows).decode('utf-8')
        tokens = word_tokenize(all_content)
        alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
        counts = Counter(alpha_tokens)
        most_common = counts.most_common(vocab_size + 100)
        print most_common[0]
        cut_most_common = [m for m in most_common if m[0] not in base_words][:vocab_size]
        word_index = {p[0]: i for i, p in enumerate(cut_most_common)}
    with open(RECENT_INDEX_FILE, 'wb') as fp:
        json.dump(word_index, fp)
    return content_rows

def update_vectors_weekly():
    conn = connect(DATABASE_URI)
    cur = conn.cursor()
    rows = update_index_weekly(cur)
    for row in rows:
        _update_vector(row, cur)
    conn.commit()

def _update_vector(row, cur):
    idx, content = row
    tokens = word_tokenize(content.decode('utf-8'))
    alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
    vector = get_recent_vector(alpha_tokens)
    query = """
        update vectors
        set recent_vector = %(v)s
        where id = %(i)s
    """
    cur.execute(query, dict(i=idx, v=vector))

update_vectors_weekly()
