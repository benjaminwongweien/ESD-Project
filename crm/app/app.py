"""
CRM Microservice

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@team   - G3T4
"""

import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model.base import db
from model.data_models import User

#####################
#   JSON MESSAGES   #
#####################

# REGISTRATION IS SUCCESSFUL
REGISTER_SUCCESS = {"status": 0,
                    "data":
                        {"register": "success"}
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
                         {"msg": "user(s) not found"}
                    }

# USER INFORMATION IS ALREADY IN THE SYSTEM
EXIST_ERROR      =  {"status": 4, 
                     "data": 
                         {"msg": "user is already registered in the system"}
                    }

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

# app = create_app("mysql+mysqlconnector://root:@127.0.0.1:3306/menu")
app = create_app(os.environ["URI"])
app.app_context().push() # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

######################
#       ROUTES       #
######################

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
def error(e):
    return jsonify({"status": "error", "error": e.description}), e.code

@app.route("/dump", methods=["GET"])
def dump():
  """ Dumps all the Table Information -> Debug Purposes """
  users = User.query.all()
  return jsonify({"user": [user.json(0,1,2) for user in users]})

@app.route("/chatid", methods=["POST"])
def chat_id():
    """ get the user's info based on the chat id -> telegram bot """
    if request.is_json:
        chat_id = request.json.get("tid")
        if chat_id:
            user = User.query.filter_by(chat_id=chat_id).first()
            if user:
                return jsonify(user.json(0,1,2))
            else:
                return jsonify(NON_EXIST_ERROR), 400
        else:
            return jsonify(INCOMPLETE_ERROR), 400
    else:
        return jsonify(FORMAT_ERROR), 400

@app.route("/username", methods=["POST"])
def username():
    """ get the user's info based on the username """
    if request.is_json:
        username = request.json.get("username")
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify(user.json(0,1,2))
            else:
                return jsonify(NON_EXIST_ERROR), 400
        else:
            return jsonify(INCOMPLETE_ERROR), 400
    else:
        return jsonify(FORMAT_ERROR), 400

@app.route("/usertype", methods=["POST"])
def user_type():
    """ get all the user's information based on usertype """
    if request.is_json:
        username = request.json.get("user_type")
        if user_type:
            users = User.query.filter_by(user_type=user_type).all()
            if users:
                return jsonify([user.json(0,2) for user in users])
            else:
                return jsonify(NON_EXIST_ERROR), 400
        else:
            return jsonify(INCOMPLETE_ERROR), 400       
    else:
        return jsonify(FORMAT_ERROR), 400

@app.route("/register", methods=["POST"])
def register():
    """ registers a user """
    if request.is_json:
        uid, uType = request.json.get("uid"), request.json.get("type")
        if uid and uType:
            users = User.query.filter_by(username=uid).scalar()
            if users:
                    return jsonify(EXIST_ERROR), 400
            else:
                db.session.add(User(uid, uType, request.json.get("tid")))
                db.session.commit()
                return jsonify(REGISTER_SUCCESS), 200
        else:
            return jsonify(INCOMPLETE_ERROR), 400    
    else:
        return jsonify(FORMAT_ERROR), 400

@app.route("/register_tele", methods=["POST"])
def register_tele():
    """ registers a user's telegram chat id """
    if request.is_json:
        uid, teleId = request.json.get("uid"), request.json.get("tid")
        if uid and teleId:
            users = User.query.filter_by(username=uid).scalar()
            if not users:
                    return jsonify(EXIST_ERROR), 400
            else:
                user = User.query.filter_by(username=uid).update({"chat_id": teleId})
                db.session.commit()
                return jsonify(REGISTER_SUCCESS), 200
        else:
            return jsonify(INCOMPLETE_ERROR),400  
    else:
        return jsonify(FORMAT_ERROR), 400