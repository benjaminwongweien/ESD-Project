"""
Data Models - Menu Microservice

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@team   - G3T4
"""

from .base import db

class Vendor(db.Model):
    vendor_id          = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    vendor_name        = db.Column(db.String(80), nullable=False)
    vendor_email       = db.Column(db.String(80), nullable=False)
    vendor_description = db.Column(db.Text,       nullable=True )
    vendor_location    = db.Column(db.String(80), nullable=False)
    vendor_image       = db.Column(db.String(80), nullable=True )
    menu_foods         = db.relationship("Food",  backref="Vendor", lazy=True)
    
    def __init__(self,vendor_name,vendor_email,vendor_description,vendor_location,vendor_image=None):
        self.vendor_name        = vendor_name
        self.vendor_email       = vendor_email
        self.vendor_description = vendor_description
        self.vendor_location    = vendor_location
        self.vendor_image       = vendor_image
        
    def directory(self):
        return [
            ("vendor_id"         , self.vendor_id),
            ("vendor_name"       , self.vendor_name),
            ("vendor_email"      , self.vendor_email),
            ("vendor_description", self.vendor_description),
            ("vendor_location"   , self.vendor_location),
            ("vendor_image"      , self.vendor_image)            
        ]
    
    def json(self,*args):
        output = []
        values = self.directory()
        for key in args:
            output.append(values[key])
        return dict(output)
    
class Food(db.Model):
    vendor_id        = db.Column(db.Integer, db.ForeignKey(Vendor.vendor_id), primary_key=True)
    food_id          = db.Column(db.Integer,            primary_key=True, autoincrement=True)
    food_name        = db.Column(db.String(80),         nullable=False)
    food_description = db.Column(db.Text,               nullable=True )
    food_image       = db.Column(db.String(80),         nullable=True )
    food_price       = db.Column(db.Float(precision=2), nullable=False)
    food_label       = db.Column(db.String(80),         nullable=True )
    availability     = db.Column(db.Boolean,            nullable=False,   default=True) # take item off an order
    listed           = db.Column(db.Boolean,            nullable=False,   default=True) # take item off the menu
    
    def __init__(self,vendor_id,food_name,food_description,food_price,food_label=None,food_image=None):
        self.vendor_id        = vendor_id
        self.food_name        = food_name
        self.food_description = food_description
        self.food_image       = food_image
        self.food_price       = food_price
        self.food_label       = food_label

    def directory(self):
        return [
            ("vendor_id"        , self.vendor_id),
            ("food_id"          , self.food_id),
            ("food_name"        , self.food_name),
            ("food_description" , self.food_description),
            ("food_image"       , self.food_image),
            ("food_price"       , self.food_price), 
            ("food_label"       , self.food_label), 
            ("availability"     , self.availability), 
            ("listed"           , self.listed),            
        ]
    
    def json(self,*args):
        output = []
        values = self.directory()
        for key in args:
            output.append(values[key])
        return dict(output)   
        
    