import register
from pony.orm import *

class Stock(register.db.Entity):
    name = Required(str)
    code = Required(str)
    active = Optional(bool, default=True)
    category = Optional("StockCategory")
    history_lines = Set("StockHistory")
    transactions = Set("StockTransaction")