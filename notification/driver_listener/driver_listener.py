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
CRM_USR_FROM_CHATID  = os.environ['CRM_USR_FROM_CHATID']

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

#############################
#    RABBITMQ CONNECTION    #
#############################

time.sleep(30)

count = 0

print("Attempting to connect to RabbitMQ Broker...")

while True:
    try:
        credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host         = HOST,
                                                                       port         = PORT,
                                                                       virtual_host = VIRTUAL_HOST,
                                                                       credentials  = credentials))
        channel = connection.channel()
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
        connection        = engine.connect()
        metadata          = db.MetaData()
        DriverOrder       = db.Table ("deliver_messenger",   metadata,
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

############################
#     RABBITMQ PRODUCE     #
############################
def produce(msg):
    channel.exchange_declare(exchange      = PRODUCER_EXCHANGE, 
                             durable       = True, 
                             exchange_type = 'direct' )

    channel.queue_declare(queue   = PRODUCER_QUEUE,
                          durable = True)

    channel.queue_bind(queue       = PRODUCER_QUEUE,
                       exchange    = PRODUCER_EXCHANGE,  
                       routing_key = PRODUCER_BINDING_KEY)
    
    channel.basic_publish(exchange    = PRODUCER_EXCHANGE,
                          routing_key = PRODUCER_BINDING_KEY,
                          body        = msg,
                          properties  = pika.BasicProperties(delivery_mode = 2, 
                                                             content_type  = "application/json"))

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

############################
#      SCHEDULER INIT      #
############################

s = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(10,1,vendor_listen, ())
    s.run()

###########################
#         GLOBALS         #
###########################

update_id = None

############################
#         LISTENER         #
############################

def vendor_listen():
    
    global update_id
    
    # RECONNECT TO THE DATABASE
    while True:
        try:
            engine            = db.create_engine(os.environ['URI'])
            connection        = engine.connect()
            metadata          = db.MetaData()
            DriverOrder       = db.Table ("deliver_messenger",   metadata,
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

    # RECEIVE UPDATES FROM THE TELEGRAM BOT
    updates = bot.get_updates(offset=update_id).get("result",[])

    # RETRIEVE THE LATEST UPDATE
    if updates:
        update_id = updates[-1]["update_id"] + 1 
    
        for item in updates:
            
            try:
                message    = item["message"]["text"]       # MESSAGE TEXT
                message_id = item["message"]["message_id"] # MESSAGE ID
                sender     = item["message"]["from"]["id"] # THE CHAT_ID OF THE SENDER OF THE MESSAGE (CAN BE NORMAL / REPLY MESSAGE)
            except:
                message, message_id, sender = None, None, None
            
            if all([message, message_id, sender]):
            # CHECK IF MESSAGE IS ACCEPT ORDER
                if message == "Accept":
                    
                    query = db.select([DriverOrder]).limit(1)
                    ResultProxy = connection.execute(query)
                    
                    output = ResultProxy.fetchall()
                    
                    # IF THERE IS A PENDING ORDER TO DELIVER IN THE DATABASE
                    if output:
                        
                        output = output[0]
                        
                        # SEND MESSAGE TO THE DRIVER WHO ACCEPTED
                        bot.send_message("You have accepted the Delivery Order.", sender)
                        
                        # DELETE THE DATABASE ENTRY
                        query = db.delete(DriverOrder).where(DriverOrder.columns.order_id==output[0])
                        ResultProxy = connection.execute(query)
                        
                        # QUERY CRM FOR ALL THE DRIVERS
                        response = json.loads(requests.post(CRM_USR_FROM_USRTYPE, json={"user_type": "driver"}).text)
                        
                        # NOTIFY EACH DRIVER IT HAS BEEN TAKEN BY OTHERS
                        for driver in response:
                            driver_chat_id = driver.get("chat_id")  
                            if driver_chat_id != sender:
                                bot.send_message("The order has been accepted by another driver", driver_chat_id)             
                        
                        # QUERY CRM TO OBTAIN DRIVER USERNAME
                        response = json.loads(requests.post(CRM_USR_FROM_CHATID, json={"tid": sender}).text)
                        
                        print(response.get("username"))
                        
                        # RABBITMQ TOWARDS ORDER PROCESSING
                        produce(json.dumps({"orderID"      : output[0],
                                            "delivererID"  : response.get("username"),
                                            "order_status" : "completed"}))
                
###########################
#          START          #
###########################
      
while True:
    try:
        scheduler()
    except:
        print("An unexpected error occured, retrying in 3 seconds")
        time.sleep(3)

connection.close()