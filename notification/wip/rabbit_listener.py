import os
import pika
import json
import time
import requests
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

# HEXADECIMAL CHAT CONSTANTS
LINE_BREAK = "%0A"

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#    RABBITMQ CONNECTION    #
#############################

credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)

connection = pika.BlockingConnection(pika.ConnectionParameters(host         = HOST,
                                                               port         = PORT,
                                                               virtual_host = VIRTUAL_HOST,
                                                               credentials  = credentials))
channel = connection.channel()

#############################
#     RABBITMQ PRODUCER     #
#############################

def produce(order_id,status):
    channel.exchange_declare(exchange      = PRODUCER_EXCHANGE, 
                             durable       = True, 
                             exchange_type = 'direct')

    channel.queue_declare(queue   = PRODUCER_QUEUE,
                          durable = True)

    channel.queue_bind(queue       = PRODUCER_QUEUE,
                       exchange    = PRODUCER_EXCHANGE,  
                       routing_key = PRODUCER_BINDING_KEY)
    
    channel.basic_publish(exchange    = PRODUCER_EXCHANGE, 
                          routing_key = PRODUCER_BINDING_KEY,
                          body        = {"orderID"     : order_id,
                                         "order_status": status},
                          properties  = pika.BasicProperties(delivery_mode = 2))
    connection.close()

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
    
    channel.basic_consume(queue=CONSUMER_QUEUE,
                          on_message_callback=callback,
                          auto_ack=False)

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

    ###############################
    #   TELEGRAM BOT --> VENDOR   #
    #    PAYMENT IS SUCCESSFUL    #
    ###############################

    if order_status.lower() == "payment success":
        
        # OBTAIN USER'S CHAT ID
        user_information = requests.post("http://localhost:88/username", json={"username": body['vendorID']})
        user_information = json.loads(user_information.text)
        chat_id          = user_information["chat_id"]
        
        # TRIGGER THE TELEGRAM BOT
        response = bot.display_button(chat_id = chat_id, 
                                      msg     =  "You have a new order! Please accept the order.")
        
        # TO FACILITATE REPLIES FROM THE TELEGRAM BOT
        message_id = response["result"]["message_id"] + 1

        now       = time.time() # START TIME 
        update_id = None        # PRE-DEFINED UPDATE ID
        update    = None        # PRE-DEFINED UPDATE INFORMATION
        success   = False       # DEFAULT FALSE [TO NACK MESSAGES]
        
        # TIMEOUT = 10s
        while time.time() - now <= 10:
            
            # OBTAIN UPDATE ID BASED ON OFFSET
            if update_id:
                updates = bot.get_updates(update_id)["result"]
                
            # GET ALL UPDATES
            else:
                updates = bot.get_updates()["result"]
            
            # LOOP TO VALIDATE MESSAGES
            for update in updates:
                if update["message"]["text"]       == "Accept"     and \
                   update["message"]["from"]["id"] == chat_id      and \
                   update["message"]["message_id"] >= message_id:
                       success = True
                       produce(orderid = body['orderID'], 
                               order_status = "order ready")
                       break
                   
            # FOR ELSE LOOP TO CATCH THE LAST UPDATE ID (IF THERE IS NO REPLY)
            else:
                update_id = update["update_id"]
                continue 
            
            # FORCEFULLY END THE LOOP
            break
        
        # ACK THE MESSAGE        
        if success:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
        # NACK THE MESSAGE
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    ###############################
    #   TELEGRAM BOT --> DELIVER  #
    #  ORDER IS READY TO COLLECT  #
    ###############################
   
    elif order_status.lower() == "order ready":
        pass

    ###############################
    #  TELEGRAM BOT --> CUSTOMER  #
    #       ORDER DELIVERED       #
    ###############################
                  
    elif order_status.lower() == "completed":
        pass

consume()
