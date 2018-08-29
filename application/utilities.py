from application import app, db
from sqlalchemy.sql import text

# fetch contents of page page_number
def page_query(query, params, limit, page_number):
    statement = text(query  + " LIMIT " + str(limit) + " OFFSET " + str(limit * (page_number - 1)) + ";")
    return db.engine.execute(statement, params)