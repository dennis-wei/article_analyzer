import urllib2
import re
from bs4 import BeautifulSoup
import cookielib

def scrape_wp(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    raw_html = opener.open(url).read()
    soup = BeautifulSoup(raw_html, "lxml")
    test = soup.find_all("article")[0].find_all("p")
    return " ".join([para.get_text() for para in test])
