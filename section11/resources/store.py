from flask_restful import Resource
from flask_jwt_extended import jwt_required # JSON Web Token
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        
        return {'messgae': 'Store not found'}, 404

    def post(self, name):
        
        if StoreModel.find_by_name(name):
            return {'message': 'store with name {} already exist'.format(name)}, 400

        store = StoreModel(name)
        store.save_to_db()

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message' : 'Store deleted'}


class StoresList(Resource):

    def get(self):
        return {'Stores': [store.json() for store in StoreModel.find_all()]}
