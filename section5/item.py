import sqlite3
from sqlite3.dbapi2 import Cursor
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required # JSON Web Token

class Item(Resource):

    # Use parser as part of the class itself to be reused wherever we want
    parser = reqparse.RequestParser()
    # Add arg named 'price' --> that will make sure that only this 
    # field will be checked and updated into existing item
    parser.add_argument('price', 
                        type=float, # price can be 12.00
                        required=True, # will make sure that you must give this filed
                        help="This files cannot be empty" # message to be display upon error
                        )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert_value(cls, new_item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (new_item['name'], new_item['price']))

        connection.commit()
        connection.close()


    @jwt_required() # required authentication when you want to get item
    def get(self, name): # 'GET'
        item = self.find_by_name(name)

        if item:
            return item
        return {'message': 'Item not found'} ,404

    @jwt_required()
    def post(self, name): # 'POST'
        
        # Check if already exist --> do nothing but display message
        if self.find_by_name(name):
            return {'message': "An item with name: {} is already exists".format(name)}, 400

        # get the arguments after they checked by the parser
        request_data = Item.parser.parse_args()

        new_item = {'name': name,
                    'price': request_data['price']
                   }
        Item.insert_value(new_item)
        
        return new_item, 201

    @jwt_required()
    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        
        return {"message": "Item deleted"}

    @jwt_required()
    def put(self, name):

        request_data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name' : name, 'price' : request_data['price']}
        
        if item is None:

            Item.insert_value(updated_item)
        
        else:

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (updated_item['price'], updated_item['name']))
            
            connection.commit()
            connection.close()


        return updated_item



class ItemsList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        rows = result.fetchall()
        connection.close()
        return {'items': rows}
