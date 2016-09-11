from flask_restful import reqparse, abort, Resource, fields, marshal_with, request
from flask_classy import FlaskView, route
from models.Stock import Stock
from models.StockHistory import StockHistory
from pony.orm import *
import json
from pony.orm.serialization import to_json, to_dict
import ystockquote
import datetime
import itertools
from copy import copy
from operator import itemgetter
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

month_replacer = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

class StockView(Resource):
    route_base = '/stocks/<int:id>'

    def get(self, id):
        # stock_dict = {'Stock':{}}
        # stock_dict.update(Stock=Stock[id].to_dict(with_collections=True))
        return convert_stocks(to_dict(Stock[id]))

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
        date_from = request.args.get('date_from', '1970-01-01')[:10]
        date_to = request.args.get('date_to', str(datetime.date.today()))[:10]
        if Stock.get(id=id):
            stock = Stock[id]
            history_dict = ystockquote.get_historical_prices(stock.code, date_from, date_to)
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

    def chart_history_lines(self, id):
        if Stock.get(id=id):
            return_dict = {'GroupedData':{}}
            month_sockets = [(m, 0.0) for m in month_replacer.values()]
            stock = Stock[id]
            query = select((hl.date.year, hl.date.month, avg(hl.close)) for s in Stock for hl in s.history_lines if
                   s.id == stock.id and hl.date.year == datetime.date.today().year)
            data = query.order_by(1, 2)[:]
            changed_data = []
            for d in data:
                changed_data.append({'label': month_replacer.get(d[1]), 'value': round(d[2], 2)})
            return_dict['GroupedData'] = changed_data
            return_dict['maxYaxis'] = max(changed_data, key=lambda x: x['value'])
            return return_dict
        abort(404)

