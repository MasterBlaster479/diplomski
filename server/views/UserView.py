from flask_restful import reqparse, Resource, fields, marshal_with, request, abort
from pony.orm.serialization import to_json, to_dict
from pony.orm import *
from models.User import User
from models.StockTransaction import StockTransaction
from models.StockHistory import StockHistory
import json
parser = reqparse.RequestParser()
parser.add_argument('user', 'users', 'username', 'password')
from useful import make_error

resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'login': fields.String,
    'password': fields.String,
    'active': fields.Boolean,
}

class UserView(Resource):
    route_base = '/users/<int:id>'
    @marshal_with(resource_fields)
    def get(self, id):
        return User[id]

    @marshal_with(resource_fields)
    def put(self, id):
        # data = parser.parse_args()
        data = request.data
        data = json.loads(data.get('user'))
        user = User.get(id=id)
        user.set(**data)
        return User[id], 201

    def delete(self, id):
        user = User.get(id=id)
        if user:
            user.delete()
            return '', 204
        abort(404)

class UserViewList(Resource):
    route_base = '/users'

    @marshal_with(resource_fields)
    def get(self):
        return User.select()

    @marshal_with(resource_fields)
    def post(self):
        # data = parser.parse_args()
        data = request.data
        user_data = json.loads(data).get('user')
        new_user = User(**user_data)
        return new_user, 201

class UserLogin(Resource):
    route_base = '/users/login/'

    def get(self):
        user, passwd = request.args.values()
        if User.get(login=user):
            if User.get(login=user).password == passwd:
                return User.get(login=user).to_dict()
            else:
                msg = 'Password for user %s is not correct, try again !' %(user)
                error_dict= {'password': [msg,]}
                return make_error(406, 42, msg, '', errors=error_dict)
        else:
            msg = 'User %s does not exist, try again !' % (user)
            error_dict = {'login': [msg, ]}
            return make_error(406, 42, msg, '', errors=error_dict)

class UserMethodView(Resource):
    route_base = '/users/<int:id>/<string:method>'

    def get(self, id, method):
        # Dynamic call of methods in MethodView and rollback in case of exception
        try:
            return getattr(self, method)(id)
        except:
            rollback()
            abort(404)

    def stock_portfolio(self, id):
        if User.get(id=id):
            user = User[id]
            data = select((st.stock, sum(st.qty)) for st in StockTransaction if st.user_id == user)[:]
            new_data = []
            user_dict = {'User':{}}
            for line in data:
                last_hl = line[0].history_lines.order_by(StockHistory.date).first()
                curr_price = last_hl and last_hl.close or 0.00
                new_line = {'stock':line[0].to_dict(), 'qty': line[1], 'current_price': curr_price}
                new_data.append(new_line)
            user_dict['User'].update(portfolio=new_data)
            return user_dict

        raise 'User not found'




