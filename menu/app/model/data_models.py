##!/usr/bin/python

"""
Menu Microservice Data Models
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
from .base import db

class Vendor(db.Model):
    vendor_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_name     = db.Column(db.String(80), nullable=False)
    halal           = db.Column(db.Boolean, nullable=False)
    # We point to the Food class
    menu_foods      = db.relationship("Food", backref="Vendor", lazy=True)
    
    def __init__(self,vendor_name,halal):
        self.vendor_name = vendor_name
        self.halal       = halal
    
    def json_basic(self):
        return {"vendor_id":   self.vendor_id,
                "vendor_name": self.vendor_name}        
    
    def json_full(self):
        return {"vendor_id":   self.vendor_id,
                "vendor_name": self.vendor_name,
                "halal":       self.halal}

class Food(db.Model):
    vendor_id        = db.Column(db.Integer, db.ForeignKey(Vendor.vendor_id), primary_key=True)
    food_id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name        = db.Column(db.String(80), nullable=False)
    food_description = db.Column(db.Text, nullable=True)
    food_price       = db.Column(db.Float(precision=2), nullable=False)
    # Vendor can take item off an order
    availability     = db.Column(db.Boolean, nullable=False, default=True)
    # Vendor deletes the item off the menu
    listed           = db.Column(db.Boolean, nullable=False, default=True)
    
    def __init__(self,vendor_id,food_name,food_description,food_price):
        self.vendor_id        = vendor_id
        self.food_name        = food_name
        self.food_description = food_description
        self.food_price       = food_price
    
    def json_default(self):
        return {"food_id":          self.food_id,
                "food_name":        self.food_name,
                "food_description": self.food_description,
                "food_price":       self.food_price}    
    
    def json_basic(self):
        return {"food_id":          self.food_id,
                "food_name":        self.food_name}     
    
    def json_full(self):
        return {"vendor_id":        self.vendor_id,
                "food_id":          self.food_id,
                "food_name":        self.food_name,
                "food_description": self.food_description,
                "food_price":       self.food_price,
                "availability":     self.availability,
                "listed":           self.listed}
        
    

    
    