import register
from pony.orm import *

class Stock(register.db.Entity):
    name = Required(str)
    code = Required(str)
    active = Optional(bool, sql_default=False)