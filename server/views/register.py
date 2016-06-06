# Register views
from UserView import UserView, UserViewList, UserLogin
from flask_restful import reqparse, abort, Api, Resource

def register_views(app, api_prefix):
    api = Api(app)
    api.add_resource(UserView, api_prefix + UserView.route_base)
    api.add_resource(UserViewList, api_prefix + UserViewList.route_base)
    # api.add_resource(UserLogin, api_prefix + UserViewList.route_base)
    UserLogin.register(app, route_prefix=api_prefix)