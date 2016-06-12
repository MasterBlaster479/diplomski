# Register views
from UserView import UserView, UserViewList, UserLogin
from StockView import StockView, StockViewList, StockMethodView
from StockCategoryView import StockCategoryView, StockCategoryViewList
from flask_restful import reqparse, abort, Api, Resource

def register_views(app, api_prefix):
    api = Api(app)
    api.add_resource(UserView, api_prefix + UserView.route_base)
    api.add_resource(UserViewList, api_prefix + UserViewList.route_base)
    api.add_resource(UserLogin, api_prefix + UserLogin.route_base)
    # api.add_resource(UserLogin, api_prefix + UserViewList.route_base)
    # UserLogin.register(app, route_prefix=api_prefix)
    # Stock Views register
    api.add_resource(StockView, api_prefix + StockView.route_base)
    api.add_resource(StockViewList, api_prefix + StockViewList.route_base)
    api.add_resource(StockMethodView, api_prefix + StockMethodView.route_base)
    # StockCategory Views register
    api.add_resource(StockCategoryView, api_prefix + StockCategoryView.route_base)
    api.add_resource(StockCategoryViewList, api_prefix + StockCategoryViewList.route_base)
