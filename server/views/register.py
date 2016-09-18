# Register views
from UserResource import UserResource, UserResourceList, UserLogin, UserMethodResource
from StockResource import StockResource, StockResourceList, StockMethodResource
from StockCategoryResource import StockCategoryResource, StockCategoryResourceList
from StockTransactionResource import StockTransactionResource
from StockMarketResource import StockMarketResource
from flask_restful import Api

def register_resources(app, api_prefix):
    api = Api(app)
    # User Resource register
    api.add_resource(UserResource, api_prefix + UserResource.route_base)
    api.add_resource(UserResourceList, api_prefix + UserResourceList.route_base)
    api.add_resource(UserLogin, api_prefix + UserLogin.route_base)
    api.add_resource(UserMethodResource, api_prefix + UserMethodResource.route_base)
    # Stock Resource register
    api.add_resource(StockResource, api_prefix + StockResource.route_base)
    api.add_resource(StockResourceList, api_prefix + StockResourceList.route_base)
    api.add_resource(StockMethodResource, api_prefix + StockMethodResource.route_base)
    # StockCategory Resource register
    api.add_resource(StockCategoryResource, api_prefix + StockCategoryResource.route_base)
    api.add_resource(StockCategoryResourceList, api_prefix + StockCategoryResourceList.route_base)
    # StockTransaction Resource register
    api.add_resource(StockTransactionResource, api_prefix + StockTransactionResource.route_base)
    # StockMarket Resource register
    api.add_resource(StockMarketResource, api_prefix + StockMarketResource.route_base)
