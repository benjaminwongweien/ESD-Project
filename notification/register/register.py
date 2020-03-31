import os
import time
import json
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

API_KEY          = os.environ['API_KEY'] 
CRM_USERNAME_GET = os.environ['CRM_USERNAME_GET']
CRM_REGISTER     = os.environ['CRM_REGISTER']
CRM_CHATID_GET   = os.environ['CRM_CHATID_GET']

#############################
#     TELEGRAM BOT INIT     #
#############################

bot       = telegram_chatbot(API_KEY)

update_id = None
tries     = 0
first     = True

#############################
#      SCHEDULER INIT       #
#############################

s         = sched.scheduler(time.time, time.sleep)

def scheduler():
    s.enter(3,1,register, ())
    s.run()

def register():
        
    global update_id
    global first
    
    updates = bot.get_updates(offset=update_id).get("result",[])
    
    if first:
        if updates:
            first      = False
            update_id  = updates[-1]["update_id"] + 1
            updates = bot.get_updates(offset=update_id).get("result",[])

    for item in updates:
        
        message    = item["message"]["text"]       # MESSAGE TEXT
        message_id = item["message"]["message_id"] # MESSAGE ID
        sender     = item["message"]["from"]["id"] # THE CHAT_ID OF THE SENDER OF THE MESSAGE (CAN BE NORMAL / REPLY MESSAGE)
        
        try:
            # MESSAGE ID OF A REPLY MESSAGE
            reply_message_id = item["message"]["reply_to_message"]["message_id"]
        except:
            reply_message_id = None
            
        if reply_message_id:
            # CHECK IF HE HAS ASKED TO REGISTER IN THE DATABASE WITH HIS REPLY MESSAGE ID (1)
            query       = db.select([Register]).where(Register.columns.message_id==reply_message_id)
            ResultProxy = connection.execute(query)
            ResultSet   = ResultProxy.fetchall()
            
            if ResultSet:
                # CHECK IF USER EXISTS IN CRM
                response = requests.post(CRM_USERNAME_GET, json={"username": message})
                response = json.loads(response.text)
                # (2 fail) REGISTER WITH US ON EASYDELIVERY FIRST!
                if response.get("status"):
                    bot.send_message(msg="Invalid username used to register, resume the registration process by pressing /start", 
                                    chat_id=sender)
                else:
                    # CHECKS IF USER HAS AN ENTRY IS IN DATAVASE
                    response = requests.post(CRM_CHATID_GET, json={"tid": sender})
                    response = json.loads(response.text)      
                    if not response.get("status"):
                        response = requests.post(CRM_REGISTER, json={"uid": response["username"],
                                                                     "tid": None})             
                    
                    # IF USER EXISTS REGISTER HIM IN CRM
                    response = requests.post(CRM_REGISTER, json={"uid": message,
                                                                 "tid": sender})  
                    
                    # REPLY TO USER SUBSCRIPTION SUCCESSFUL
                    bot.send_message(msg="Registration Successful!", chat_id=sender)
                    query        = db.delete(Register).where(Register.columns.chat_id==sender)
                    ResultProxy  = connection.execute(query)
                
            # (1 fail) REPLY YOU HAVE REGISTERED BEFORE PLEASE START PROCESS BY WRITING /START
            else:
                bot.send_message(msg="You have not started the reigstration process. Please start by pressing /start.", chat_id=sender)

        
        elif message == "/start":
            # CHECK IF REGISTRATION REQUEST WAS MADE BEFORE
            query       = db.select([Register]).where(Register.columns.chat_id==sender)
            ResultProxy = connection.execute(query)
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
            
            if ResultSet:
                query = db.update(Register).values(message_id=reply_to_message_id).where(Register.columns.chat_id==sender)
            else:
                query = db.insert(Register).values(chat_id=sender, message_id=reply_to_message_id)
                
            ResultProxy = connection.execute(query)

    else:
        if updates:
            update_id = item["update_id"] + 1

#############################
#    DATABASE CONNECTION    #
#############################

while True:
    print("Attempting to connect to the database")
    try:
        engine     = db.create_engine(os.environ['URI'])
        connection = engine.connect()
        metadata   = db.MetaData()
        Register = db.Table("register", metadata,
                            db.Column("chat_id", db.Integer(), nullable=False, autoincrement=False ,primary_key=True),
                            db.Column("message_id", db.Integer(), nullable=False))
        metadata.create_all(engine)
        print("Connection Succesful")
        break
    except:
        tries += 1
        print(f"Connection Failed, retrying in 3s, tries: {tries}")
        time.sleep(3)

print("Registration Listener has started with no Errors.")
while True:
    scheduler()

