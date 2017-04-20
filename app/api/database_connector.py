"""
Describe a simple interface for connecting to the database, abstracting away
any necessary setup and teardown code. This is intended for code that only
needs database access.
"""
# pylint: disable=missing-docstring

from app.api.main import API_SERVICE
from app.api.models import db


def database_connect(callback):
    """
    Setup up a database connection, pass the database object to the callback,
    then teardown the connection.
    """

    ctx = API_SERVICE.app_context()
    ctx.push()

    callback(db)

    ctx.pop()


def get_connection_context():
    ctx = API_SERVICE.app_context()
    ctx.push()
    return ctx
