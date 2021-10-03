from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT # JSON Web Token

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemsList

app = Flask(__name__)
app.secret_key = 'start_flask'
api = Api(app)

app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=5)
jwt = JWT(app, authenticate, identity)

# add resources to the api --> each resource has its own 'GET','POST, etc...
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

# debug=True is necessary for detailed errors
app.run(port=5000 ,debug=True)