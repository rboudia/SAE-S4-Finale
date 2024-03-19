from flask import Blueprint
from pymongo import MongoClient

collections_bp = Blueprint('collections', __name__)


class Client2Mongo:
    def __init__(self, nom_bd):
        self.client = MongoClient()
        self.bd = self.client[nom_bd]

    def liste_des_collections(self):
        return self.bd.list_collection_names()

    def get_collection(self, coll):
        return self.bd[coll]

    def find_one(self, collection_name):
        return self.bd[collection_name].find_one()

    def find(self, collection_name):
        return self.bd[collection_name].find()


