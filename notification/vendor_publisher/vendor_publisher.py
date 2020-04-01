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
CRM_USR_FROM_USRNAME  = os.environ['CRM_USR_FROM_USRNAME']

#############################
#    DATABASE CONNECTION    #
#############################

time.sleep(25)

print("Attempting to connect to the database")

count = 0

while True:
    
    try:
        engine     = db.create_engine(os.environ['URI'])
        connection = engine.connect()
        metadata   = db.MetaData()
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        count += 1
        print(f"Connection Failed, retrying in 3s, tries: {count}")
        time.sleep(3)

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#      SCHEDULER INIT       #
#############################

s = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(10,1,vendor_publish, ())
    s.run()

def vendor_publish():
    
    while True:
        try:
            engine     = db.create_engine(os.environ['URI'])
            connection = engine.connect()
            metadata   = db.MetaData()
            VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                                db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                                db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
            metadata.create_all(engine)
            break
        except:
            print(f"Connection Lost, retrying in 3s...")
            time.sleep(3)
    
    query       = db.select([VendorMessenger.columns.order_id,
                             VendorMessenger.columns.vendor_id,
                             db.func.min(VendorMessenger.columns.messaging_timestamp)]).group_by(VendorMessenger.columns.vendor_id)
    ResultProxy = connection.execute(query)   
    
    output = ResultProxy.fetchall()
    
    for vendor in output:

        vendor_id, order_id, messaging_timestamp = vendor[1], vendor[0], vendor[-1]

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 12:

            response = requests.post(CRM_USR_FROM_USRNAME, json={"username": vendor_id})
            chat_id  = json.loads(response.text).get("chat_id")

            if chat_id != None:
                if messaging_timestamp == None:
                    bot.display_button("You have received a new order! Will you accept?", "Accept Order", chat_id)
                    time.sleep(1)
                else:
                    bot.display_button("You have pending orders. Please accept the order to proceed", "Accept Order", chat_id)
                    time.sleep(1)
                
                query       = db.update(VendorMessenger).values(messaging_timestamp=time.time(), message_id=chat_id).where(VendorMessenger.columns.order_id==order_id)
                ResultProxy = connection.execute(query)

while True:
    scheduler()

