from flask import Flask, render_template, redirect, url_for
import time
import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from models.models import db
from forms import SearchForm

app = Flask(__name__)
app.config.from_pyfile('settings.py')

with app.app_context():
    from scrapers.scrape import insert_single_article
    from neighbors.neighbors import get_neighbors
    from services.database import test_url_rep, get_matrix_size, get_raw_url
    from vectorize.index import store_base_index

db.init_app(app)
with app.app_context():
    db.create_all()
    from job_drivers.daily_scrape import start_daily_scrape
    from job_drivers.weekly_update import update_vectors_weekly

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        url = form.url.data
        url_rep = test_url_rep(url) or insert_single_article(url)
        return redirect(url_for('results', url_rep=url_rep))
    return render_template('index.html', form=form)

@app.route('/results')
@app.route('/results/<url_rep>')
def results(url_rep=None):
    if get_matrix_size() < app.config['MIN_MATRIX_SIZE']:
        neighbors = 'INSUFFICIENT_SIZE'
    else:
        neighbors = get_neighbors(url_rep) if url_rep else None
        raw_url = get_raw_url(url_rep) if url_rep else None
    return render_template('results.html', raw_url=raw_url, neighbors=neighbors)

with app.app_context():
    store_base_index()
    start_daily_scrape()
    update_vectors_weekly()

def schedule_daily():
    with app.app_context():
        start_daily_scrape()

def schedule_weekly():
    with app.app_context():
        update_vectors_weekly()

logging.basicConfig()
scheduler = BackgroundScheduler()
scheduler.start()

scheduler.add_job(
    func=schedule_daily,
    trigger=IntervalTrigger(days=1),
    id='daily_scrape',
    name='Scrape every day',
    replace_existing=True
)

scheduler.add_job(
    func=schedule_weekly,
    trigger=IntervalTrigger(weeks=1),
    id='weekly_update',
    name='Update vectors once a week',
    replace_existing=True
)
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5050)

application = app
