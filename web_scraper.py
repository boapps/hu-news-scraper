from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import urllib.robotparser as urobot
import urllib.request

UA = 'hu-news-scraper'

def scrape_article_extra(url, rules):
    host = urlparse(url).hostname
    scheme = urlparse(url).scheme
    rp = urobot.RobotFileParser()
    rp.set_url(scheme + '://' + host + "/robots.txt")
    rp.read()
    if not rp.can_fetch(UA, url):
        raise Exception()
    extra_data = {}

    if not rules:
        return extra_data

    try:
        response = requests.get(url, headers={'user-agent': UA})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for rule in rules:
            for data_type in rule:
                extra_data[data_type] = soup.select_one(rule[data_type]).get_text(separator='\n', strip=True)
        return extra_data
    except requests.RequestException as e:
        print(f"Error fetching article: {e}")
        return extra_data

