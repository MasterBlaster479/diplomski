from flask_restful import reqparse, abort, Resource, fields, marshal_with, request, marshal
from flask import jsonify
from flask_classy import FlaskView
from models.Stock import Stock
import json
from pony.orm.serialization import to_json, to_dict

parser = reqparse.RequestParser()
parser.add_argument('stock')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'code': fields.String,
    'active': fields.Boolean,
}

class StockView(Resource):
    route_base = '/stocks/<int:id>'
    def get(self, id):
        return to_dict(Stock[id]).get('Stock').values()[0]

    @marshal_with(resource_fields)
    def put(self, id):
        # data = parser.parse_args()
        data = json.loads(request.data)
        stock = Stock.get(id=id)
        stock.set(**data)
        return Stock[id], 201

    def delete(self, id):
        stock = Stock.get(id=id)
        if stock:
            stock.delete()
            return '', 204
        abort(404)


class StockViewList(Resource):
    route_base = '/stocks'

    def get(self):
        stocks = to_dict(Stock.select().limit(80))
        send_stocks = stocks.get('Stock').values()
        return send_stocks

    @marshal_with(resource_fields)
    def post(self):
        data = request.data
        stock_data = json.loads(data)
        if isinstance(stock_data, (unicode, str,)):
            stock_data = eval(stock_data)
        new_stock = Stock(**stock_data)
        return new_stock, 201




