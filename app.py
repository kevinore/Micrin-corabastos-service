from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import urllib.parse
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
username = urllib.parse.quote_plus('kevin')
password = urllib.parse.quote_plus('@Kevin3132480890')

client = MongoClient("mongodb+srv://%s:%s@corabastos-yqyfv.mongodb.net/test?retryWrites=true&w=majority"%(username,password))
db = client.Corabastos

@app.route('/', methods=['GET'])
def index():
    return "Hey"

@app.route('/data', methods=['GET'])
def getItems():
    items = list(db.items.find({}))
    json_return = []
    for item in items:
        json_docs = {'nombre':item['nombre'], 'presentacion':item['presentacion'], 'cantidad':item['cantidad'], 'unidad':item['unidad'], 'cal_extra':item['cal_extra'], 'cal_primera':item['cal_primera'], 'valorxunidad':item['valorxunidad']}
        json_return.append(json_docs)
        
    return jsonify(json_return)
    

if __name__ == '__main__':
    app.run()
