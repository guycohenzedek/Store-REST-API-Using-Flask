from flask_jwt_extended.utils import get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='This field cannot left blank')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cannot left blank')



class UserRegister(Resource):
    
    def post(self): #register new user into database
        
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'username {} already exist'.format(data['username'])}, 400

        if UserModel.check_is_password_exist(data['password']):
            return {'message': 'password is occuipied'}, 400

        user = UserModel(**data)
        user.save_to_db()
        
        return {'message' : 'user created successfully'}, 201


class User(Resource):
    
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
        
        return {"message": "User deleted"}, 200


class UserList(Resource):
    
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {'access_token' : access_token,
                    'refresh_token': refresh_token }, 200

        return {'message': 'Invalid Credentials!'}, 401


class UserLogOut(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200


class TokenRefresh(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
    
        return {'access_token': new_token}, 200