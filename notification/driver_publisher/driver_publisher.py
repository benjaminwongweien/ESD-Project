import os
import time
import json
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Driver Publisher...")

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

# URLS
CRM_USR_FROM_USRTYPE     = os.environ['CRM_USR_FROM_USRTYPE']
MENU_GET_VENDOR_LOCATION = os.environ['MENU_GET_VENDOR_LOCATION']

# HEXADECIMAL CHAT CONSTANTS
LINE_BREAK = "%0A"

#############################
#    DATABASE CONNECTION    #
#############################   

time.sleep(25)

count = 0

print("Attempting to connect to the Database...")

while True:
    try:
        engine            = db.create_engine(os.environ['URI'])
        connection        = engine.connect()
        metadata          = db.MetaData()
        DriverOrder   = db.Table ("deliver_messenger",    metadata,
                        db.Column("order_id",            db.String(80),    nullable=False, autoincrement=False , primary_key=True),
                        db.Column("vendor_id",           db.String(80),    nullable=False, primary_key=True                      ),
                        db.Column("order_status",        db.String(80),    nullable=False                                        ),
                        db.Column("delivery_address",    db.String(1000), nullable=False                                         ),
                        db.Column("timestamp",           db.Integer(),     nullable=False, default=time.time()                   ),
                        db.Column("messaging_timestamp", db.Integer(),     nullable=True,  default=None                          ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Driver Publisher has successfull started with no errors.")

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#      SCHEDULER INIT       #
#############################

s   = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(10,1,driver_publish, ())
    s.run()

#############################
#         PUBLISHER         #
#############################

def driver_publish():
    while True:
        try:
            engine            = db.create_engine(os.environ['URI'])
            connection        = engine.connect()
            metadata          = db.MetaData()
            DriverOrder       = db.Table ("deliver_messenger",    metadata,
                                db.Column("order_id",            db.String(80),    nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80),    nullable=False, primary_key=True                      ),
                                db.Column("order_status",        db.String(80),    nullable=False                                        ),
                                db.Column("delivery_address",    db.String(1000), nullable=False                                         ),
                                db.Column("timestamp",           db.Integer(),     nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),     nullable=True,  default=None                          ))
            metadata.create_all(engine)
            break
        except:
            print("Connection Lost, Attempting to Reconnect in 3s...")
            time.sleep(3)

    # OBTAIN PENDING ORDER FROM THE DATABASE
    query       = db.select([DriverOrder]).limit(1)
    ResultProxy = connection.execute(query)   
    
    # IF THERE IS AN ORDER (ELSE EMPTY LIST)
    if order := ResultProxy.fetchall()[0]: 
        
        order_id            = order[0]
        messaging_timestamp = order[-1]
        delivery_location   = order[3]

        

        # REPUBLISH AFTER 10 SECONDS
        if messaging_timestamp == None or time.time() - messaging_timestamp >= 12:
            
            print(f"""
                Found an pending delivery, Details: 
                Order ID          : {order_id}
                Delivery Location : {delivery_location}
                """)
            
            print("Obtaining Deliverery Collection from Menu...")
            vendor_location = json.loads(requests.post(MENU_GET_VENDOR_LOCATION, json={"vendor_email": order[1]}).text)
            vendor_location = vendor_location.get("vendor_location",{})
            vendor_location = vendor_location.get("vendor_location")
            print(f"Successfully obtained Vendor Location {vendor_location}")
            
            print("Obtaining Deliverer ChatIDs from CRM...")
            response = json.loads(requests.post(CRM_USR_FROM_USRTYPE, json={"user_type": "driver"}).text)
            print(f"Successfully obtained Deliver ChatIDs")
            
            for driver in response:
                driver_chat_id = driver.get("chat_id")
                
                if driver_chat_id != None:
                    if messaging_timestamp == None:
                        
                        print("Order to be delivered has been found sending...")
                        bot.display_button(f"You have received a new order! Will you accept?{LINE_BREAK}Please collect the order at: {vendor_location}{LINE_BREAK}Please deliver the order to{delivery_location}", driver_chat_id)
                    
                    else:
                        print("Overdue order to be delivered has been found sending...")
                        bot.display_button(f"You have an outstanding order. Will you accept?{LINE_BREAK}Please collect the order at: {vendor_location}{LINE_BREAK}Please deliver the order to{delivery_location}", driver_chat_id)
            
            print("Updating the Database with the new Timestamp")
            query       = db.update(DriverOrder).values(messaging_timestamp=time.time()).where(DriverOrder.columns.order_id==order_id)
            ResultProxy = connection.execute(query)
            print("Update Successful...")

###########################
#          START          #
###########################

while True:
    try:
        scheduler()
    except:
        print("An unexpected error occured, retrying in 3 seconds")
        time.sleep(3)

