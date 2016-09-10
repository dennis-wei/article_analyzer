import cookielib
import urllib2
from nltk import word_tokenize

from scrapers.nyt import scrape_nyt
from scrapers.wp import scrape_wp
from services.utils import get_url_rep
from services.database import test_url_rep
from models.models import db, Meta, Content, Vector

source_dict = {
    'nyt': scrape_nyt,
    'wp': scrape_wp
}

def insert_articles(source, urls):
    scrape_func = source_dict[source]

    meta_list, content_list, vector_list = _get_rows(urls, scrape_func)
    full_list = meta_list + content_list + vector_list

    db.session.bulk_save_objects(full_list)
    db.session.commit()

def insert_single_article(url):
    url_rep = get_url_rep(url)
    source = url_rep.split('_')[0]
    insert_articles(source, [url])
    return url_rep

def _get_rows(urls, scrape_func):
    meta_rows = []
    content_rows = []
    vector_rows = []

    for url in urls:
        if test_url_rep(url):
            continue
        content = scrape_func(url)
        url_rep = get_url_rep(url)
        date_posted = url_rep.split('_')[-1]

        meta_rows.append(Meta(url, url_rep))
        content_rows.append(Content(date_posted, content))
        tokens = word_tokenize(content)
        alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
        vector_rows.append(Vector(get_base_vector(alpha_tokens), get_recent_vector(alpha_tokens)))

    return (meta_rows, content_rows, vector_rows)
