"""
Notification Microservice - Driver Broker

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman, Low Louis
@team   - G3T4
"""

import os
import time
import json
import pika
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Driver Listener...")

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

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
CRM_USR_FROM_USRTYPE     = os.environ['CRM_USR_FROM_USRTYPE']
CRM_USR_FROM_CHATID      = os.environ['CRM_USR_FROM_CHATID']
MENU_GET_VENDOR_LOCATION = os.environ['MENU_GET_VENDOR_LOCATION']

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

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
        engine            = db.create_engine(os.environ['URI'])
        db_connection     = engine.connect()
        metadata          = db.MetaData()
        Telegram          = db.Table ("telegram",            metadata,
                            db.Column("update_id",           db.Integer(),    nullable=False, primary_key=True ),
                            db.Column("sender",              db.Integer(),    nullable=False,                  ),
                            db.Column("message_id",          db.Integer(),    nullable=False                   ),
                            db.Column("text",                db.String(1000), nullable=False                   ),
                            db.Column("reply_to_message_id", db.Integer(),    nullable=True,                   ))
        DriverOrder       = db.Table ("deliver_messenger",   metadata,
                            db.Column("order_id",            db.String(80),    nullable=False, primary_key=True    ),
                            db.Column("vendor_id",           db.String(80),    nullable=False,                     ),
                            db.Column("order_status",        db.String(80),    nullable=False                      ),
                            db.Column("delivery_address",    db.String(1000),  nullable=False                      ),
                            db.Column("timestamp",           db.Integer(),     nullable=False, default=time.time() ),
                            db.Column("messaging_timestamp", db.Integer(),     nullable=True,  default=None        ))
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Driver Listener has successfully started with no errors.")

############################
#     RABBITMQ PRODUCE     #
############################

def produce(msg):    
    channel.basic_publish(exchange         = PRODUCER_EXCHANGE,
                          routing_key      = PRODUCER_BINDING_KEY,
                          body             = msg,
                          properties       = pika.BasicProperties(delivery_mode = 2, 
                                                                  content_type  = "application/json"))

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
    
    if output:
        
        for result in output:
            
            update_id  = result[0]
            sender     = result[1]
            message_id = result[2]
            text       = result[3]
                    
            if all([update_id, sender, message_id, text]):
            # CHECK IF MESSAGE IS ACCEPT ORDER
                if text == "Accept":

                    print(f"Message Accept Found from sender {sender}")
                    print(f"Querying the database to find if there are orders to be delivered...")
                    query = db.select([DriverOrder]).limit(1)
                    ResultProxy = db_connection.execute(query)
                    output = ResultProxy.fetchall()
                    
                    # IF THERE IS A PENDING ORDER TO DELIVER IN THE DATABASE
                    if output:
                        
                        print("Order to be delivered found... Accepting...")
                        output = output[0]
                        orderID = output[0]
                        
                        print(f"Notifying the sender {sender} that he has accepted the order")
                        # SEND MESSAGE TO THE DRIVER WHO ACCEPTED
                        bot.send_message("You have accepted the Delivery Order.", sender)
                        
                        # QUERY CRM FOR ALL THE DRIVERS
                        response = json.loads(requests.post(CRM_USR_FROM_USRTYPE, json={"user_type": "driver"}).text)
                        
                        print("Notifying the other drivers that the order has been taken")
                        # NOTIFY EACH DRIVER IT HAS BEEN TAKEN BY OTHERS
                        for driver in response:
                            driver_chat_id = driver.get("chat_id")  
                            if driver_chat_id != sender:
                                bot.send_message("The order has been accepted by another driver", driver_chat_id)        
                        
                        
                        print("Obtaining DelivererID from CRM...")
                        # QUERY CRM TO OBTAIN DRIVER USERNAME
                        response = json.loads(requests.post(CRM_USR_FROM_CHATID, json={"tid": sender}).text)
                        delivererID = response.get("username")
                        print(f"Successfully obtained DelivererID: {delivererID}")
                        
                        
                        print("Notifying Order Processing of new Status...")
                        # RABBITMQ TOWARDS ORDER PROCESSING
                        produce(json.dumps({"orderID"      : orderID,
                                            "delivererID"  : response.get("username"),
                                            "order_status" : "completed"}))
                        print("Successfully sent the message through the broker...")
                        print("Deleting old entry from the database...")
                        # DELETE THE DATABASE ENTRY
                        query = db.delete(DriverOrder).where(DriverOrder.columns.order_id==output[0])
                        ResultProxy = db_connection.execute(query)
                        print("Successfully deleted the old entry from the database.")
        else:
            offset = update_id + 1
            
############################
#         PUBLISHER        #
############################

    # OBTAIN PENDING ORDER FROM THE DATABASE
    query       = db.select([DriverOrder]).limit(1)
    ResultProxy = db_connection.execute(query) 
    order       = ResultProxy.fetchall()
    
    if order:
        
        order_id            = order[0][0]
        vendor_id           = order[0][1]
        delivery_location   = order[0][3]
        messaging_timestamp = order[0][5]
    
        # REPUBLISH AFTER 20 SECONDS
        if messaging_timestamp == None or time.time() - messaging_timestamp >= 20:
            
            print(f"""
                Found an pending delivery, Details: 
                Order ID          : {order_id}
                Delivery Location : {delivery_location}
                """)
    
            print("Obtaining Deliverery Collection from Menu...")
            vendor_location = json.loads(requests.post(MENU_GET_VENDOR_LOCATION, json={"vendor_email": vendor_id}).text)
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
                        bot.display_button(f"You have received a new order! Will you accept?", driver_chat_id)
                        bot.send_message(f"Collect at: {vendor_location}", driver_chat_id)
                        bot.send_message(f"Deliver to: {delivery_location}", driver_chat_id)
                    
                    else:
                        print("Overdue order to be delivered has been found sending...")
                        bot.display_button(f"You have an outstanding order. Will you accept?", driver_chat_id)
                        bot.send_message(f"Collect at: {vendor_location}", driver_chat_id)
                        bot.send_message(f"Deliver to {delivery_location}", driver_chat_id)
            
            print("Updating the Database with the new Timestamp")
            query = db.update(DriverOrder).values(messaging_timestamp=time.time()).where(DriverOrder.columns.order_id==order_id)
            ResultProxy = db_connection.execute(query)
            print("Update Successful...")

rabbit_connection.close()