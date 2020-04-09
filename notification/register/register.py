"""
Notification Microservice - Register

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman, Low Louis
@team   - G3T4
"""

import os
import time
import json
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Register...")

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

API_KEY          = os.environ['API_KEY'] 
CRM_USERNAME_GET = os.environ['CRM_USERNAME_GET']
CRM_REGISTER     = os.environ['CRM_REGISTER']
CRM_CHATID_GET   = os.environ['CRM_CHATID_GET']

#############################
#    DATABASE CONNECTION    #
#############################

time.sleep(25)

print("Attempting to connect to the database...")

count = 0

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
        Register          = db.Table("register",    metadata,
                            db.Column("chat_id",    db.Integer(), nullable=False ,primary_key=True),
                            db.Column("message_id", db.Integer(), nullable=False                  ))
        metadata.create_all(engine)
        print("Connection Successful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Register has started successfully with no Errors.")

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

###########################
#         GLOBALS         #
###########################

offset = None

#############################
#      SCHEDULER INIT       #
#############################

while True:

    time.sleep(3)
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
            
            update_id           = result[0]
            sender              = result[1]
            message_id          = result[2]
            text                = result[3]
            reply_to_message_id = result[4]
                    
            if all([update_id, sender, message_id, text]):
            # CHECK IF MESSAGE IS ACCEPT ORDER
                
                if reply_to_message_id:
                    print("Found a Register Reply")
                    query       = db.select([Register]).where(Register.columns.message_id==reply_to_message_id)
                    ResultProxy = db_connection.execute(query)
                    ResultSet   = ResultProxy.fetchall()
                    
                    if ResultSet:
                        # CHECK IF USER EXISTS IN CRM
                        response = requests.post(CRM_USERNAME_GET, json={"username": text})
                        response = json.loads(response.text)
                        # (2 fail) REGISTER WITH US ON EASYDELIVERY FIRST!
                        if response.get("status"):
                            bot.send_message(msg="Invalid username used to register, resume the registration process by pressing /start", 
                                            chat_id=sender)
                        else:
                            # CHECKS IF USER HAS AN ENTRY IS IN DATABASE
                            response = requests.post(CRM_CHATID_GET, json={"tid": sender})
                            
                            response = json.loads(response.text)     
                             
                            if not response.get("status"):
                                response = requests.post(CRM_REGISTER, json={"uid": response["username"],
                                                                             "tid": None})             
                            
                            # IF USER EXISTS REGISTER HIM IN CRM
                            response = requests.post(CRM_REGISTER, json={"uid": text,
                                                                        "tid": sender})  
                            
                            # REPLY TO USER SUBSCRIPTION SUCCESSFUL
                            bot.send_message(msg="Registration Successful!", chat_id=sender)
                            
                            query        = db.delete(Register).where(Register.columns.chat_id==sender)
                            ResultProxy  = db_connection.execute(query)
                        
                    # (1 fail) REPLY YOU HAVE REGISTERED BEFORE PLEASE START PROCESS BY WRITING /START
                    else:
                        bot.send_message(msg="You have not started the reigstration process. Please start by pressing /start.", chat_id=sender)

            
                elif text == "/start":
                    print("Found a Register Request")
                    # CHECK IF REGISTRATION REQUEST WAS MADE BEFORE
                    query       = db.select([Register]).where(Register.columns.chat_id==sender)
                    ResultProxy = db_connection.execute(query)
                    ResultSet   = ResultProxy.fetchall()
                    if ResultSet:
                        bot_response = bot.message_reply("You have already attempted to register, please reply to this message to continue.", sender)
                        
                    else:
                        # CHECK IF USER's CHAT ID IS IN DATABASE
                        response = requests.post(CRM_CHATID_GET, json={"tid": sender})
                        response = json.loads(response.text)
                                    
                        if response.get("status"):
                            bot_response = bot.message_reply("Thank you for subscribing to EaSy Delivery! If you are a new user, please register by replying to this message.", sender)

                        else:
                            # IF NOT IN DATABASE
                            bot_response = bot.message_reply("This telegram id is already registered. To reassociate your telegram account, please reply to this message with your new username.", sender)

                    
                    reply_to_message_id = bot_response["result"]["message_id"]
                    
                    print("Updating Register Database...")
                    if ResultSet:
                        query = db.update(Register).values(message_id=reply_to_message_id).where(Register.columns.chat_id==sender)
                    else:
                        query = db.insert(Register).values(chat_id=sender, message_id=reply_to_message_id)
                        
                    ResultProxy = db_connection.execute(query)
                    print("Successfully updated Register Database.")
        
        else:
            offset = update_id + 1   



