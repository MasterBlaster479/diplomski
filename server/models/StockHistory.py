import register
from pony.orm import *
from datetime import datetime, date

class StockHistory(register.db.Entity):
    _table_ = "stock_history"

    stock = Required("Stock", index=True)
    date = Required(datetime)
    volume = Optional(int)
    high = Optional(float)
    low = Optional(float)
    open = Optional(float)
    close = Optional(float)
    composite_key(stock, date)
