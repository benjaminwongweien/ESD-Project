import os
import time
import json
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

API_KEY           = os.environ['API_KEY'] 
CRM_USERNAME_GET  = os.environ['CRM_USERNAME_GET']
MENU_GET_EMAIL    = os.environ['MENU_GET_EMAIL']

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#      SCHEDULER INIT       #
#############################

s = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(3,1,vendor_publish, ())
    s.run()

def vendor_publish():
    
    while True:
        try:
            engine     = db.create_engine(os.environ['URI'])
            connection = engine.connect()
            metadata   = db.MetaData()
            VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                                db.Column("order_id",            db.Integer(),  nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                                db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
            metadata.create_all(engine)
            break
        except:
            tries += 1
            print(f"Connection Lost, retrying in 3s...")
            time.sleep(3)
    
    query       = db.select([VendorMessenger]).group_by(VendorMessenger.columns.vendor_id)
    ResultProxy = connection.execute(query)   
    
    output = ResultProxy.fetchall()
    
    for vendor in output:
        print(vendor)
        vendor_id, order_id, messaging_timestamp = vendor[1], vendor[0], vendor[-2]

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 10:

            response = requests.post(CRM_USERNAME_GET, json={"username": vendor_id})
            chat_id  = json.loads(response.text).get("chat_id")

            if chat_id != None:
                if messaging_timestamp == None:
                    bot.display_button("You have received a new order! Will you accept?", "Accept Order", chat_id)
                else:
                    bot.display_button("You have pending orders. Please accept the order to proceed", "Accept Order", chat_id)
                
                query       = db.update(VendorMessenger).values(messaging_timestamp=time.time(), message_id=chat_id).where(VendorMessenger.columns.order_id==order_id)
                ResultProxy = connection.execute(query)

#############################
#    DATABASE CONNECTION    #
#############################

tries = 0

while True:
    print("Attempting to connect to the database")
    try:
        engine     = db.create_engine(os.environ['URI'])
        connection = engine.connect()
        metadata   = db.MetaData()
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.Integer(),  nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        tries += 1
        print(f"Connection Failed, retrying in 3s, tries: {tries}")
        time.sleep(3)

while True:
    scheduler()

