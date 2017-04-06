"""
Database models described with SQLAlchemy.
"""

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=bad-whitespace
# pylint: disable=too-many-arguments

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # type: SQLAlchemy


class Simple(db.Model):
    """
    Table of ingredients.
    """

    __tablename__ = "simple"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "<Simple %d %s>" % (self.id, self.name)
