from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required # JSON Web Token

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'start_flask'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# Create in-memory database
items = []

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

    @jwt_required() # required authentication when you want to get item
    def get(self, name): # 'GET'
        
        # next() --> will take the first result from the list of the results returned by filter()
        item = next(filter(lambda x: x['name'] == name, items), None)
        
        # return the item + coressponding error code
        return {'item': item}, 200 if item is not None else 404


    def post(self, name): # 'POST'
        
        # Check if already exist --> do nothing but display message
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name: {} is already exists".format(name)}, 400

        # get the arguments after they checked by the parser
        request_data = Item.parser.parse_args()
        new_item = {'name': name,
                    'price': request_data['price']
                   }
        items.append(new_item)
        
        return new_item, 201

    def delete(self, name):
        
        # must use the global "items" because python will 
        # think that you define it by itself which is impossible
        global items 

        # build new list that contains all the previous list except for the one we requested to delete     
        items = list(filter(lambda x: x['name'] != name, items)) 
        
        return {"message": "Item deleted"}

    def put(self, name):

        request_data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {'name' : name, 'price' : request_data['price']}
            items.append(item)
        else:
            # update dictionary by another dictionary
            # only the relevant fields will be updated according to the parser validation
            item.update(request_data)

        return item



class ItemsList(Resource):

    def get(self):
        return {'items': items}


# add resources to the api --> each resource has its own 'GET','POST, etc...
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

# debug=True is necessary for detailed errors
app.run(port=5000 ,debug=True)