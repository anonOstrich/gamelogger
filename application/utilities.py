from application import app, db
from application.constants import MAXIMUM_LENGTH_OF_LISTED_TITLE
from sqlalchemy.sql import text
from decimal import Decimal, ROUND_DOWN
import os

# fetch contents of page page_number
def page_query(query, params, limit, page_number, order_column = "", order_direction = ""):
    order_part = ""
    if order_column: 
        order_part = " ORDER BY " + order_column + " " + order_direction + " "
    statement = text(query + order_part  + " LIMIT " + str(limit) + " OFFSET " \
    + str(limit * (page_number - 1)) + ";")
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

def parse_to_int(x):
    try: 
        return int(x)
    except: 
        return None
             