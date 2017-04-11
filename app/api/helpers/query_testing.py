# pylint: disable=missing-docstring

from app.api.main import API_SERVICE
from app.api.models import db


def query(sql):
    return db.engine.execute(sql)


def queryfm(sql, count):
    res = query(sql)
    rows = res.fetchmany(count)
    res.close()
    return rows

def main():
    ctx = API_SERVICE.app_context()
    ctx.push()

    with open("/home/noelb/veggie.sql", "r") as _file:
        db.engine.execute(_file.read())

    ctx.pop()

if __name__ == "__main__":
    main()
