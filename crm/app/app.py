"""
CRM Microservice
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model.base import db
from model.data_models import User

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


@app.route("/bootstrap", methods=["GET"])
def bootstrap():
    import csv
    db.create_all()
    db.session.commit()
    with open("users.csv", "r", encoding="cp1252") as file:
        csvfile = list(csv.reader(file, delimiter=","))
    for user in csvfile:
        db.session.add(User(*user))
    db.session.commit()
    return jsonify({"bootstrap": "success"})

@app.route("/dump", methods=["GET"])
def dump():
    users = User.query.all()
    return jsonify([user.json(0,1,2) for user in users])
        

@app.route("/chatid", methods=["POST"])
def chatId():
    '''get the user info using chatId'''
    chat_id = request.form.get("chatid")
    if chat_id:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify(user.json(0,1,2))
        else:
            return jsonify({"status": 0, "data": {"msg": "user not found"}})
    else:
        return jsonify({"status": 0, "data": {"msg": "cannot read chat_id"}})



@app.route("/username", methods=["POST"])
def username():
    ''' get user information using userId'''
    username = request.form.get("username")
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify(user.json(0,1,2))
        else:
            return jsonify({"status": 0, "data": {"msg": "user not found"}})
    else:
        return jsonify({"status": 0, "data": {"msg": "cannot read userid"}})



@app.route("/usertype", methods=["POST"])
def user_type():
    '''get all user and info by usertype'''
    user_type = request.form.get("user_type")
    if user_type:
        users = User.query.filter_by(user_type=user_type).all()
        if users:
            return jsonify([user.json(0,2) for user in users])
        else:
            return {"status": 0, "data": {"msg": "type not found"}}
    else:
        return {"status": 0, "data": {"msg": "cannot read type"}}


@app.route("/register", methods=["POST"])
def register():
    uid = request.json.get("uid")
    uType = request.json.get("type")
    teleId = request.json.get("tid")
    if uid and uType and teleId:
        with open("users.csv", "r", encoding="cp1252") as file:
            csvfile = csv.reader(file, delimiter=",")
            csvfile = list(csvfile)
            existingUIds = [u[0] for u in csvfile]
            existingTeleIds = [u[2] for u in csvfile]
            if uid in existingUIds:
                return {"status": 0, "data": {"msg": "user id exists"}}
            if teleId in existingTeleIds:
                return {"status": 0, "data": {"msg": "tele id exists"}}
            else:
                with open("users.csv", "a", encoding="cp1252") as file:
                    file.write(uid+','+uType+','+teleId)
                    return {"status": 1, "data": "success"}
    else:
        return {"status": 0, "data": {"msg": "cannot read data"}}
