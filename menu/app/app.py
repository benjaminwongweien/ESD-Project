"""
Menu Microservice

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@team   - G3T4
"""
import os
import os.path
import json
from flask import Flask, jsonify, request, send_from_directory
from sqlalchemy import desc
from flask_cors import CORS
from model.base import db
from model.data_models import Vendor, Food

#####################
#   JSON MESSAGES   #
#####################

# REGISTRATION IS SUCCESSFUL
UPLOAD_SUCCESS = {"status": 0,
                    "data":
                        {"register": "success"}
                    }

# UPLOAD IS SUCCESSFUL
UPLOAD_SUCCESS = {"status": 0,
                    "data":
                        {"upload": "success"}
                    }

# THE MESSAGE RECEIVED IS NOT JSON
FORMAT_ERROR     = {"status": 1, 
                    "data": 
                        {"msg": "message not json"}
                    }

# THE MESSAGE RECEIVED HAS INCOMPLETE DATA
INCOMPLETE_ERROR = {"status": 2,
                    "data": 
                        {"msg": "missing data in request"}
                    }

# USER INFORMATION IS NOT FOUND
NON_EXIST_ERROR  =  {"status": 3, 
                     "data": 
                         {"msg": "information not found"}
                    }

# USER INFORMATION IS ALREADY IN THE SYSTEM
EXIST_ERROR      =  {"status": 4, 
                     "data": 
                         {"msg": "user is already registered in the system"}
                    }

DATABASE_ERROR   =  {"status": 5, 
                     "data": 
                         {"error": "the database had an unknown error",
                          "check": "check if your inputs are in the correct format e.g. INT etc"}
                    }

# INCOMPATIBILITY
BAD_REQUEST    =  {"status": 6,
                    "data":
                        {"msg": "one or more of the data sent over is incompatible with the database"}
                    }

####################
#    VALIDATION    #
####################

def is_float(s):
  try:
    return float(s)
  except:
    return False
  
#####################
#     FLASK APP     #
#####################

def create_app(uri):
  """ Creates and starts the App with all the required settings """
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = uri
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  return app

######################
#      INIT APP      #
######################

# app=create_app("mysql+mysqlconnector://root:@127.0.0.1:3306/menu")
app = create_app(os.environ["URI"])
app.app_context().push() # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

#######################
#        DEBUG        #
#######################

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

@app.route("/dump", methods=["GET"])
def dump():
  """ Dumps all the Table Information -> Debug Purposes """
  vendors = Vendor.query.all()
  foods   = Food.query.all()
  return jsonify({"vendor": [vendor.json(0,1,2,3,4,5) for vendor in vendors],
                  "food": [food.json(0,1,2,3,4,5,6,7,8) for food in foods]})

@app.route("/all_vendor", methods=["GET"])
def all_vendors():
  """ Obtains JSON of all Vendors """
  output = dict()
  output['status'] = 0
  output['vendors'] = [vendor.json(0,1,2,3,4,5) for vendor in Vendor.query.all()]
  return jsonify(output), 200

@app.route("/all_food", methods=["GET"])
def all_food():
  """ Obtains JSON of all Available Food """
  output = dict()
  output['status'] = 0
  output['food'] = [food.json(0,1,2,3,4,5,6,7,8) for food in Food.query.all()]
  return jsonify(output), 200

#######################
#   CUSTOMER UI API   #
#######################

@app.route("/menu", methods=["GET"])
def menu():
  """ Obtains the FULL Menu
  
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
    } """
    
  output = dict()
  vendor_list = []
  for vendor in Vendor.query.all():
    foods = Food.query.filter_by(vendor_id=vendor.vendor_id, availability=True, listed=True)
    vendor_json = vendor.json(0,1,3,4,5)
    vendor_json['foods'] = [food.json(1,2,3,4,5,6) for food in foods]
    vendor_list.append(vendor_json)
  output['status'] = "success"
  output['vendors'] = vendor_list
  return jsonify(output), 200
    
@app.route("/search/vendor", methods=["POST"])
def shopfront():
  """ search for a vendor's shopfront """
  if request.is_json:
    if vendor_id := request.json.get('vendor_id'): 
      vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
      foods  = Food.query.filter_by(vendor_id=vendor_id,availability=True,listed=True).all()
      if vendor and foods:
        output = {"status": "success"}
        output.update(dict(vendor.directory()))
        output.update({"food": [food.json(1,2,3,4,5,6) for food in foods]})
        return jsonify(output), 200 
      else:
        return jsonify(NON_EXIST_ERROR), 400
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400

@app.route("/search/food", methods=["POST"])
def purchase():
  """ search for a vendor's food information """
  if request.is_json:
    vendor_id, food_id = request.json.get('vendor_id'), request.json.get('food_id')
    if vendor_id and food_id:
      food = Food.query.filter_by(vendor_id=vendor_id,food_id=food_id,availability=True,listed=True).first()
      if food:
        output = {"status": "success"}
        output.update({"food": food.json(0,1,2,3,4,5,6)})
        return jsonify(output), 200 
      else:
        return jsonify(NON_EXIST_ERROR), 400
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400
    
#######################
#    VENDOR UI API    #
#######################
@app.route("/register_info", methods=["POST"])
def register_info():
  """ registeres a new vendor with a menu """
  if request.is_json:
    vendor_name        = request.json.get('vendor_name')
    vendor_email       = request.json.get('vendor_email')
    vendor_description = request.json.get('vendor_description')
    vendor_location    = request.json.get('vendor_location')
    if all([vendor_name,vendor_email,vendor_description,vendor_location]):
      try:
        db.session.add(Vendor(vendor_name,vendor_email,vendor_description,vendor_location,vendor_image="vendor/default"))
        db.session.commit()
        vendor = Vendor.query.filter_by(vendor_email=vendor_email).first()
        return jsonify({"status": 0,
                        "data":
                          {"vendor_id": vendor.vendor_id}
                        }), 200
      except:
        return jsonify(DATABASE_ERROR), 503
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400  

@app.route("/update_info/<string:vendor_id>", methods=["PUT"])
def register(vendor_id):
  """ updates new vendor information """
  if request.is_json:
    vendor_name        = request.json.get('vendor_name')
    vendor_description = request.json.get('vendor_description')
    vendor_location    = request.json.get('vendor_location')
    if all([vendor_name,vendor_description,vendor_location]):     
      if all([len(var) <= 80 for var in [vendor_name,vendor_location]]): 
        try:
          vendor = Vendor.query.filter_by(vendor_id=vendor_id).update({"vendor_name": vendor_name,
                                                                      "vendor_description": vendor_description,
                                                                      "vendor_location": vendor_location})
          if vendor:
            db.session.commit()
            return jsonify(UPLOAD_SUCCESS), 200
          else:
            return jsonify(NON_EXIST_ERROR), 400
        except:
          return jsonify(DATABASE_ERROR), 503
      else:
        return jsonify(BAD_REQUEST), 400
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400 


@app.route("/vendor/add", methods=["POST"])
def add():
  """ allows a vendor to add an item to the menu """
  if request.is_json:
    vendor_id        = request.json.get('vendor_id')
    food_name        = request.json.get('food_name')
    food_description = request.json.get('food_description')
    food_price       = request.json.get('food_price')
    if all([vendor_id,food_name,food_description,food_price]):
      if is_float(food_price) and len(food_name) <= 80:
        try:
          db.session.add(Food(vendor_id,food_name,food_description,food_price))
          db.session.commit()
          food = Food.query.filter_by(vendor_id = vendor_id).order_by(desc(Food.food_id)).first()
          return jsonify({"status": 0,
                          "data":
                            { "vendor_id": vendor_id,
                              "food_id"  : food.food_id}
                          }), 200
        except:
          return jsonify(DATABASE_ERROR), 503
      else:
        return jsonify(BAD_REQUEST), 400        
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400
    
@app.route("/vendor/update", methods=["PUT"])
def update():
  """ allows a vendor to add an item to the menu """
  if request.is_json:
    vendor_id        = request.json.get('vendor_id')
    food_id          = request.json.get('food_id')
    food_name        = request.json.get('food_name')
    food_description = request.json.get('food_description')
    food_price       = request.json.get('food_price')
    if all([vendor_id,food_id,food_name,food_name,food_description,food_price]):
      try:
        food = Food.query.filter_by(vendor_id = vendor_id,
                                    food_id   = food_id).update({"food_name"       : food_name,
                                                                 "food_description": food_description,
                                                                 "food_price"      : food_price})
        db.session.commit()
        food = Food.query.filter_by(vendor_id = vendor_id,
                                    food_id   = food_id).first()
        return jsonify({"status": 0,
                        "data":
                          { "vendor_id": vendor_id,
                            "food_id"  : food.food_id}
                        }), 200
      except:
        return jsonify(DATABASE_ERROR), 503
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400
    
@app.route("/vendor/delete", methods=["DELETE"])
def delete():
  """ Allows a Vendor to delete an item from the menu """
  if request.is_json:
    vendor_id = request.json.get('vendor_id')
    food_id   = request.json.get('food_id')
    if vendor_id and food_id:
      food = Food.query.filter_by(vendor_id = vendor_id,
                                  food_id   = food_id).update({"availability": False,
                                                               "listed": False})
      if food:
        db.session.commit()
        return jsonify(UPLOAD_SUCCESS), 200 
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400

@app.route("/vendor/take_off", methods=["PUT"])
def take_off():
  """ allows a vendor to take an item off the menu """
  if request.is_json:
    vendor_id = request.is_json('vendor_id')
    food_id   = request.is_json('food_id')
    if vendor_id and food_id:
      food = Food.query.filter_by(vendor_id = vendor_id,
                                  food_id   = food_id,
                                  listed    = True).update({"availability": False})
      if food:
        db.session.commit()
        return jsonify(UPLOAD_SUCCESS), 200
      else:
        return jsonify(NON_EXIST_ERROR), 400
    else:
      return jsonify(INCOMPLETE_ERROR), 200 
  else:
      return jsonify(FORMAT_ERROR), 400

@app.route("/vendor/put_up", methods=["PUT"])
def put_up():
  """ Allows a Vendor to take an item off the menu """
  if request.is_json:
    vendor_id = request.is_json('vendor_id')
    food_id   = request.is_json('food_id')
    if vendor_id and food_id:
      food = Food.query.filter_by(vendor_id = vendor_id,
                                  food_id   = food_id,
                                  listed    = True).update({"availability": True})
      if food:
        db.session.commit()
        return jsonify(UPLOAD_SUCCESS), 200
      else:
        return jsonify(NON_EXIST_ERROR), 400
    else:
      return jsonify(INCOMPLETE_ERROR), 400
  else:
    return jsonify(FORMAT_ERROR), 400

@app.route("/images/<path:file_name>", methods=["GET"])
def staticfiles(file_name):
  """ Returns an image in static folder """
  if os.path.exists(os.path.join("./static",file_name)):
    return send_from_directory("./static", file_name)
  else:
    return jsonify(NON_EXIST_ERROR), 400

@app.route("/upload/<string:vendor_id>/<string:food_id>", methods=["POST"])
def upload_menu(vendor_id,food_id):
    """ Upload a food image in static folder """
    if "file" not in request.files:
      return jsonify(INCOMPLETE_ERROR), 400
    file = request.files["image"]
    food = Food.query.filter_by(food_id=food_id).update({f"food_image": "food/{vendor_id}/{food_id}"})
    if not food:
      return jsonify(NON_EXIST_ERROR), 400
    else:
      db.session.commit()
      file.filename = food_id
      path = os.path.join("./static/food", vendor_id)
      if not os.path.exists(path):
        os.makedirs(path)
      file.save(os.path.join(path, file.filename))
      return jsonify(UPLOAD_SUCCESS), 400
    
@app.route("/upload/<string:vendor_id>/", methods=["POST"])
def upload_vendor(vendor_id):
    """ Upload a vendor_image in static folder """
    if "file" not in request.files:
      return jsonify(INCOMPLETE_ERROR), 400
    file = request.files["image"]
    vendor = Vendor.query.filter_by(vendor_id=vendor_id).update({f"vendor_image": "vendor/{vendor_id}"})
    if not vendor:
      return jsonify(NON_EXIST_ERROR), 400
    else:
      db.session.commit()
      file.filename = vendor_id
      file.save(os.path.join("./static/vendor", file.filename))
      return jsonify(UPLOAD_SUCCESS), 400