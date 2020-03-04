from model.base import db

class Vendor(db.Model):
    vendor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_name = db.Column(db.String(80), nullable=False)
    halal = db.Column(db.Boolean, nullable=False)
    # We point to the Food class
    menu_foods = db.relationship("Food", backref="Vendor", lazy=True)
    
    def __init__(self,vendor_name,halal):
        self.vendor_name = vendor_name
        self.halal = halal
    
    def __str__(self):
        return dir(self)

class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String(80), nullable=False)
    food_description = db.Column(db.Text, nullable=True)
    food_price = db.Column(db.Float(precision=2), nullable=False)
    # Vendor can take item off an order
    availability = db.Column(db.Boolean, nullable=False, default=True)
    # Vendor deletes the item off the menu
    listed = db.Column(db.Boolean, nullable=False, default=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey(Vendor.vendor_id), nullable=False)
    
    def __init__(self,vendor_id,food_name,food_description,food_price):
        self.vendor_id = vendor_id
        self.food_name = food_name
        self.food_description = food_description
        self.food_price = food_price
        
    def __str__(self):
        return dir(self)
    

    
    