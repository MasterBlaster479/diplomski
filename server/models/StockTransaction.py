import register
from pony.orm import *
from datetime import datetime, date

class StockTransaction(register.db.Entity):
    _table_ = "stock_transaction"

    stock = Required("Stock", index=True)
    user_id = Required("User", index=True)
    qty = Required(int)
    price = Required(float)
    date = Required(datetime, default=lambda : datetime.now())
    state = Required(str, default='draft')
