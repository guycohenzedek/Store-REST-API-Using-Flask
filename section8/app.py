import os

from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT # JSON Web Token

from security import authenticate, identity
from resources.user import UserList, UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoresList
from resources.user import User, UserList

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=5)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'start_flask'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# add resources to the api --> each resource has its own 'GET','POST, etc...
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(StoresList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()

    from db import db
    db.init_app(app)

    # debug=True is necessary for detailed errors
    app.run(port=5000 ,debug=True)
