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

    ###############################
    #   TELEGRAM BOT --> VENDOR   #
    #    PAYMENT IS SUCCESSFUL    #
    ###############################

    if order_status.lower() == "payment success":
        
        # OBTAIN USER'S CHAT ID
        user_information = requests.post(CRM_USR_FROM_USRNAME, 
                                         json = {"username": body['vendorID']})
        
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
                       
                       # PRODUCE THE MESSAGE SEND IT TOWARDS ORDER PROCESSING
                       produce(orderid      = body['orderID'], 
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
        
        # RETRIEVE ALL THE DRIVERS WITHIN THE DATABASE
        drivers = requests.post(CRM_USR_FROM_USRTYPE, 
                                json = {"user_type": "driver"})
        
        drivers_info = json.loads(drivers.text)
        
        # LIST OF THE CHAT IDS OF DRIVERS     
        drivers_chatID = []
        
        # RETURN CONSIST OF LIST OF JSON WITH USERNAME AND CHAT_ID
        for driver in drivers_info:
            driver_chat_id = driver.get("chat_id")
            drivers_chatID.append(driver_chat_id)
            # FANOUT THE MESSAGE TO ALL DRIVERS
            response = bot.display_button("There is a pending order! Would you like to accept?", driver_chat_id)
        
        message_id = response["result"]["message_id"] + 1
    
        update_id = None
        order_accepted = None

        while time.time() - now <= 10:
            
            updates = bot.get_updates(offset=update_id)["result"]
            
            if updates: 
                for item in updates:
                    update_id = item["update_id"]
                    
                    # ENSURES THAT THE MOST RECENT MESSAGE HAS BEEN RECEIVED
                    update_id = update_id + 1

                    try:
                        message = str(item["message"]["text"])
                    except:
                        message = None

            sender = str(item["message"]["from"]["id"])
            # THE FIRST DRIVER TO ACCEPT --> INFORM WHAT ORDER TO SEND AND WHERE
            # CURRENT ASSUMPTION: THERE WILL ALWAYS BE AT LEAST ONE PERSON ACCEPTING THE ORDER 
            if message == "Accept":
                if order_accepted == None:
                    order_accepted = True
                    bot.send_message("Please deliver to this location...", sender)
                # SECOND DRIVER WHO ACCEPT ONWARDS
                else:
                    bot.send_message("Another driver has been assigned to the order", sender)
            # WELCOMING MESSAGE --> FOR USERS WHO START THE BOT
            elif message == "/start":
                bot.send_message("Thank you for subscribing with us!", sender)
            # ANY OTHER MESSAGES ARE NOT PERMITTED
            else:
                bot.send_message("Operation not permitted!", sender)
        # AFTER WINNDOW TIME, ALL DRIVERS WILL RECEIVE THIS MESSAGE
        for driver in drivers_chatID:
            bot.send_message("There are currently no pending orders", driver)

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
