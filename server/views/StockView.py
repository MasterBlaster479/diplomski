from flask_restful import reqparse, abort, Resource, fields, marshal_with, request
from flask_classy import FlaskView, route
from models.Stock import Stock
from models.StockHistory import StockHistory
from pony.orm import *
import json
from pony.orm.serialization import to_json, to_dict
import ystockquote
from useful import make_error


parser = reqparse.RequestParser()
parser.add_argument('stock')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'code': fields.String,
    'active': fields.Boolean,
}

def convert_stocks(stock_data):
    if stock_data.get('StockHistory'):
        for key, line in stock_data.get('StockHistory').items():
            if line.get('date'):
                line['date'] = str(line['date'])
    if stock_data.get('StockTransaction'):
        del stock_data['StockTransaction']
    return stock_data

class StockView(Resource):
    route_base = '/stocks/<int:id>'

    def get(self, id):
        # return to_dict(Stock[id]).get('Stock').values()[0]
        return (Stock[id].to_dict(related_objects=True))

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
        stock_select = Stock.select()
        stocks = to_dict(stock_select)
        # Cast date in string
        return convert_stocks(stocks)

    @marshal_with(resource_fields)
    def post(self):
        data = request.data
        stock_data = json.loads(data)
        if isinstance(stock_data, (unicode, str,)):
            stock_data = eval(stock_data)
        new_stock = Stock(**stock_data)
        return new_stock, 201

class StockMethodView(Resource):
    route_base = '/stocks/<int:id>/<string:method>'

    def get(self, id, method):
        # Dynamic call of methods in MethodView and rollback in case of exception
        try:
            return getattr(self, method)(id)
        except:
            rollback()
            abort(404)

    def populate_lines(self, id):
        if Stock.get(id=id):
            stock = Stock[id]
            history_dict = ystockquote.get_historical_prices(stock.code, '2016-01-01', '2016-05-01')
            for date, values in history_dict.items():
                new_vals = {
                    'date': date, 'volume': values['Volume'], 'high': values['High'],
                    'low': values['Low'], 'open': values['Open'], 'close': values['Close']
                }
                if not StockHistory.get(stock=stock, date=date):
                    stock.history_lines.create(**new_vals)
                else:
                    StockHistory.get(stock=stock, date=date).set(**new_vals)
            return convert_stocks(to_dict(Stock[id]))
        abort(404)



