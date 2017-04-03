"""
Script to create a database
"""
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

from app.api.main import API_SERVICE
from app.api.database.simple_model import Simple

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def add_random_ingredient():
    from random import randint
    sid = randint(0, 10)
    sname = "Ing::{}".format(sid)
    s = Simple(id=sid, name=sname)
    db.session.add(s)
    db.session.commit()
    print("Data created... {}".format(repr(s)))
    result_s = Simple.query.get(sid)
    print("Data returned from query... {}".format(repr(result_s)))

if __name__ == "__main__":
    with API_SERVICE.app_context():
        init_db(API_SERVICE)
        add_random_ingredient()
