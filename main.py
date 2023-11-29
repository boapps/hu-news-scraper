import yaml
from fastapi import FastAPI
from models import Session, Article
from apscheduler.schedulers.background import BackgroundScheduler
from rss_parser import fetch_and_store_feeds

with open('scraping_rules.yaml', 'r') as file:
    scraping_rules = yaml.safe_load(file)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_feeds, 'interval', hours=1)
scheduler.start()

app = FastAPI()

@app.get("/articles/")
def read_all_articles():
    session = Session()
    articles = session.query(Article).all()
    return articles

@app.get("/articles/{feed}")
def read_articles(feed):
    session = Session()
    articles = session.query(Article).filter(Article.feed == feed).all()
    return articles

@app.get("/feeds/")
def read_rules():
    return [r for r in scraping_rules]

