from flask_restful import reqparse, Resource, fields, marshal_with, request, abort
from pony.orm.serialization import to_json, to_dict
import json
from pony.orm import *
from models.User import User
from models.StockTransaction import StockTransaction
from models.Stock import Stock
from datetime import datetime, date


class StockMarketView(Resource):
    route_base = '/stock_market/'

    def combine_sorting(self, query, request):
        mapper = {'sorting[currPrice]': 2, 'sorting[bought]': 3, 'sorting[sold]': 4}
        for key, value in request.items():
            if key.startswith('sorting'):
                if key == 'sorting[stockCode]':
                    if value == 'desc':
                        query = query.order_by(lambda stock, cp, b, s: desc(stock.code))
                    else:
                        query = query.order_by(lambda stock, cp, b, s: stock.code)
                else:
                    position = mapper.get(key)
                    if value == 'desc':
                        position *= -1
                    query = query.order_by(position)
        return query

    def combine_filter(self, query, request):
        for key, value in request.items():
            if key.startswith('filter'):
                if key == 'filter[stockCode]':
                    query = query.filter(lambda stock,cp,b,s: value in stock.code)
        return query

    def get(self):
        pagenum = int(request.args.get('page', 1))
        pagesize = int(request.args.get('count', 10))
        market_dict = {'StockMarket': {}}
        query = select(
            (s, avg(hl.close for hl in s.history_lines if hl.date == max(hl.date for hl in s.history_lines)),
             sum(t.qty for t in s.transactions if t.qty > 0 and t.date == date.today()),
             sum(abs(t.qty) for t in s.transactions if t.qty < 0 and t.date == date.today())) for s in Stock)
        query = self.combine_filter(query, request.args)
        query = self.combine_sorting(query, request.args)
        current_data = query.page(pagenum, pagesize)
        new_data = []
        for line in current_data:
            new_line = {'stock': line[0].to_dict(), 'current_price': line[1] or 0.0,
                        'bought': line[2], 'sold': line[3]}
            new_data.append(new_line)
        market_dict.update(StockMarket=new_data)
        return new_data