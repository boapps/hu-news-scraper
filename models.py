from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///rss_feeds.db')
Session = sessionmaker(bind=engine)

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String, unique=True)
    published = Column(DateTime)
    feed = Column(String)
    content = Column(String)

    # Add a unique constraint
    UniqueConstraint('title', 'link', name='uix_title_link')


Base.metadata.create_all(engine)

