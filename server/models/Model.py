from pony.orm import *
db = Database('postgres', user='goran', password='goran', host='localhost', database='diplomski')

class User(db.Entity):
    first_name = Required(str)
    last_name = Required(str)
    email = Optional(str)
    login = Required(str, unique=True)
    password = Required(str)
    active = Optional(bool, sql_default=False)

class StockCategory(db.Entity):
    _table_ = "stock_category"
    name = Required(str)
    code = Required(str)
    active = Optional(bool, sql_default=False)
    stocks = Set("Stock", reverse="category")

class Stock(db.Entity):
    name = Required(str)
    code = Required(str)
    active = Optional(bool, sql_default=False)
    category = Optional(StockCategory)

db.generate_mapping(create_tables=True, check_tables=True)