import os
import time
import json
import requests
import sqlalchemy as db
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

print("Starting Updater...")

##########################
#     INITIALIZE ENV     #
##########################

load_dotenv(find_dotenv())

#########################
#       CONSTANTS       #
#########################

# BOT API KEY
API_KEY = os.environ['API_KEY'] 

#############################
#    DATABASE CONNECTION    #
#############################

time.sleep(25)

print("Attempting to connect to the Database...")

count = 0

while True:
    
    try:
        engine        = db.create_engine(os.environ['URI'])
        db_connection = engine.connect()
        metadata      = db.MetaData()
        Telegram      = db.Table ("telegram",            metadata,
                        db.Column("update_id",           db.Integer(),    nullable=False, primary_key=True ),
                        db.Column("sender",              db.Integer(),    nullable=False,                  ),
                        db.Column("message_id",          db.Integer(),    nullable=False                   ),
                        db.Column("text",                db.String(1000), nullable=False                   ),
                        db.Column("reply_to_message_id", db.Integer(),    nullable=True,                   ))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        count += 1
        print(f"Connection Failed... Attempting to Reconnect in 3s, tries: {count}")
        time.sleep(3)

print("Updater has successfull started with no errors.")

#############################
#     TELEGRAM BOT INIT     #
#############################

bot = telegram_chatbot(API_KEY)

#############################
#        SCHEDULER          #
#############################

offset = None

while True:
    
    response = bot.get_updates(offset=offset)
    success = response.get("ok")
    
    if success == True:
        
        result = response.get("result")
        
        if result:
            
            for item in result:
            
                update_id           = item.get("update_id")
                sender              = item.get("message",{}).get("from",{}).get("id")
                message_id          = item.get("message",{}).get("message_id")
                text                = item.get("message",{}).get("text")
                reply_to_message_id = item.get("message",{}).get("reply_to_message",{}).get("message_id",None)
             
                if all([update_id,sender,message_id,text]):
            
                    print(f"""
                        Found an new update, Details: 
                        Update ID           : {update_id}
                        Sender ID           : {sender}
                        Message ID          : {message_id}
                        text                : {text}
                        reply_to_message_id : {reply_to_message_id}
                        """)
            
                    print("Updating the Database with the new Timestamp")  
                    query       = db.insert(Telegram).values(update_id           = update_id,
                                                             sender              = sender,
                                                             message_id          = message_id,
                                                             text                = text,
                                                             reply_to_message_id = reply_to_message_id)
                    ResultProxy = db_connection.execute(query)
                    print("Update Successful...")
            
            else:
                offset = update_id + 1

