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

# BOT API KEY
API_KEY = os.environ['API_KEY'] 
        
#############################
#    RABBITMQ CONNECTION    #
#############################

time.sleep(15)

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
        engine = db.create_engine(os.environ['URI'])
        connection = engine.connect()
        metadata = db.MetaData()
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
        
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

############################
#     RABBITMQ PRODUCE     #
############################
def produce(msg):
    channel.exchange_declare(exchange = PRODUCER_EXCHANGE, 
                             durable  = True, 
                             exchange_type = 'direct')

    channel.queue_declare(queue   = PRODUCER_QUEUE,
                          durable = True)

    channel.queue_bind(queue       = PRODUCER_QUEUE,
                       exchange    = PRODUCER_EXCHANGE,  
                       routing_key = PRODUCER_BINDING_KEY )
    
    channel.basic_publish(exchange    = PRODUCER_EXCHANGE,
                          routing_key = PRODUCER_BINDING_KEY,
                          body        = msg,
                          properties  = pika.BasicProperties(delivery_mode=2))

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

############################
#      SCHEDULER INIT      #
############################

s   = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(3,1,vendor_listen, ())
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
    
    while True:
        try:
            engine = db.create_engine(os.environ['URI'])
            connection = engine.connect()
            metadata = db.MetaData()
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
            count += 1
            print(f"Connection Lost, Attempting to Reconnect in 3s...")
            time.sleep(3)

    # RECEIVE UPDATES FROM THE TELEGRAM BOT
    updates = bot.get_updates(offset=update_id).get("result",[])
    
    # RETRIEVE THE LATEST UPDATE
    if updates:
        update_id = updates[-1]["update_id"] + 1    
    
    for item in updates:
        
        message    = item["message"]["text"]       # MESSAGE TEXT
        message_id = item["message"]["message_id"] # MESSAGE ID
        sender     = item["message"]["from"]["id"] # THE CHAT_ID OF THE SENDER OF THE MESSAGE (CAN BE NORMAL / REPLY MESSAGE)
        
        # CHECK IF MESSAGE IS ACCEPT ORDER
        if message == "Accept Order":
            
            query = db.select([VendorMessenger]).where(VendorMessenger.columns.message_id==sender)
            ResultProxy = connection.execute(query)
            
            if output := ResultProxy.fetchall():
                bot.send_message("You have accepted the Order.", sender)
                
                query = db.delete(VendorMessenger).where(VendorMessenger.columns.message_id==sender)

                ResultProxy = connection.execute(query)
                
                produce(json.dumps({"orderID"      : output[0][0],
                                    "order_status" : "order ready"}))
                
###########################
#          START          #
###########################
       
while True:
    scheduler()

connection.close()