import os
import time
import json
import pika
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

API_KEY = os.environ['API_KEY']

# Constants to consume (receive) from ORDER PROCESSING
PRODUCER_EXCHANGE     = os.environ['PRODUCER_EXCHANGE']
PRODUCER_QUEUE        = os.environ['PRODUCER_QUEUE']
PRODUCER_BINDING_KEY  = os.environ['PRODUCER_BINDING_KEY']

# Credentials
RABBIT_USERNAME = os.environ['RABBIT_USERNAME']
RABBIT_PASSWORD = os.environ['RABBIT_PASSWORD']
HOST            = os.environ['HOST']
PORT            = os.environ['PORT']
VIRTUAL_HOST    = os.environ['VIRTUAL_HOST']

# URLS
CRM_USR_FROM_USRNAME = os.environ['CRM_USR_FROM_USRNAME']
CRM_USR_FROM_USRTYPE = os.environ['CRM_USR_FROM_USRTYPE']

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

#############################
#    RABBITMQ CONNECTION    #
#############################

count = 0

while True:

    try:
        print("Attempting to connect to RabbitMQ Broker...")
        credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host        = HOST,
                                                                       port         = PORT,
                                                                       virtual_host = VIRTUAL_HOST,
                                                                       credentials  = credentials))
        channel = connection.channel()
        print("Connection Successful!")
        break

    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s... Number of tries: {count}")
        time.sleep(3)
        
#############################
#    DATABASE CONNECTION    #
#############################     

count = 0

print("Attempting to connect to the Database...")

while True:
    
    try:
        engine = db.create_engine(os.environ['URI'])
        connection = engine.connect()
        metadata = db.MetaData()
        vendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                         ))
        
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

############################
#      SCHEDULER INIT      #
############################

s   = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(3,1,vendor_publish, ())
    s.run()

############################
#         LISTENER         #
############################

# globals
update_id = None
first     = True

def vendor_listen():
    
    global first
    global update_id

    updates = bot.get_updates(offset=update_id)["result"]

    if first:
        if updates:
            first     = False
            update_id = updates[-1]["update_id"] + 1
            updates   = bot.get_updates(offset=update_id)["result"]    


def vendor_publish():
    query = db.select([VendorMessenger]).group_by(VendorMessenger.columns.vendor_id)
    ResultProxy = connection.execute(query)   
    
    for vendor in ResultProxy.fetchall():

        vendor_id, messaging_timestamp = vendor[1], vendor[-1]

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 10:

            response = requests.post(CRM_USERNAME_GET, json={"username": vendor_email})
            chat_id = json.loads(response.text).get("chat_id")

            if chat_id != None:
                if messaging_timestamp == None:
                    bot.display_button("You have received a new order! Will you accept?", chat_id)
                else:
                    bot.display_button("You have pending orders. Please accept the order to proceed", chat_id)
                
                query = db.update(VendorMessenger).values(messaging_timestamp=time.time()).where(VendorMessenger.columns.order_id==order_id)
                ResultProxy = connection.execute(query)

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

