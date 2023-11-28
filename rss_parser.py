import feedparser
from urllib.parse import urlparse
from models import Session, Feed, Article
import datetime
from web_scraper import scrape_article_extra
import yaml
from time import sleep
from tqdm import tqdm

# Load scraping rules from YAML file
with open('scraping_rules.yaml', 'r') as file:
    scraping_rules = yaml.safe_load(file)

def fetch_and_store_feeds():
    for site in scraping_rules:
        print(site)
        session = Session()
        feed_url = scraping_rules[site]['feed']
        parsed_feed = feedparser.parse(feed_url)

        for entry in tqdm(parsed_feed.entries):
            # Convert struct_time to datetime object
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime.datetime(*entry.published_parsed[:6])
            else:
                # Handle cases where published date is not available
                published_date = datetime.datetime.now()

            existing_article = session.query(Article).filter_by(title=entry.title, link=entry.link).first()
            if not existing_article:
                extra_data = scrape_article_extra(entry.link, scraping_rules[site].get('extra'))
                article = Article(title=entry.title, link=entry.link, published=published_date, feed=urlparse(feed_url).hostname, **extra_data)
                session.add(article)
            sleep(1)

        session.commit()
        session.close()

