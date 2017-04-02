# pylint: disable=missing-docstring

from functools import wraps
def allow_cors(flask_route_fn):
    @wraps(flask_route_fn)
    def add_cors(*args, **kwargs):
        """
        Appends CORS headers to a flask response
        return the updated response
        """
        resp = flask_route_fn(*args, **kwargs)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    return add_cors
