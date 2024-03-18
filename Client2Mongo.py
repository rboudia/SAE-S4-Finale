from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import pprint

collections_bp = Blueprint('collections', __name__)

class Client2Mongo:
    def __init__(self, bd):
        self.client = MongoClient()
        self.bd = self.client[bd]
        
    def liste_des_collections(self):
        return self.bd.list_collection_names()
    
    def get_collection(self, coll):
        return self.bd[coll]
    
    def find_one(self, collection_name):
        return self.bd[collection_name].find_one()
    
    def find(self, collection_name):
        return self.bd[collection_name].find()
    
    

if __name__ == "__main__":
   
    bd = Client2Mongo("rayan")
    
    pprint.pprint(bd.liste_des_collections())
    
    print(" ")
    
    for joueurs in bd.find("tournois"):
        pprint.pprint(joueurs)
        print(" ")

    
    