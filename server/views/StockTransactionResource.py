from flask_restful import reqparse, Resource, fields, marshal_with, request, abort
from pony.orm.serialization import to_json, to_dict
import json
from pony.orm import *
from models.User import User
from models.StockTransaction import StockTransaction


class StockTransactionResource(Resource):
    route_base = '/stock_transactions'

    def post(self):
        data = request.data
        transaction_data = json.loads(data)
        if isinstance(transaction_data, (unicode, str,)):
            transaction_data = eval(transaction_data)
        new_stock = StockTransaction(**transaction_data)
        return new_stock, 201

    def get(self):
        pass