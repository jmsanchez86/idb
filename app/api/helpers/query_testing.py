# pylint: disable=missing-docstring

import pprint
from app.api.main import API_SERVICE
from app.api.models import *


def query(sql):
    return db.engine.execute(sql)


def queryfm(sql, count):
    res = query(sql)
    rows = res.fetchmany(count)
    res.close()
    return rows


if __name__ == "__main__":
    ctx = API_SERVICE.app_context()
    ctx.push()

    with open("/home/noelb/veggie.sql", "r") as f:
        db.engine.execute(f.read())

    ctx.pop()
