##!/usr/bin/python

"""
Menu Microservice
@Author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman
@Team   - G3T4
"""
import os
from flask import Flask
from model.base import db
from model.data_models import Vendor, Food

def create_app(user,ip,port,dbname,password=""):
  
  """
  Creates and starts the App with all the required settings
  mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
  """
  
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{password}@{ip}:{port}/{dbname}"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  return app

app = create_app(os.environ['USER'],os.environ['IP'],os.environ['PORT'],os.environ['DBNAME'])
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
app.app_context().push()

Hello = Vendor("Ben",True)
db.session.add(Hello)
db.session.commit()

# add other db stuff here flask app shld kinda be ready hope so XD
