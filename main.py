from fastapi import FastAPI
from models import Session, Article
from apscheduler.schedulers.background import BackgroundScheduler
from rss_parser import fetch_and_store_feeds

fetch_and_store_feeds()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_feeds, 'interval', minutes=1)
scheduler.start()

app = FastAPI()

@app.get("/articles/")
def read_articles():
    session = Session()
    articles = session.query(Article).all()
    return articles

