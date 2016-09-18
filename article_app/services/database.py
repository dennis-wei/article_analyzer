from models.models import Meta, db

def test_url_rep(url):
    res = Meta.query.filter_by(raw_url=url).first()
    return res.flask_url if res else None

def get_matrix_size():
    return db.session.query(Meta).count()

def get_raw_url(url_rep):
    res = Meta.query.filter_by(flask_url=url_rep).first()
    return res.raw_url
