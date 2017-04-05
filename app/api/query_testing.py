# pylint: disable=missing-docstring
from app.api.main import API_SERVICE
from app.api.models import *

ctx = API_SERVICE.app_context()
ctx.push()

tag_list = ["tag_name='{}'".format(t) for t in ["Vegan", "Dairy-free"]]
tag_where_clause = ' OR '.join(tag_list)
print (tag_where_clause)
order_param="name"
asc = True

page = 10
page_size = 5
start = page_size * page

x = ("SELECT ingredient_id, name, image_url FROM (SELECT ingredient_id, name, image_url, COUNT(ingredient_id) AS cnt "
     "FROM (SELECT i.ingredient_id, i.name, i.image_url, t.tag_name FROM ingredient i JOIN "
           "tag_ingredient t ON i.ingredient_id = t.ingredient_id WHERE {tag_where_clause} )"
           "AS fst "
     "GROUP BY ingredient_id, name, image_url) AS "
     "scnd WHERE cnt = {tag_count} "
     "ORDER BY {order_param} {asc} "
     "LIMIT {size} OFFSET {start};")\
     .format(tag_where_clause=tag_where_clause,
             tag_count = len(tag_list),
             order_param=order_param,
             asc="ASC" if asc else "DESC",
             start=start,
             size=page_size)

y = db.engine.execute(x)
y2 = db.engine.execute(x)
for r in y:
    print(r)
