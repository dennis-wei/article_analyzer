from flask import Flask, render_template, redirect, url_for

from models.models import db
from forms import SearchForm

app = Flask(__name__)
app.config.from_pyfile('settings.py')

with app.app_context():
    from scrapers.scrape import insert_single_article
    from neighbors.neighbors import get_neighbors
    from services.database import test_url_rep, get_matrix_size

db.init_app(app)

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
        print get_matrix_size(), app.config['MIN_MATRIX_SIZE']
        neighbors = 'INSUFFICIENT_SIZE'
    else:
        neighbors = get_neighbors(url_rep) if url_rep else None
    return render_template('results.html', neighbors=neighbors)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

application = app
