from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot left blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot left blank')


    def post(self): #register new user into database
        
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'username {} already exist'.format(data['username'])}, 400

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
        return {'users': [user.json() for user in UserModel.find_all()]}
