# Here, we define blueprint for this api

from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import User


users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)


user_param = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})


class UsersList(Resource):

    @api.expect(user_param, validate=True)
    def post(self):
        '''
        创建一条内容：user
        '''
        print("In UsersList.post()")
        post_data = request.get_json()
        username  = post_data.get('username')
        email     = post_data.get('email')

        #-----------------------------------------------

        response_object = {}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        # 添加
        db.session.add( User(username=username, email=email) )
        db.session.commit()

        response_object = {
            'message': f'{email} was added!'
        }
        return response_object, 201


    @api.marshal_with(user_param, as_list=True)
    def get(self):
        return User.query.all(), 200



class Users(Resource):

    @api.marshal_with(user_param)
    def get(self, user_id):
        '''
        查找某用户id是否存在
        url的参数处理：user_id <-- <int:user_id>
        '''
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200


api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')

