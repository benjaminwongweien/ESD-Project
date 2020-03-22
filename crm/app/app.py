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

# get the user info using chatId
@app.route("/chatId", methods=["POST"])
def chatId():
    chat_id = request.args.get("chatId")
    if chat_id:
        with open("users.csv", "r", encoding="cp1252") as file:
            csvfile = csv.reader(file, delimiter=",")
            csvfile = list(csvfile)
            for user in csvfile:
                if user[2] == chat_id:
                    return {"status": 1, "data": {"uid": user[0], "user_type": user[1]}}
        return {"status": 0, "data": {"msg": "user not found"}}
    else:
        return {"status": 0, "data": {"msg": "cannot read chat_id"}}

# get user information using userId
@app.route("/userId", methods=["POST"])
def userId():
    if uid:
        with open("users.csv", "r", encoding="cp1252") as file:
            csvfile = csv.reader(file, delimiter=",")
            csvfile = list(csvfile)
            for user in csvfile:
                if user[0] == uid:
                    return {
                        "status": 1,
                        "data": {"chat_id": user[2], "user_type": user[1]},
                    }
        return {"status": 0, "data": {"msg": "user not found"}}
    else:
        return {"status": 0, "data": {"msg": "cannot read uid"}}

# get all user and info by usertype
@app.route("/type", methods=["POST"])
def uType():
    uType = request.args.get("type")
    if uType:
        with open("users.csv", "r", encoding="cp1252") as file:
            csvfile = csv.reader(file, delimiter=",")
            csvfile = list(csvfile)
            users = [{"uid": u[0], "chatId": u[2]}
                     for u in csvfile if u[1] == uType]
            userString = json.loads(json.dumps(users))
            return {"status": 1, "data": userString}
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


if __name__ == "__main__":
    app.run()
