import datetime
import cookielib
import urllib2
import re
from nltk import word_tokenize

from scrapers.nyt import scrape_nyt
from vectorize.vectors import get_base_vector, get_recent_vector
from scrapers.wp import scrape_wp
from services.utils import get_url_rep
from models.models import Content, Meta, Vector, db

base_regex = '(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
base_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

source_dict = {
    'nyt': scrape_nyt,
    'wp': scrape_wp
}

source_meta = {
    'nyt': {
        'url': 'http://www.nytimes.com/pages/politics/index.html',
        'starts': [
            'http://www.nytimes.com/201'
        ],
        'opener': base_opener,
        'regex': base_regex + '(ref=politics)'
    }
    # 'wp': {
    #     'url': 'https://www.washingtonpost.com/politics/',
    #     'starts': [
    #         'https://www.washingtonpost.com/politics/',
    #         'https://www.washingtonpost.com/news/post-politics/wp/201',
    #         'https://www.washingtonpost.com/news/the-fix/wp/201'
    #     ],
    #     'opener': base_opener,
    #     'regex': base_regex
    # }
}

def insert_articles(source, urls):
    scrape_func = source_dict[source]

    meta_list, content_list, vector_list = _get_rows(urls, scrape_func)
    combined_list = meta_list + content_list + vector_list

    db.session.bulk_save_objects(combined_list)
    db.session.commit()

def scrape_daily(source, meta):
    pol_url = meta['url']
    opener = meta['opener']
    regex = meta['regex']
    urls = _get_urls(pol_url, meta['starts'], opener, regex)
    insert_articles(source, urls)

def _get_urls(pol_url, starts, opener, regex):
    raw_html = opener.open(pol_url).read()
    url_search = re.compile(regex)
    urls = url_search.findall(raw_html)
    urls = list(set(map(lambda u: "".join(u), urls)))
    urls = [url for url in urls if _is_valid(url, starts)]
    return urls

def _is_valid(url, starts):
    for start in starts:
        if url.startswith(start):
            return True
    return False

def _get_rows(urls, scrape_func):
    meta_rows = []
    content_rows = []
    vector_rows = []

    for url in urls:
        if _check_duplicate(url):
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

def _check_duplicate(url):
    url_exists = Meta.query.filter_by(raw_url=url).first()
    return url_exists or None

def start_daily_scrape():
    print "Running Daily Scrape!"
    for source, meta in source_meta.iteritems():
        scrape_daily(source, meta)
