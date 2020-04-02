import os
import time
import json
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Vendor Publisher...")

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
CRM_USR_FROM_USRNAME  = os.environ['CRM_USR_FROM_USRNAME']
MENU_FOOD_NAME        = os.environ['MENU_FOOD_NAME']

# HEXADECIMAL CHAT CONSTANTS
LINE_BREAK = "%0A"

#############################
#    DATABASE CONNECTION    #
#############################

time.sleep(25)

print("Attempting to connect to the Database...")

count = 0

while True:
    
    try:
        engine     = db.create_engine(os.environ['URI'])
        db_connection = engine.connect()
        metadata   = db.MetaData()
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("food_id",             db.Integer(), nullable=False                                         ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Vendor Publisher has successfull started with no errors.")

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
            db_connection = engine.connect()
            metadata   = db.MetaData()
            VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                                db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("food_id",              db.Integer(), nullable=False                                       ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                                db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
            metadata.create_all(engine)
            break
        except:
            print("Connection Lost, Attempting to Reconnect in 3s...")
            time.sleep(3)
    
    query       = db.select([VendorMessenger.columns.order_id,
                             VendorMessenger.columns.vendor_id,
                             VendorMessenger.columns.food_id,
                             db.func.min(VendorMessenger.columns.messaging_timestamp)]).group_by(VendorMessenger.columns.vendor_id)
    ResultProxy = db_connection.execute(query)    
    output = ResultProxy.fetchall()
    
    for vendor in output:
        
        order_id            = vendor[0]
        vendor_id           = vendor[1]
        food_id             = vendor[2]
        messaging_timestamp = vendor[-1]

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 12:
            
            print(f"""
                Found an pending order, Details: 
                Order ID        : {order_id}
                Vendor ID       : {vendor_id}
                Food ID         : {food_id}
                """)
            
            print("Obtaining Vendor ChatID from CRM...")
            response = requests.post(CRM_USR_FROM_USRNAME, json={"username": vendor_id})
            chat_id  = json.loads(response.text).get("chat_id")
            print(f"Successfully obtained Vendor ChatID: {chat_id}")
            
            print("Obtaining Food Name from Menu...")
            food_name = requests.post(MENU_FOOD_NAME, json={"food_id": food_id})
            food_name = json.loads(food_name.text).get("food",{}).get("food_name")
            print(f"Successfully obtained Food Name: {food_name}")

            if chat_id != None and food_name != None:
                if messaging_timestamp == None:
                    print(f"Sending a new Order Notification to Vendor ID {vendor_id}...")
                    bot.display_button(f"You have received a new order!{LINE_BREAK}The Order:{food_name}{LINE_BREAK}Will you accept?", "Accept Order", chat_id)
                    time.sleep(1)
                    print("Message successfully sent.")
                else:
                    print(f"Sending an overdue Order Notification to Vendor ID {vendor_id}...")
                    bot.display_button("You have pending orders. Please accept the order to proceed", "Accept Order", chat_id)
                    time.sleep(1)
              
                print("Updating the Database with the new Timestamp")  
                query       = db.update(VendorMessenger).values(messaging_timestamp=time.time(), 
                                                                message_id=chat_id).where(VendorMessenger.columns.order_id==order_id)
                ResultProxy = db_connection.execute(query)
                print("Update Successful...")
# START
while True:
    scheduler()

