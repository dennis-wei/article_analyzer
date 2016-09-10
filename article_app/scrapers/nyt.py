import urllib2
import re
from bs4 import BeautifulSoup
import cookielib

def scrape_nyt(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    raw_html = opener.open(url).read()
    soup = BeautifulSoup(raw_html, "lxml")
    paragraphs = soup.find_all("p", class_="story-body-text story-content")
    return " ".join([para.get_text() for para in paragraphs])
