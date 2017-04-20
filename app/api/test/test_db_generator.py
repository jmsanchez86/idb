# pylint: disable=missing-docstring
# pylint: disable=invalid-name

from app.api.main import API_SERVICE
from app.api import models

app = API_SERVICE
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///api/test/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
db = models.db
db.init_app(app)
with app.app_context():
    db.create_all()
    check = 0
    with open('dump.sql', 'r') as dump_file:
        for line in dump_file.readlines():
            db.engine.execute(line)
            check += 1
            if check % 100 == 0:
                print(check)
