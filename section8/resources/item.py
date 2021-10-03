from flask_restful import Resource, reqparse
from flask_jwt import jwt_required # JSON Web Token

from models.item import ItemModel

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
    
    parser.add_argument('store_id', 
                        type=int, # price can be 12.00
                        required=True, # will make sure that you must give this filed
                        help="Every item need store id" # message to be display upon error
                        )
    
    

    @jwt_required() # required authentication when you want to get item
    def get(self, name): # 'GET'
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'} ,404

    @jwt_required()
    def post(self, name): # 'POST'
        
        # Check if already exist --> do nothing but display message
        if ItemModel.find_by_name(name):
            return {'message': "An item with name: {} is already exists".format(name)}, 400

        # get the arguments after they checked by the parser
        request_data = Item.parser.parse_args()

        new_item = ItemModel(name, request_data['price'], request_data['store_id'])
        
        new_item.save_to_db()
        
        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        
        if item:
            item.delete_from_db()
        
        return {"message": "Item deleted"}

    @jwt_required()
    def put(self, name):

        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']

        item.save_to_db()
        return item.json()



class ItemsList(Resource):

    def get(self):
        
        return {'items': [item.json() for item in ItemModel.find_all()]}
