from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY, JSON
import datetime as dt

db = SQLAlchemy()

class Meta(db.Model):
    __tablename__ = 'metadata'

    id = db.Column(db.Integer, primary_key=True)
    raw_url = db.Column(String)
    flask_url = db.Column(String)

    def __init__(self, raw_url, flask_url):
        self.raw_url = raw_url
        self.flask_url = flask_url

    def __repr__(self):
        return '<id {}>'.format(self.id)

    pass

class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    date_scraped = db.Column(Date)
    content = db.Column(String)

    def __init__(self, date_scraped, content):
        self.date_scraped = date_scraped
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)

    pass

class Vector(db.Model):
    __tablename__ = 'vectors'

    id = db.Column(db.Integer, primary_key=True)
    base_vector = db.Column(ARRAY(Integer))
    recent_vector = db.Column(ARRAY(Integer))

    def __init__(self, base_vector, recent_vector):
        self.base_vector = base_vector
        self.recent_vector = recent_vector

    def __repr__(self):
        return '<id {}>'.format(self.id)

    pass

class IndexJSON(db.Model):
    __tablename__ = 'word_index_jsons'

    id = db.Column(db.Integer, primary_key = True)
    index_type = db.Column(String)
    date_fetched = db.Column(Date)
    index = db.Column(JSON)

    def __init__(self, index, index_type='recent'):
        self.index_type = index_type
        self.index = index
        self.date_fetched = dt.date.today()

    def __repr__(self):
        return '<date_fetched {}>'.format(self.date_fetched)

    pass
