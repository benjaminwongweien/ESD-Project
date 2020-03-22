"""
Menu Microservice
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import random

globals = {}
dummy_address = {'lat': 1.2, 'lng': 103}
dummy_history = []


def create_app():
    """
    Creates and starts the App with all the required settings
    """
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
    return globals['vendors']


@app.route("/recommendation", methods=["GET"])
def recommendation():
    # uncomment when order api is working
    uid = request.args.get('uid')
    if uid == None:
        return random.choice(globals['vendors']) 
    order_url = "http://localhost:8080/order/history/customer"
    order_hist_request = requests.post(url=order_url, json={"userid": uid})
    order_hist_data = order_hist_request.json()
    order_hist_data = [
        {'orderID': 1, 'vendorID': 2, 'delivererID': 1, 'foodID': 30, 'quantity': 10,
            'checkoutID': '21232323432', 'customerId': 1001, 'status': '1', 'address': '81 Victoria St, Singapore 188065'},
        {'orderID': 1, 'vendorID': 2, 'delivererID': 1, 'foodID': 30, 'quantity': 10,
            'checkoutID': '21232323432', 'customerId': 1001, 'status': '1', 'address': '81 Victoria St, Singapore 188065'}
    ]
    address_list = [o['address'] for o in order_hist_data]
    top_address = max(set(address_list), key=address_list.count)
    gmap_params = {
        'address': top_address,
        'key': 'AIzaSyBVt4jAsStVZQSezuy8v-ydY-08HfTiBz4'
    }
    gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    gmap_request = requests.get(url=gmap_url, params=gmap_params)
    gmap_data = gmap_request.json()
    user_position = gmap_data['results'][0]['geometry']['location']
    closest_vendor = {}
    closest_dist = 999
    for vendor in globals['vendors']:
        dist = ((user_position['lat'] - vendor['position']['lat']) ** 2 +
                (user_position['lng'] - vendor['position']['lng']) ** 2) ** 0.5
        if dist < closest_dist:
            closest_dist = dist
            closest_vendor = vendor
    return str(closest_vendor)


@app.before_first_request
def before_first_request_func():
    # uncomment if menu api is working
    # menu_url = "http://localhost/all_vendor"
    # menu_request = requests.get(url=menu_url)
    # vendors = menu_request.json()['vendors']

    vendors = [
        {'vendor_location': '68 Orchard Rd, Plaza Singapura, #B1-21/22, Singapore 238839'},
        {'vendor_location': '52 Li Hwan Terrace, Singapore 556980'},
        {'vendor_location': 'Raffles Institution Boarding, 1 Raffles Lane, 575954'},
    ]

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


if __name__ == '__main__':
    app.run(port=5001)
