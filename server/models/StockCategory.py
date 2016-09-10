import register
from pony.orm import *

class StockCategory(register.db.Entity):
    _table_ = "stock_category"

    name = Required(str)
    code = Required(str)
    active = Optional(bool, default=True)
    stocks = Set("Stock")