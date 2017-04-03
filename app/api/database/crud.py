"""
Script to create a database
"""
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

from app.api.database import simple_model

def init_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    simple_model.db.init_app(app)

def create_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    init_db(app)
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    simple_model.db.init_app(app)
    with app.app_context():
        simple_model.db.create_all()
    print("All tables created")

def read_db(sid):
    return simple_model.Simple.query.get(sid)

def add_random_ingredient():
    from random import randint
    sid = randint(0, 10)
    sname = "Ing::{}".format(sid)
    s = simple_model.Simple(id=sid, name=sname)
    simple_model.db.session.add(s)
    simple_model.db.session.commit()
    print("Data created... {}".format(repr(s)))
    result_s = simple_model.Simple.query.get(sid)
    print("Data returned from query... {}".format(repr(result_s)))
    count_query = simple_model.Simple.query.count()
    print("Table size: {}".format(str(count_query)))
