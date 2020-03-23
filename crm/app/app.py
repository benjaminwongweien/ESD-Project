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

def create_app(uri):
    """ Creates and starts the App with all the required settings """
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

# app=create_app("mysql+mysqlconnector://root:@127.0.0.1:3306/menu")
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
    return jsonify({"status": "error", "error": e.description}), e.code
        
@app.route("/chatid", methods=["POST"])
def chatId():
    ''' get the user's info based on the chat id -> telegram bot '''
    chat_id = request.form.get("chatid")
    if chat_id:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify(user.json(0,1,2))
        else:
            return jsonify(
                {"status": 0, 
                 "data": {"msg": "user not found"}})
    else:
        return jsonify({"status": 0, 
                        "data": {"msg": "cannot read chat_id"}})

@app.route("/username", methods=["POST"])
def username():
    ''' get the user's info based on the username '''
    username = request.form.get("username")
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify(user.json(0,1,2))
        else:
            return jsonify({"status": 0, 
                            "data": {"msg": "user not found"}})
    else:
        return jsonify({"status": 0, 
                        "data": {"msg": "cannot read userid"}})

@app.route("/usertype", methods=["POST"])
def user_type():
    ''' get all the user's information based on usertype '''
    user_type = request.form.get("user_type")
    if user_type:
        users = User.query.filter_by(user_type=user_type).all()
        if users:
            return jsonify([user.json(0,2) for user in users])
        else:
            return jsonify({"status": 0, 
                    "data": {"msg": "type not found"}})
    else:
        return jsonify({"status": 0,
                "data": {"msg": "cannot read type"}})

@app.route("/register", methods=["POST"])
def register():
    ''' registers a user '''
    uid = request.form.get("uid")
    uType = request.form.get("type")
    teleId = request.form.get("tid")
    if uid and uType:
       users = User.query.filter_by(username=uid).scalar()
       if users:
            return jsonify({"status": 0, 
                    "data": {"msg": "user is registered in the system"}})
       else:
           db.session.add(User(uid,uType,teleId))
           db.session.commit()
           return jsonify({"registration":"success"})
    else:
        return jsonify({"status": 0, 
                "data": {"msg": "cannot read data"}})


@app.route("/register_tele", methods=["POST"])
def register():
    ''' registers a user's telegram chat id '''
    uid = request.form.get("uid")
    uType = request.form.get("type")
    teleId = request.form.get("tid")
    if uid and uType:
       users = User.query.filter_by(username=uid).scalar()
       if not users:
            return jsonify({"status": 0, 
                    "data": {"msg": "user is not registered in the system"}})
       else:
           user = User.query.filter_by(username=uid).update({"chat_id": teleId})
           db.session.commit()
           return jsonify({"registration":"success"})
    else:
        return jsonify({"status": 0, 
                "data": {"msg": "cannot read data"}})