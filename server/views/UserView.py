from flask_restful import reqparse, abort, Resource, fields, marshal_with, request, marshal
from flask import jsonify
from flask_classy import FlaskView
from models.User import User
import json

parser = reqparse.RequestParser()
parser.add_argument('user', 'users', 'username', 'password')

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
        return User.select().limit(80)

    @marshal_with(resource_fields)
    def post(self):
        # data = parser.parse_args()
        data = request.data
        user_data = json.loads(data).get('user')
        new_user = User(**user_data)
        return new_user, 201

class UserLogin(FlaskView):
    route_base = '/users/login/'

    def get(self):
        user, passwd = request.args.values()
        if User.get(login=user):
            return jsonify(marshal(User.get(login=user), resource_fields))
        abort(404)



