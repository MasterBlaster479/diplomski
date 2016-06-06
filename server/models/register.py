from pony.orm import *
db = Database('postgres', user='goran', password='goran', host='localhost', database='diplomski')

def register_models(app):
    # Make sure each thread gets a db session
    app.wsgi_app = db_session(app.wsgi_app)
    sql_debug(True)
    db.generate_mapping(create_tables=True, check_tables=True)