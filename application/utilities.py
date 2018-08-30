from application import app, db
from application.constants import MAXIMUM_LENGTH_OF_LISTED_TITLE
from sqlalchemy.sql import text
from decimal import Decimal, ROUND_DOWN
import os

# fetch contents of page page_number
def page_query(query, params, limit, page_number):
    statement = text(query  + " LIMIT " + str(limit) + " OFFSET " + str(limit * (page_number - 1)) + ";")
    return db.engine.execute(statement, params)


def shorten_if_longer_than(text, max = MAXIMUM_LENGTH_OF_LISTED_TITLE):
    if len(text) > max:
        return text[:max+1] + "..."
    return text

def format_average(avg):
    if avg is None:
        return ""
        
    #postgresql:ssä tyyppi on decimal 
    if  not os.environ.get("HEROKU"):
        avg = Decimal(avg)

    return avg.quantize(Decimal('.01'), rounding = ROUND_DOWN)
             