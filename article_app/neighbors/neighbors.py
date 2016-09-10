from sklearn.neighbors import KDTree
from flask import current_app

from unpack import unpack_db, unpack_url, unpack_results

def get_neighbors(url_rep):
    point_index = unpack_url(url_rep)
    arr = unpack_db()

    k = current_app.config['K_NEAREST']
    tree = KDTree(arr)
    raw_neighbors_indices = tree.query(arr[point_index], k=k+1)[1][0]
    list_indices = list(raw_neighbors_indices)
    list_indices.remove(point_index)
    return unpack_results(list_indices)
