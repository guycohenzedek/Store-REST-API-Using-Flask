import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, _username, _password):
        self.id = _id
        self.username = _username
        self.password = _password


    @classmethod
    def find_by_username(cls, username):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conection.close()

        return user

    
    @classmethod
    def find_by_id(cls, _id):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conection.close()

        return user


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
        
        if User.find_by_username(data['username']) is not None:
            return {'message': 'username {} already exist'.format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_user_query = "INSERT INTO users  VALUES (NULL, ?, ?)"
        cursor.execute(insert_user_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message' : 'user created successfully'}, 201



