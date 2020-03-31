import os
import pika
import json
import time
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

# Constants to produce (send) to ORDER PROCESSING
PRODUCER_EXCHANGE    = os.environ['PRODUCER_EXCHANGE']
PRODUCER_QUEUE       = os.environ['PRODUCER_QUEUE']
PRODUCER_BINDING_KEY = os.environ['PRODUCER_BINDING_KEY']

# Constants to consume (receive) from ORDER PROCESSING
CONSUMER_EXCHANGE     = os.environ['CONSUMER_EXCHANGE']
CONSUMER_QUEUE        = os.environ['CONSUMER_QUEUE']
CONSUMER_BINDING_KEY  = os.environ['CONSUMER_BINDING_KEY']

# Credentials
RABBIT_USERNAME = os.environ['RABBIT_USERNAME']
RABBIT_PASSWORD = os.environ['RABBIT_PASSWORD']
HOST            = os.environ['HOST']
PORT            = os.environ['PORT']
VIRTUAL_HOST    = os.environ['VIRTUAL_HOST']

# URLS
CRM_USR_FROM_USRNAME = "http://localhost:88/username"
CRM_USR_FROM_USRTYPE = "http://localhost:88/usertype"

# HEXADECIMAL CHAT CONSTANTS
LINE_BREAK = "%0A"

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

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
        vendorMessenger = db.Table("vendor_messenger", metadata,
                            db.Column("order_id", db.String(80), nullable=False, autoincrement=False ,primary_key=True),
                            db.Column("vendor_id", db.Integer(), nullable=False, primary_key=True),
                            db.Column("order_status", db.String(80), nullable=False),
                            db.Column("timestamp", db.Integer(), default=time.time(), nullable=False),
                            db.Column("messaging_timestamp", db.Integer(), default=None, nullable=True))
        
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

#############################
#     RABBITMQ CONSUMER     #
#############################

def consume():
    channel.exchange_declare(exchange      = CONSUMER_EXCHANGE, 
                             durable       = True, 
                             exchange_type = 'direct')

    channel.queue_declare(queue   = CONSUMER_QUEUE,
                          durable = True)

    channel.queue_bind(queue       = CONSUMER_QUEUE,
                       exchange    = CONSUMER_EXCHANGE,  
                       routing_key = CONSUMER_BINDING_KEY)
    
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue               = CONSUMER_QUEUE,
                          on_message_callback = callback,
                          auto_ack            = False)

    channel.start_consuming()

##############################
#       MAIN FUNCTIONS       #
##############################

def callback(channel, method, properties, body):
    ''' ORDER PROCESSING --> TELEGRAM BOT

        Types of Status:
        1. Payment Success (Send to Vendor)
        2. Order Ready (Send to delivery man)
        3. Completed (Send to Customer)'''
    
    body = json.loads(body)
    
    order_id     = body['orderID']
    order_status = body['order_status']
    vendor_id = body['vendorID']

    ###############################
    #   TELEGRAM BOT --> VENDOR   #
    #    PAYMENT IS SUCCESSFUL    #
    ###############################

    if order_status.lower() == "payment success":
        success = True   
        if success:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
            query = db.insert(vendorMessenger).values(order_id = order_id, vendor_id=vendor_id, order_status = order_status)
            
            ResultProxy = connection.execute(query)
            
        # NACK THE MESSAGE
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    ###############################
    #   TELEGRAM BOT --> DELIVER  #
    #  ORDER IS READY TO COLLECT  #
    ###############################
   
    elif order_status.lower() == "order ready":
        if success:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
            query = db.update(vendorMessenger).values(vendorMessenger.order_status==order_status).where(vendorMessenger.vendor_id==vendorID and vendorMessenger.order_id == orderID)
            
            ResultProxy = connection.execute(query)
        
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    ###############################
    #  TELEGRAM BOT --> CUSTOMER  #
    #       ORDER DELIVERED       #
    ###############################
                  
    elif order_status.lower() == "completed":
        # RETRIEVE THE CUSTOMER FOR THAT PARTICULAR ORDER
        cust_information = requests.post(CRM_USR_FROM_USRNAME, json={"username": body['customerID']})
        cust_chat_id = json.loads(cust_information)["chat_id"]
        bot.send_message("Great News! Your order has been delivered", cust_chat_id)
        bot.send_message("Thank you for your purchase!", cust_chat_id) 
        bot.rate_service("Please take a few moments to rate our service", cust_chat_id)
        
        
consume()
