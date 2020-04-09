"""
Notification Microservice - Telegram Vendor Broker

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman, Low Louis
@team   - G3T4
"""

import os
import time
import json
import pika
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Vendor Broker...")

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

# BOT API KEY
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
MENU_FOOD_NAME       = os.environ['MENU_FOOD_NAME']

# LINE BREAK
LINE_BREAK = "%0A"
        
#############################
#    RABBITMQ CONNECTION    #
#############################

time.sleep(25)

count = 0

print("Attempting to connect to RabbitMQ Broker...")

while True:

    try:
        credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
        rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host         = HOST,
                                                                              port         = PORT,
                                                                             virtual_host = VIRTUAL_HOST,
                                                                             credentials  = credentials))
        channel = rabbit_connection.channel()
        channel.exchange_declare(exchange      = PRODUCER_EXCHANGE, 
                                 durable       = True, 
                                 exchange_type = 'direct' )

        channel.queue_declare(queue            = PRODUCER_QUEUE,
                              durable          = True)

        channel.queue_bind(queue               = PRODUCER_QUEUE,
                           exchange            = PRODUCER_EXCHANGE,  
                           routing_key         = PRODUCER_BINDING_KEY)
        print("Connection Successful")
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
        db_connection = engine.connect()
        metadata = db.MetaData()
        Telegram          = db.Table ("telegram",            metadata,
                            db.Column("update_id",           db.Integer(),    nullable=False, primary_key=True ),
                            db.Column("sender",              db.Integer(),    nullable=False,                  ),
                            db.Column("message_id",          db.Integer(),    nullable=False                   ),
                            db.Column("text",                db.String(1000), nullable=False                   ),
                            db.Column("reply_to_message_id", db.Integer(),    nullable=True,                   ))
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, primary_key=True    ),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True    ),
                            db.Column("food_id",             db.Integer(), nullable=False                       ),
                            db.Column("order_status",        db.String(80), nullable=False                      ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time() ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None        ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None       ))
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Vendor Listener has successfully started with no errors.")

############################
#     RABBITMQ PRODUCE     #
############################
def produce(msg):
    channel.basic_publish(exchange    = PRODUCER_EXCHANGE,
                          routing_key = PRODUCER_BINDING_KEY,
                          body        = msg,
                          properties  = pika.BasicProperties(delivery_mode = 2,
                                                             content_type  = 'application/json'))

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

###########################
#         GLOBALS         #
###########################

offset = None

############################
#         LISTENER         #
############################

while True:
    
    time.sleep(3)
    channel       = rabbit_connection.channel()
    db_connection = engine.connect()
    
    # CHECK IF THERE ARE NEW UPDATE ENTRIES
    if offset:
        query = db.select([Telegram]).where(Telegram.columns.update_id >= offset)
    else:
        query = db.select([Telegram])

    # RETRIEVE THE LATEST UPDATE
    ResultProxy = db_connection.execute(query)
    output = ResultProxy.fetchall()
    
    # RETRIEVE THE LATEST UPDATE
    if output:
        
        for result in output:
            
            update_id  = result[0]
            sender     = result[1]
            message_id = result[2]
            text       = result[3]
                    
            if all([update_id, sender, message_id, text]):
                        
                # CHECK IF MESSAGE IS ACCEPT ORDER
                if text == "Accept Order":
                    
                    print(f"Message Accept Order Found from sender {sender}")
                    print(f"Querying the database to find if the Vendor has pending orders...")
                    query = db.select([VendorMessenger]).where(VendorMessenger.columns.message_id==sender)
                    ResultProxy = db_connection.execute(query)
                    output = ResultProxy.fetchall()
                    
                    if output:
                        
                        order_id = output[0][0]
                        
                        print("Pending Order Found... Accepting...")
                        print("Sending Confirmation Message back to the Vendor...")
                        bot.send_message("You have accepted the Order.", sender)
                        print("Message successfully sent.")
                        
                        print("Notifying Order Processing of new Status...")
                        produce(json.dumps({"orderID"      : order_id,
                                            "delivererID"  : "0",
                                            "order_status" : "order ready"}))
                        print("Successfully sent the message through the broker...")
                        print("Deleting old entry from the database...")
                        query       = db.delete(VendorMessenger).where(VendorMessenger.columns.message_id==sender)
                        ResultProxy = db_connection.execute(query)
                        print("Successfully deleted the old entry from the database.")
                        
        else:
            offset = update_id + 1
            
############################
#         PUBLISHER        #
############################

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

        if messaging_timestamp == None or time.time() - messaging_timestamp >= 20:
            
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
                    bot.display_button(f"You have received a new order!{LINE_BREAK}The Order:{food_name}{LINE_BREAK}Will you accept?", chat_id)
                    print("Message successfully sent.")
                else:
                    print(f"Sending an overdue Order Notification to Vendor ID {vendor_id}...")
                    bot.display_button("You have pending orders. Please accept the order to proceed", chat_id)
              
                print("Updating the Database with the new Timestamp")  
                query       = db.update(VendorMessenger).values(messaging_timestamp=time.time(), 
                                                                message_id=chat_id).where(VendorMessenger.columns.order_id==order_id)
                ResultProxy = db_connection.execute(query)
                print("Update Successful...")
                
rabbit_connection.close()