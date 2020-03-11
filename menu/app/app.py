"""
Menu Microservice
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model.base import db
from model.data_models import Vendor, Food

def create_app(uri):
  """
  Creates and starts the App with all the required settings
  """
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = uri
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  return app

app = create_app(os.environ["URI"])
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
app.app_context().push() 

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
def error(e):
  return jsonify({"status": "error",
                  "error" : e.description}), e.code

@app.route("/bootstrap", methods=["GET"])
def bootstrap():
  """Bootstrap the Server"""
  db.create_all()
  db.session.commit()
  import csv
  with open("menu.csv","r") as file:
    csvfile = csv.reader(file,delimiter=",",quotechar='"')
    csvfile = list(csvfile)
  
  for x in range(1,6):
    line = csvfile[x-1]
    db.session.add(Vendor(line[0],
                          line[1],
                          line[2],
                          "vendor/{}".format(x)))  
  db.session.commit()

  vendor_id=1
  food_id=1
  for x in range(7,36):
    line = csvfile[x-1]
    if line[0] == "":
      vendor_id += 1
    else:
      db.session.add(Food(vendor_id,
                          line[0],
                          line[1],
                          line[2],
                          line[3],
                          "food/{}/{}".format(vendor_id,food_id)))
      food_id += 1
  db.session.commit()
  return jsonify({"boostrap": "success"})

@app.route("/all_vendor", methods=["GET"])
def all_vendors():
  """ Obtains JSON of all Vendors """
  output = {"status": ""}
  vendors = Vendor.query.all()
  output['status'] = "success"
  output['vendors'] = [vendor.json(0,1,2,3,4) for vendor in vendors]
  return jsonify(output), 200

@app.route("/all_food", methods=["GET"])
def all_food():
  """ Obtains JSON of all Available Food """
  output = dict()
  foods = Food.query.all()
  output['status'] = "success"
  output['food'] = [food.json(0,1,2,3,4,5,6,7,8) for food in foods]
  return jsonify(output), 200

@app.route("/images/<path:file_name>", methods=["GET"])
def staticfiles(file_name):
  return send_from_directory("./static", file_name)

@app.route("/upload/<string:vendor_id>/<string:food_id>", methods=["POST"])
def upload_file(vendor_id,food_id):
    if request.method == "POST":
        file = request.files["image"]
        
        food = Food.query.filter_by(food_id=food_id).update({"food_image": "food/{}/{}".format(vendor_id,food_id)})
        db.session.commit()
        
        file.filename = food_id
        path = os.path.join("./static/food", vendor_id)
        if not os.path.exists(path):
          os.makedirs(path)
        file.save(os.path.join(path, file.filename))
        
    return {"status"      : "success",
            "image_upload": "success"}

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
        vendor_description:
        vendor_location:
        vendor_image:
        halal:
        foods: [
          {
            food_id:
            food_name:      
            food_description:
            food_image:
            food_price:
            food_label:
          } 
        ]
      }
    ]
  }
  """
  output = dict()
  vendor_list = []
  vendors = Vendor.query.all()
  for vendor in vendors:
    foods = Food.query.filter_by(vendor_id=vendor.vendor_id, availability=True, listed=True)
    vendor_json = vendor.json(0,1,2,3,4)
    vendor_json['foods'] = [food.json(1,2,3,4,5,6) for food in foods]
    vendor_list.append(vendor_json)
  output['status'] = "success"
  output['vendors'] = vendor_list
  return jsonify(output), 200
  
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
  output = dict()
  vendor_list = []
  vendors = Vendor.query.all()
  for vendor in vendors:
    foods = Food.query.filter_by(vendor_id=vendor.vendor_id, availability=True, listed=True)
    vendor_json = vendor.json(0,1)
    vendor_json['food'] = [food.json(1,2) for food in foods]
    vendor_list.append(vendor_json)
    output['status'] = "success"
    output['vendors'] = vendor_list
    return jsonify(output), 200
  
@app.route("/search/vendor", methods=["POST"])
def shopfront():
  if request.is_json:
    information = request.json
    try:
      vendor_id = information['vendor_id']
      vendor    = Vendor.query.filter_by(vendor_id=vendor_id).first()
      foods     = Food.query.filter_by(vendor_id=vendor_id,availability=True,listed=True).all()
      output = {"status": "success"}
      output.update(dict(vendor.directory()))
      output.update({"food": [food.json(1,2,3,4,5,6) for food in foods]})
      return jsonify(output), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400  

@app.route("/search/food", methods=["POST"])
def purchase():
  if request.is_json:
    information = request.json
    try:
      vendor_id = information['vendor_id']
      food_id   = information['food_id']
      food      = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id,availability=True,listed=True).first()
      output = {"status": "success"}
      output.update(food.json(0,1,2,3,4,5,6))
      return jsonify(output), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400  
  
### --- VENDOR APIs --- ###  
@app.route("/vendor/add", methods=["POST"])
def add():
  """ Allows a Vendor to add an item to the menu """
  if request.is_json:
    information = request.json
    try:
      vendor_id        = information['vendor_id']
      food_name        = information['food_name']
      food_description = information['food_description']
      food_price       = information['food_price']
      food_label       = information.get('food_label', None)
      db.session.add(Food(vendor_id,food_name,food_description,food_price,food_label))
      db.session.commit()
      return jsonify({"status"     : "success",
                      "description": "item has been added to the menu"}), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400
   
@app.route("/vendor/update", methods=["PUT"])
def update():
  """ Allows a Vendor to add an item to the menu """
  if request.is_json:
    information = request.json
    try:
      vendor_id        = information['vendor_id']
      food_id          = information['food_id']
      food_name        = information['food_name']
      food_description = information['food_description']
      food_price       = information['food_price']
      food = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id).update({"food_name"       : food_name,
                                                                               "food_description": food_description,"food_price"      : food_price})
      db.session.commit()
      return jsonify({"status"     : "success",
                      "description": "item has been modified in the menu"}), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400

@app.route("/vendor/delete", methods=["DELETE"])
def delete():
  """ Allows a Vendor to delete an item from the menu """
  if request.is_json:
    information = request.json
    try:
      vendor_id = information['vendor_id']
      food_id   = information['food_id']
      food = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id).update({"availability": False,
                                                                               "listed": False})
      db.session.commit()
      return jsonify({"status"     : "success",
                      "description": "item has been removed from the menu"}), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400

@app.route("/vendor/take_off", methods=["PUT"])
def take_off():
  """ Allows a Vendor to take an item off the menu """
  if request.is_json:
    information = request.json
    try:
      vendor_id = information['vendor_id']
      food_id   = information['food_id']
      food = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id,listed=True).update({"availability": False})
      db.session.commit()
      return jsonify({"status"     : "success",
                      "description": "item has been taken off the menu"}), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400

@app.route("/vendor/put_up", methods=["PUT"])
def put_up():
  """ Allows a Vendor to take an item off the menu """
  if request.is_json:
    information = request.json
    try:
      vendor_id = information['vendor_id']
      food_id   = information['food_id']
      food = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id,listed=True).update({"availability": True})
      db.session.commit()
      return jsonify({"status"     : "success",
                      "description": "item has been put onto the menu"}), 200 
    except:
      return jsonify({"status"     : "error", 
                      "description": "bad request"}), 400
  else:
    return jsonify({"status"     : "error", 
                    "description": "posted information is not json"}), 400
    
  return jsonify({"status"     : "error", 
                  "description": "an unknown error occured"}), 400