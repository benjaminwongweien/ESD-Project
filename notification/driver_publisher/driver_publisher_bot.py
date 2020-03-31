import os
import time
import json
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY            = os.environ['API_KEY'] 
CRM_USERTYPE_GET   = os.environ['CRM_USERTYPE_GET']

bot = telegram_chatbot(API_KEY)

s   = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(3,1,driver_publish, ())
    s.run()

def driver_publish():
    query = db.select([DriverOrder])
    ResultProxy = connection.execute(query)   
    
    for order in ResultProxy.fetchall():

        order_id, messaging_timestamp = order[0], order[-1]

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 10:

            response = requests.post(CRM_USERTYPE_GET, json={"user_type": "driver"}) 
            response = requests.post(CRM_USERTYPE_GET, json={"user_type": 0}) 
            
            for driver in response:
                driver_chat_id = json.loads(response.text).get("chat_id")
                
                if driver_chat_id != None:
                    if messaging_timestamp == None:
                        bot.display_button("You have received a new order! Will you accept?", driver_chat_id)
                    
                else:
                    bot.display_button("You have pending orders. Please accept the order to proceed", driver_chat_id)
                
            query = db.update(DriverOrder).values(messaging_timestamp=time.time()).where(DriverOrder.columns.order_id==order_id)
            ResultProxy = connection.execute(query)

tries = 0

while True:
    print("Attempting to connect to the database")
    try:
        engine            = db.create_engine(os.environ['URI'])
        connection        = engine.connect()
        metadata          = db.MetaData()
        DriverOrder       = db.Table ("driver_order",        metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                         ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        tries += 1
        print(f"Connection Failed, retrying in 3s, tries: {tries}")
        time.sleep(3)

while True:
    scheduler()

