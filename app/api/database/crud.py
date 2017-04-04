"""
Script to create a database
"""
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

from app.api import models

def init_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    print("initing...", end="")
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    models.db.init_app(app)
    print("done")

def create_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    init_db(app)
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    models.db.init_app(app)
    with app.app_context():
        models.db.create_all()
    print("All tables created")
