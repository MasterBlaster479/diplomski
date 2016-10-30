from flask_restful import reqparse, Resource, fields, marshal_with, request, abort
from pony.orm.serialization import to_json, to_dict
import json
from pony.orm import *
from pony.orm.serialization import to_json, to_dict
from models.User import User
from models.StockTransaction import StockTransaction
from datetime import date

def convert_data(data):
    if data.get('StockTransaction'):
        for key, line in data.get('StockTransaction').items():
            if line.get('date'):
                line['date'] = str(line['date'])
    if data.get('User'):
        del data['User']
    return data

class StockTransactionResourceList(Resource):
    route_base = '/stock_transactions'

    def post(self):
        data = request.data
        transaction_data = json.loads(data)
        if isinstance(transaction_data, (unicode, str,)):
            transaction_data = eval(transaction_data)
        new_stock = StockTransaction(**transaction_data)
        return new_stock, 201

class StockTransactionMethodResource(Resource):
    route_base = '/stock_transactions//<string:method>'

    def get(self, method, *args, **kwargs):
        # Dynamic call of methods in MethodView and rollback in case of exception
        try:
            return getattr(self, method)(*args, **kwargs)
        except:
            rollback()
            abort(404)

    def user_transactions(self, *args, **kwargs):
        user_id = int(request.args.get('user_id'))
        if not User.get(id=user_id):
            abort(404)
        query = StockTransaction.select(lambda t: t.user_id.id == user_id
                                        and t.date == date.today())
        data = query[:]
        return convert_data(to_dict(data))
