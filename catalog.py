from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask,jsonify,json
import json


app = Flask(_name_)
api = Api(app)

 
@app.route('/books/<id>', methods=['GET'])
def getBookById(id):

    f = open('books.json',) 
    data = json.load(f) 

    for book in data['books']: 
        if book['id'] == int(id) :
            return jsonify(book)
    f.close()
    abort(404)

@app.route('/books', methods=['GET'])
def getBooksByTopic():
    topic = request.args.get('topic')
    f = open('books.json',) 
    data = json.load(f) 
    booksList = []
    for book in data['books']: 
        if book['topic'] == topic :
            bookDict = {
            'id': book['id'],
            'title': book['title']}
            booksList.append(bookDict)
            
    f.close()

    if len(booksList) == 0 :
        abort(404)

    return jsonify(booksList)

@app.route('/books/<id>', methods=['PUT'])
def updateBookQuantity(id):

    body = request.json
    newQuantity = body["quantity"]

    f = open('books.json','r+') 
    data = json.load(f) 
    for book in data['books']: 
        if book['id'] == int(id) :
            if (book['quantity'] < 1) or (newQuantity < 0) : 
                return abort(403) 
            book['title'] = body["title"]
            book['topic'] = body["topic"]
            book['quantity'] = newQuantity
            book['price'] = body["price"]
    f.close()

    with open("books.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return flask.Response(status=204)
    

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0')