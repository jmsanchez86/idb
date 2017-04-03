"""
Script to create a database
"""
# pylint: disable=invalid-name

from app.api.main import API_SERVICE

from app.api.database import simple_model

def create_db(app):
    """
    Build an empty database for the given flask app
    """
    # init app
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    simple_model.db.init_app(app)
    with app.app_context():
        simple_model.db.create_all()
    print("All tables created")

if __name__ == "__main__":
    print("Creating new db...")
    create_db(API_SERVICE)
    print("Done!")
