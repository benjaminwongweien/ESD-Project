import os
import time
import json
import pika
import sched
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Vendor Listener...")

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
        
#############################
#    RABBITMQ CONNECTION    #
#############################

time.sleep(27)

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
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("food_id",              db.Integer(), nullable=False                                       ),
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

print("Vendor Listener has successfull started with no errors.")

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
                          properties  = pika.BasicProperties(delivery_mode = 2,
                                                             content_type  = 'application/json'))

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

############################
#      SCHEDULER INIT      #
############################

s   = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(10,1,vendor_listen, ())
    s.run()

###########################
#         GLOBALS         #
###########################

update_id = None
order_id  = None

############################
#         LISTENER         #
############################

def vendor_listen():
    
    global update_id
    global order_id
    
    while True:
        try:
            engine = db.create_engine(os.environ['URI'])
            db_connection = engine.connect()
            metadata = db.MetaData()
            VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                                db.Column("order_id",            db.String(80), nullable=False, autoincrement=False , primary_key=True),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("food_id",             db.Integer(), nullable=False                                         ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                                db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
            metadata.create_all(engine)
            break
        except:
            count += 1
            print("Connection Lost, Attempting to Reconnect in 3s...")
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
                if message == "Accept Order":
                    
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
                        time.sleep(1)
                        print("Message successfully sent.")
                        
                        while True:
                            try:
                                credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
                                rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host         = HOST,
                                                                                               port         = PORT,
                                                                                               virtual_host = VIRTUAL_HOST,
                                                                                               credentials  = credentials))
                                channel = rabbit_connection.channel()
                                print("Connection Successful")
                                break
                            except:
                                count += 1
                                print(f"Connection Failed... Attempting to Reconnect in 3s... Number of tries: {count}")
                                time.sleep(3)

                        print("Notifying Order Processing of new Status...")
                        produce(json.dumps({"orderID"      : order_id,
                                            "delivererID"  : "0",
                                            "order_status" : "order ready"}))
                        print("Successfully sent the message through the broker...")
                        print("Deleting old entry from the database...")
                        query       = db.delete(VendorMessenger).where(VendorMessenger.columns.message_id==sender)
                        ResultProxy = db_connection.execute(query)
                        print("Successfully deleted the old entry from the database.")
                    
###########################
#          START          #
###########################
       
while True:
    scheduler()
    try:
        scheduler()
    except pika.exceptions.StreamLostError:
        print("Network Error")
        time.sleep(3)
    
        print("Attempting to re-connect to RabbitMQ Broker...")
        while True:

            try:
                credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)

                rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host         = HOST,
                                                                            port         = PORT,
                                                                            virtual_host = VIRTUAL_HOST,
                                                                            credentials  = credentials))
                channel = rabbit_connection.channel()
                print("Re-connection Successful")
                break
            except:
                count += 1
                print(f"Connection Failed... Attempting to Reconnect in 3s... Number of tries: {count}")
                time.sleep(3)

            if order_id:
                print("Re-Sending Lost Message...")
                produce(json.dumps({"orderID"      : order_id,
                                    "order_status" : "order ready"})) 
                order_id = None
    except:
        print("Unexpected Error... Restarting in 3s")
        time.sleep(3)

rabbit_connection.close()