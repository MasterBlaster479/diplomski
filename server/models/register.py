from pony.orm import *
db = Database()
db.bind('postgres', user='goran', password='goran', host='localhost', database='diplomski')
import User
import StockCategory
import Stock
import StockHistory
import StockTransaction

def register_models(app):
    # Make sure each thread gets a db session
    app.wsgi_app = db_session(app.wsgi_app)
    sql_debug(True)
    db.generate_mapping(create_tables=True, check_tables=True)