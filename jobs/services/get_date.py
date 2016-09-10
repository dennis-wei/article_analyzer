import re

def basic_search(url):
    date_string = re.search(r'(\d+/\d+/\d+)', url).group(0)
    return date_string.replace('/', '-')

def nyt_date(url):
    return basic_search(url)

def wp_date(url):
    return basic_search(url)
