"""
Recommendation Microservice

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@team   - G3T4
"""

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import random

# list of addresses for all vendors before first request
globals = {}
# hardcoded
dummy_address = {'lat': 1.2, 'lng': 103}
dummy_history = []


def create_app():
    """ Creates and starts the App with all the required settings """
    app = Flask(__name__)
    CORS(app)
    # app.config['SQLALCHEMY_DATABASE_URI'] = uri
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


# app=create_app("mysql+mysqlconnector://root:@127.0.0.1:3306/menu")
app = create_app()
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
                    "error": e.description}), e.code


@app.route("/vendor_pos", methods=["GET"])
def vendor_pos():
    return jsonify(globals['vendors'])


@app.route("/all", methods=["GET"])
def all():
    order_url = "http://localhost:8080/order/all"
    order_hist_request = requests.get(
        url=order_url
        # json={"customerID": username}
    )
    order_hist_data = order_hist_request.json()
    return(str(order_hist_data))


@app.route("/recommendation", methods=["GET"])
def recommendation():
    # uncomment when order api is working
    # get the username from the UI
    username = request.args.get('username')
    closest_vendor = {}
    if username == None:
        closest_vendor = random.choice(globals['vendors'])
    else:
        order_url = "http://localhost:8080/order/all"
        order_hist_request = requests.get(url=order_url)
        order_hist_data = order_hist_request.json()
        address = [o['delivery_address']
                   for o in order_hist_data if o['customerID'] == username][0]

        # order_hist_data hardcoded:
        # order_hist_data = [
        #     {'orderID': 1, 'vendorID': 2, 'delivererID': 1, 'foodID': 30, 'quantity': 10,
        #         'checkoutID': '21232323432', 'customerId': 1001, 'status': '1', 'address': '81 Victoria St, Singapore 188065'},
        #     {'orderID': 1, 'vendorID': 2, 'delivererID': 1, 'foodID': 30, 'quantity': 10,
        #         'checkoutID': '21232323432', 'customerId': 1001, 'status': '1', 'address': '81 Victoria St, Singapore 188065'}
        # ]

        # address_list = [o['address'] for o in order_hist_data]
        # top_address = max(set(address_list), key=address_list.count)
        gmap_params = {
            'address': address,
            'key': 'AIzaSyBVt4jAsStVZQSezuy8v-ydY-08HfTiBz4'
        }

        # request from google API
        gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        gmap_request = requests.get(url=gmap_url, params=gmap_params)
        gmap_data = gmap_request.json()
        user_position = gmap_data['results'][0]['geometry']['location']

        closest_dist = 999
        for vendor in globals['vendors']:
            dist = ((user_position['lat'] - vendor['position']['lat']) ** 2 +
                    (user_position['lng'] - vendor['position']['lng']) ** 2) ** 0.5
            if dist < closest_dist:
                closest_dist = dist
                closest_vendor = vendor
    vendor_id = closest_vendor['vendor_id']
    food_list = [f for f in globals['food'] if f['vendor_id'] == vendor_id]
    return {'food_list': str(food_list)}


@app.before_first_request
def before_first_request_func():
    # prepare vendor
    menu_url = "http://localhost:85/all_vendor"
    menu_request = requests.get(url=menu_url)
    vendors = menu_request.json()['vendors']

    for i, vendor in enumerate(vendors):
        location = vendor['vendor_location']
        gmap_params = {
            'address': location,
            'key': 'AIzaSyBVt4jAsStVZQSezuy8v-ydY-08HfTiBz4'
        }
        gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        gmap_request = requests.get(url=gmap_url, params=gmap_params)
        gmap_data = gmap_request.json()
        position = gmap_data['results'][0]['geometry']['location']
        vendors[i]['position'] = position
    globals['vendors'] = vendors

    # prepare food
    menu_url = "http://localhost:85/all_food"
    menu_request = requests.get(url=menu_url)
    food = menu_request.json()['food']
    globals['food'] = food

    

