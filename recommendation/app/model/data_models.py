"""
Data Models - CRM Microservice

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@team   - G3T4
"""

from .base import db

class User(db.Model):
    username  = db.Column(db.String(80), primary_key=True)
    vendor  = db.Column(db.String(80), primary_key=True)
    menu = db.Column(db.Integer, nullable=False)  # list of food ids 
    
    def __init__(self,username,user_type,chat_id = None):
        self.username     = username
        self.vendor    = vendor
        self.menu     = menu
        
    def directory(self):
        return [
            ("username"  , self.username),
            ("vendor" , self.vendor),
            ("menu"   , self.menu),         
        ]
    
    def json(self,*args):
        output = []
        values = self.directory()
        for key in args:
            output.append(values[key])
        return dict(output)