import os
import pika
import json
import time
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Rabbit Listener...")

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
CRM_USR_FROM_USRNAME = os.environ['CRM_USR_FROM_USRNAME']
CRM_USR_FROM_USRTYPE = os.environ['CRM_USR_FROM_USRTYPE']

# HEXADECIMAL CHAT CONSTANTS
LINE_BREAK = "%0A"

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#    RABBITMQ CONNECTION    #
#############################

time.sleep(25)

print("Attempting to connect to RabbitMQ Broker...")

count = 0

while True:

    try:
        credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
        rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host        = HOST,
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
        engine     = db.create_engine(os.environ['URI'])
        db_connection = engine.connect()
        metadata   = db.MetaData()
        
        VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                            db.Column("order_id",            db.String(80), nullable=False, autoincrement=False, primary_key=True ),
                            db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                            db.Column("food_id",             db.Integer(),  nullable=False                                        ),
                            db.Column("order_status",        db.String(80), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                            db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
        
        DeliverMessenger  = db.Table ("deliver_messenger",    metadata,
                            db.Column("order_id",            db.String(80),   nullable=False, autoincrement=False, primary_key=True ),
                            db.Column("vendor_id",           db.String(80),   nullable=False, primary_key=True                      ),
                            db.Column("order_status",        db.String(80),   nullable=False                                        ),
                            db.Column("delivery_address",    db.String(1000), nullable=False                                        ),
                            db.Column("timestamp",           db.Integer(),    nullable=False, default=time.time()                   ),
                            db.Column("messaging_timestamp", db.Integer(),    nullable=True,  default=None                          ))
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Rabbit Listener has successfully started with no errors.")

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
    
    channel.basic_qos(prefetch_count = 1)
    
    channel.basic_consume(queue               = CONSUMER_QUEUE,
                          on_message_callback = callback,
                          auto_ack            = False)

    channel.start_consuming()

##############################
#       MAIN FUNCTIONS       #
##############################

def callback(channel, method, properties, body):
    
    body = json.loads(body)
    
    customer_id      = body["customerID"]
    order_id         = body["orderID"]
    vendor_id        = body["vendorID"]
    deliverer_id     = body["delivererID"]
    food_id          = body["foodID"]
    quantity         = body["quantity"]
    price            = body["price"]
    order_status     = body["order_status"]
    delivery_address = body["delivery_address"]
    
    
    print(f"""
          Received Order, Details: 
          CustomerID      : {customer_id}
          Order ID        : {order_id}
          Vendor ID       : {vendor_id}
          Deliverer ID    : {deliverer_id}
          Food ID         : {food_id}
          Quantity        : {quantity}
          Order Status    : {order_status}
          Delivery Address: {delivery_address}
          """)
    
    while True:
        try:
            engine     = db.create_engine(os.environ['URI'])
            db_connection = engine.connect()
            metadata   = db.MetaData()
            
            VendorMessenger   = db.Table ("vendor_messenger",    metadata,
                                db.Column("order_id",            db.String(80), nullable=False, autoincrement=False, primary_key=True ),
                                db.Column("vendor_id",           db.String(80), nullable=False, primary_key=True                      ),
                                db.Column("food_id",             db.Integer(),  nullable=False                                        ),
                                db.Column("order_status",        db.String(80), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),  nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),  nullable=True,  default=None                          ),
                                db.Column("message_id",          db.Integer(),  nullable=True,  default=None                          ))
            
            DeliverMessenger  = db.Table ("deliver_messenger",    metadata,
                                db.Column("order_id",            db.String(80),   nullable=False, autoincrement=False, primary_key=True ),
                                db.Column("vendor_id",           db.String(80),   nullable=False, primary_key=True                      ),
                                db.Column("order_status",        db.String(80),   nullable=False                                        ),
                                db.Column("delivery_address",    db.String(1000), nullable=False                                        ),
                                db.Column("timestamp",           db.Integer(),    nullable=False, default=time.time()                   ),
                                db.Column("messaging_timestamp", db.Integer(),    nullable=True,  default=None                          ))
            metadata.create_all(engine)
            print("Connection Successful")
            break
        except:
            count += 1
            print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
            time.sleep(3)
    
    
    
    ###############################
    #   TELEGRAM BOT --> VENDOR   #
    #    PAYMENT IS SUCCESSFUL    #
    ###############################

    if order_status.lower() == "payment success":
        print(f"Adding Entry OrderID: {order_id} into the Database...")
        try:
            query = db.insert(VendorMessenger).values(order_id     = order_id,
                                                      vendor_id    = vendor_id,
                                                      food_id      = food_id,
                                                      order_status = order_status)
            ResultProxy = db_connection.execute(query)
            channel.basic_ack(delivery_tag = method.delivery_tag)
            print("RabbitMQ Message Acknowledged...")    
        except:
            # NACK THE MESSAGE
            channel.basic_nack(delivery_tag = method.delivery_tag, 
                               requeue      = True)
            print("RabbitMQ Message Nacked, Requeuing Message...")            

    ###############################
    #   TELEGRAM BOT --> DELIVER  #
    #  ORDER IS READY TO COLLECT  #
    ###############################
   
    elif order_status.lower() == "order ready":
        print(f"Adding Entry OrderID: {order_id} into the Database...")
        try:
            query = db.insert(DeliverMessenger).values(order_id         = order_id,
                                                       vendor_id        = vendor_id,
                                                       order_status     = order_status,
                                                       delivery_address = delivery_address)
            ResultProxy = db_connection.execute(query)
            channel.basic_ack(delivery_tag = method.delivery_tag)
            print("RabbitMQ Message Acknowledged...")
        except:
            # NACK THE MESSAGE
            
            channel.basic_nack(delivery_tag = method.delivery_tag, 
                               requeue      = True)
            print("RabbitMQ Message Nacked, Requeuing Message...")
            
    ###############################
    #  TELEGRAM BOT --> CUSTOMER  #
    #       ORDER DELIVERED       #
    ###############################
                  
    elif order_status.lower() == "completed":
        print("Attempting to notify Customer of Completed Order...")
        # RETRIEVE THE CUSTOMER FOR THAT PARTICULAR ORDER
        cust_information = requests.post(CRM_USR_FROM_USRNAME, 
                                         json = { "username": body['customerID'] })
        print("Obtaining Customer ChatID...")
        cust_chat_id = json.loads(cust_information.text)["chat_id"]
        print(f"Obtained Customer Chat ID: {cust_chat_id}")
        print("Sending Message...")
        bot.send_message("Great News! Your order has been delivered"    , cust_chat_id)
        bot.send_message("Thank you for your purchase!"                 , cust_chat_id) 
        bot.rate_service("Please take a few moments to rate our service", cust_chat_id)
        time.sleep(1)
        print("Customer Notification Successful")
        channel.basic_ack(delivery_tag = method.delivery_tag)
        print("RabbitMQ Message Acknowledged...")
              
# START          
consume()
