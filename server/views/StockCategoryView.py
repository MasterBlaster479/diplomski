from flask_restful import reqparse, abort, Resource, fields, marshal_with, request, marshal
from flask import jsonify
from flask_classy import FlaskView
from models.StockCategory import StockCategory
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

class StockCategoryView(Resource):
    route_base = '/stock_categories/<int:id>'
    def get(self, id):
        return to_dict(StockCategory[id])

    def put(self, id):
        # data = parser.parse_args()
        data = json.loads(request.data)
        stock = StockCategory.get(id=id)
        stock.set(**data)
        return to_dict(StockCategory[id]), 201

    def delete(self, id):
        stock = StockCategory.get(id=id)
        if stock:
            stock.delete()
            return '', 204
        abort(404)


class StockCategoryViewList(Resource):
    route_base = '/stock_categories'

    def get(self):
        return to_dict(StockCategory.select(),)

    def post(self):
        data = request.data
        stock_data = json.loads(data)
        if isinstance(stock_data, (unicode, str,)):
            stock_data = eval(stock_data)
        new_stock = StockCategory(**stock_data)
        return to_dict(new_stock), 201




