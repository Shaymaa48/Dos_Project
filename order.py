from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask,jsonify,json
import requests
import json
import time
from datetime import datetime

app = Flask(_name_)
api = Api(app)


@app.route('/orders', methods=['POST'])
def addNewOrder():
    body = request.get_json()
    id = body["id"]
  
    r = requests.get('http://192.168.10.112:5000/books/{}'.format(id))
    if r.status_code == 404:
        return abort(404, description="no books found") 

    response = r.json()
    quantity = response["quantity"]
    if quantity == 0 :
        return abort(400, description="out of stock") 


    newQuantity = quantity - 1
    response["quantity"] = newQuantity
    r2 = requests.put('http://192.168.10.112:5000/books/{}'.format(str(id)), json=(response))
    if r.status_code == 403: return abort(403, description="failed") 

    return jsonify({"title" : response["title"]})
    

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0')