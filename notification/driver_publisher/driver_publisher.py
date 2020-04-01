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

# URLS
CRM_USR_FROM_USRTYPE = os.environ['CRM_USR_FROM_USRTYPE']

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

#############################
#    DATABASE CONNECTION    #
#############################   

time.sleep(25)

count = 0

print("Attempting to connect to the database...")

while True:
    try:
        engine            = db.create_engine(os.environ['URI'])
        connection        = engine.connect()
        metadata          = db.MetaData()
        DriverOrder       = db.Table ("deliver_messenger",        metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                         ))
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
            DriverOrder       = db.Table ("deliver_messenger",  metadata,
                                db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                         ))
            metadata.create_all(engine)
            break
        except:
            print(f"Connection Lost, retrying in 3s...")
            time.sleep(3)

    # OBTAIN PENDING ORDER FROM THE DATABASE
    query       = db.select([DriverOrder]).limit(1)
    ResultProxy = connection.execute(query)   
    order       = ResultProxy.fetchall()
    
    # IF THERE IS AN ORDER (ELSE EMPTY LIST)
    if order: 
        order = order[0]
        order_id, messaging_timestamp = order[0], order[-1]

        # REPUBLISH AFTER 10 SECONDS
        if messaging_timestamp == None or time.time() - messaging_timestamp >= 12:

            response = json.loads(requests.post(CRM_USR_FROM_USRTYPE, json={"user_type": "driver"}).text)
            
            for driver in response:
                driver_chat_id = driver.get("chat_id")
                
                
                if driver_chat_id != None:
                    if messaging_timestamp == None:
                        print("Order to be delivered has been found sending...")
                        bot.display_button("You have received a new order! Will you accept?", driver_chat_id)
                    
                    else:
                        print("Overdue order to be delivered has been found sending...")
                        bot.display_button("You have pending orders. Please accept the order to proceed", driver_chat_id)
                
            query       = db.update(DriverOrder).values(messaging_timestamp=time.time()).where(DriverOrder.columns.order_id==order_id)
            ResultProxy = connection.execute(query)

###########################
#          START          #
###########################

while True:
    scheduler()

