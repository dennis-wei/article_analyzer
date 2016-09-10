import datetime as dt

from services.get_postfix import *
from services.get_date import *

source_prefixes = {
    'nytimes.com': 'nyt',
    'washingtonpost.com': 'wp'
}

postfix_func = {
    'nyt': nyt_post,
    'wp': wp_post
}

date_func = {
    'nyt': nyt_date,
    'wp': wp_date
}

def get_url_rep(url):
    for source in source_prefixes.keys():
        if source in url:
            prefix = source_prefixes[source]
            break
    return prefix + '_' + postfix_func[prefix](url) + '_' + date_func[prefix](url)
