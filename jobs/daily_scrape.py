import datetime
import cookielib
import urllib2
import re
from nltk import word_tokenize
from psycopg2 import connect

from scrapers.nyt import scrape_nyt
from vectorize.vectors import get_base_vector, get_recent_vector
from scrapers.wp import scrape_wp
from settings import DATABASE_URI
from services.utils import get_url_rep

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

    conn = connect(DATABASE_URI)
    cur = conn.cursor()

    meta_query = """
        insert into metadata
        (raw_url, flask_url)
        values (%s, %s)
    """

    cur.executemany(meta_query, meta_list)

    content_query = """
        insert into content
        (date_scraped, content)
        values (%s, %s)
    """

    cur.executemany(content_query, content_list)

    vector_query = """
        insert into vectors
        (base_vector, recent_vector)
        values (%s, %s)
    """

    cur.executemany(vector_query, vector_list)

    conn.commit()

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

        meta_rows.append((url, url_rep))
        content_rows.append((date_posted, content))
        tokens = word_tokenize(content)
        alpha_tokens = [t.lower() for t in tokens if t.isalpha()]
        vector_rows.append((get_base_vector(alpha_tokens), get_recent_vector(alpha_tokens)))

    return (meta_rows, content_rows, vector_rows)

def _check_duplicate(url):
    conn = connect(DATABASE_URI)
    cur = conn.cursor()
    cur.execute("select * from metadata where raw_url=%(u)s", dict(u=url))
    return cur.fetchone()

for source, meta in source_meta.iteritems():
    scrape_daily(source, meta)
