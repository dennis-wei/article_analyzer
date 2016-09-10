import pandas as pd
import numpy as np

from models.models import Vector, Meta
from flask import current_app

def unpack_db():
    rows = Vector.query.all()
    vectors = map(_concat_vectors, rows)
    return np.array(vectors)

def unpack_url(url_rep):
    id = Meta.query.filter_by(flask_url=url_rep).first().id
    return id

def unpack_results(indices):
    urls = []
    for idx in indices:
        url = Meta.query.filter_by(id=idx).first().raw_url
        urls.append(url)
    return urls

def _concat_vectors(v):
    skip_top = current_app.config['SKIP_TOP']
    return np.concatenate((v.base_vector[skip_top:], v.recent_vector))
