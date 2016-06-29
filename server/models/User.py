import register
from pony.orm import *

class User(register.db.Entity):
    first_name = Required(str)
    last_name = Required(str)
    email = Optional(str)
    login = Required(str, unique=True)
    password = Required(str)
    active = Optional(bool, sql_default=False)
    transactions = Set("StockTransaction", lazy=True)