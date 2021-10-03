import os
from datetime import timedelta
from re import T

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager # JSON Web Token

from resources.item import Item, ItemsList
from resources.store import Store, StoresList
from resources.user import User, UserList, UserLogin, UserLogOut, UserRegister, TokenRefresh
from blacklist import BLACKLIST

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=5)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = 'start_flask'
api = Api(app)

jwt = JWTManager(app)

@jwt.additional_claims_loader ## Changed on vesrion 4.0.0 (before it was --> @jwt.user_claims_loader)
def add_claims_to_jwt(identity):
    if identity == 1:
         return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_in_black_list(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST 

# add resources to the api --> each resource has its own 'GET','POST, etc...
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(StoresList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogOut, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':

    @app.before_first_request
    def create_tables():
        db.create_all()

    from db import db
    db.init_app(app)

    # debug=True is necessary for detailed errors
    app.run(port=5000 ,debug=True)
