from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api 
from flask import request
from flask import Flask,jsonify,json
import json
import requests
import argparse
import os
import sys
from typing import Type
from flask.json import jsonify
import requests
import json
from datetime import datetime
import urllib
import urllib3
urllib.request
import http

#some variables to use later 
divider = "\n_____________________________________\n"
exit = "/exit"
help = "/help"
search = "/search"
info = "/info"
purchase = "/purchase"

app = Flask(_name_)
api = Api(app)

#getting the book by its ID
@app.route('/info/<id>', methods=['GET'])
def getBookById(id):
  #using get method to get the book information by id 
    r = requests.get('http://192.168.10.112:5000/books/{}'.format(id))
  
  #checking the response status
    if r.status_code == 404:
        return "invalid book number" 

    if r.status_code == 200:
        response = r.json()
        #print the values if the response is okay
        res = divider
        res +=  "id      : "+str(response["id"]) + "\n" 
        res +=  "title   : "+response["title"] + "\n" 
        res +=  "price   : "+str(response["price"])+ "\n" 
        res +=  "quantity: "+str(response["quantity"]) 
        res += divider        
        return res

    else : return "ERROR try again later"

#getting the books by searching by a topic
@app.route('/search/<topic>', methods=['GET'])
def getBooksByTopic(topic):
    print("Book By topic")
    r = requests.get('http://192.168.10.112:5000/books?topic={}'.format(topic))
    if r.status_code == 404:
        return "  no books found with this topic" 
    if r.status_code == 200:
        response = r.json()
        print(r.text)
        res = divider
        for d in response:
            res += "id    : "+str(d["id"]) + "\n" 
            res += "title : "+d["title"] 
            res += divider
        return res

    else : return "ERROR try again later"

@app.route('/purchase/<id>', methods=['POST'])
def updateBookQuantity(id):
    print("Book Quantity")

#here we send with the request a json file with the id , for the orders to know which book to choose
    r = requests.post('http://192.168.10.111:5000/orders',
                         json={"id":int(id)})
    if r.status_code == 404:
        return "No Book found, Invalid Id"
    if r.status_code == 400:
        return "Out of stock"
    if r.status_code == 200:
        response = r.json()
        return "Bought Book '" + response["title"]+"'"
    else : return "ERROR try again later"
        

#command info
print("\n Welcome to Bazar.com ")
print("\n/help => for Command list ")
print("/exit => to exit \n")

Userinput = ""
while (True) :
    #getting user command
    Userinput = input("> ")
    command = Userinput.split(" ",1)
    if Userinput == exit :
        break
    elif Userinput == help :
        print("\n /search (topic)\n")
        print(" /info (item_id)\n")
        print(" /purchase (item_id)\n")
        
        #checking if the length of the command < 2 , so the program will refuse the command if it less than 2
        #becase the 3 commands are 2 parts 
    elif len(command) < 2 :
        print("  invalid command")
        
    else :
        if command[0] == search:
            print(getBooksByTopic(command[1]))

        elif (command[0] == info) :
            print(getBookById(command[1]))

        elif (command[0] == purchase) :
           
            print("  " + updateBookQuantity(command[1]))

        else :
            print("  invalid command")


print("Thank you for using Bazar.com ????")

divider = "\n-----------------------------------------------\n"
if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0')
