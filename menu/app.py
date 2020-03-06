##!/usr/bin/python

"""
Menu Microservice
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
import os
import json
from flask import Flask, jsonify, request
from model.base import db
from model.data_models import Vendor, Food
from sqlalchemy_utils import database_exists, create_database

def create_app(uri):
  """
  Creates and starts the App with all the required settings
  mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
  """
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = uri
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  # create the database menu if it does not exist
  if not database_exists(uri):
    create_database(uri)
  db.init_app(app)
  return app

app = create_app(os.environ['URI'])
app.app_context().push() # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
db.create_all() # Creates All Tables 

# Please disable by commenting off app.route -- For Testing Purposes Only
@app.route("/all_vendors", methods=["GET"])
def all_vendors():
  """
  Obtains JSON of all Vendors
  """
  output = {"status": ""}
  try:
    vendors = Vendor.query.all()
    output['status'] = "success"
    output['vendors'] = [vendor.json_full() for vendor in vendors]
    return jsonify(output), 200
  except:
    output['status'] = "error"
    return jsonify(output), 400 

# Please disable by commenting off app.route -- For Testing Purposes Only
@app.route("/all_food", methods=["GET"])
def all_food():
  """
  Obtains JSON of all Available Food
  """
  output = {"status": ""}
  try:
    foods = Food.query.all()
    output['status'] = "success"
    output['food'] = [food.json_full() for food in foods]
    return jsonify(output), 200
  except:
    output['status'] = "error"
    return jsonify(output), 400

@app.route("/menu", methods=["GET"])
def menu():
  """
  Obtains the FULL Menu
  
  Structure:
  
  { status:
    vendors: [
      {
        vendor_id:
        vendor_name:
        halal:
        foods: [
          {
            food_id:
            food_name:      
            food_description:
            food_price:
          } 
        ]
      }
    ]
  }
  """
  output = {"status": ""}
  try:
    vendor_list = []
    vendors = Vendor.query.all()
    for vendor in vendors:
      foods = Food.query.filter_by(vendor_id=vendor.vendor_id, availability=True, listed=True)
      vendor_json = vendor.json_full()
      vendor_json['foods'] = [food.json_default() for food in foods]
      vendor_list.append(vendor_json)
    output['status'] = "success"
    output['vendors'] = vendor_list
    return jsonify(output), 200
  except:
    output['status'] = "error"
    return jsonify(output), 400
  
@app.route("/menu_basic", methods=["GET"])
def menu_basic():
  """
  Obtains the Basic Menu
  
  Structure:
  
  { status:
    vendors: [
      {
        vendor_id:
        vendor_name:
        foods: [
          {
            food_id:
            food_name:     
          } 
        ]
      }
    ]
  }
  """
  output = {"status": ""}
  try:
    vendor_list = []
    vendors = Vendor.query.all()
    for vendor in vendors:
      foods = Food.query.filter_by(vendor_id=vendor.vendor_id, availability=True, listed=True)
      vendor_json = vendor.json_basic()
      vendor_json['foods'] = [food.json_basic() for food in foods]
      vendor_list.append(vendor_json)
    output['status'] = "success"
    output['vendors'] = vendor_list
    return jsonify(output), 200
  except:
    output['status'] = "error"
    return jsonify(output), 400

@app.route("/vendor/add", methods=["POST"])
def add():
  """
  Allows a Vendor to add an item to the menu
  """
  output = {"status": ""}
  if request.is_json:
    information = request.json
    try:
      vendor_id        = information['vendor_id']
      food_name        = information['food_name']
      food_description = information['food_description']
      food_price       = information['food_price']
      db.session.add(Food(vendor_id,food_name,food_description,food_price))
      db.session.commit()
      output['status'] = "success"
      code = 200    
    except:
      output['status'] = "error"
      output['message'] = "Error with information processing"
      code = 400
  else:
    output['status'] = "error"
    output['message'] = "Posted Information is not JSON"
    code = 400
    
  return jsonify(output), code

@app.route("/vendor/update", methods=["PUT"])
def update():
  """
  Allows a Vendor to add an item to the menu
  """
  output = {"status": ""}
  if request.is_json:
    information = request.json
    try:
      food_id        = information['food_id']
      food_name        = information['food_name']
      food_description = information['food_description']
      food_price       = information['food_price']
      food = Food.query.filter_by(food_id=food_id).update({"food_name": food_name,
                                                           "food_description": food_description,
                                                           "food_price": food_price})
      db.session.commit()
      output['status'] = "success"
      code = 200    
    except:
      output['status'] = "error"
      output['message'] = "Error with information processing"
      code = 400
  else:
    output['status'] = "error"
    output['message'] = "Posted Information is not JSON"
    code = 400
    
  return jsonify(output), code

@app.route("/vendor/delete", methods=["DELETE"])
def delete():
  """
  Allows a Vendor to add an item to the menu
  """
  output = {"status": ""}
  if request.is_json:
    information = request.json
    try:
      food_id = information['food_id']
      food = Food.query.filter_by(food_id=food_id).update({"availability": False,
                                                           "listed": False})
      db.session.commit()
      output['status'] = "success"
      code = 200    
    except:
      output['status'] = "error"
      output['message'] = "Error with information processing"
      code = 400
  else:
    output['status'] = "error"
    output['message'] = "Posted Information is not JSON"
    code = 400
    
  return jsonify(output), code