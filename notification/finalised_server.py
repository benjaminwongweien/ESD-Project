import json
import requests
from flask import request
from bot import telegram_chatbot

bot = telegram_chatbot("config.cfg")

# ------------------------------------------------------------ functions -------------------------------------------------------------#

def make_reply(msg):
    reply = None
    if msg is not None:
        reply = msg
    return reply

def user_type(chatId):
    chatIdURL = "http://localhost:5000/chatId"
    data = {"chatId":str(chatId)}
    request_userType = requests.post(chatIdURL, json=data)
    user_info = json.loads(request_userType.text.lower())
    try:
        user_type = user_info["data"]["user_type"]
    except:
        user_type = None
    
    return user_type

#Type 0 : Customer
#Type 1 : Delivery
#print(user_type(1099183304))

def retrieve_users(uType):
    userURL = "http://localhost:5000/type"
    data = {"type":uType}
    request_users = requests.post(userURL, json=data)
    users = json.loads(request_users.text.lower())
    return users

def delivery_person (chatid=None):
    if chatid != None:
        delivery_person = chatid
    else:
        delivery_person = None
    return delivery_person

# ------------------------------------------------------------ code -------------------------------------------------------------------#

update_id = None
order_status = None
accept_order = None
customer = None
delivery_person = None

while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    
    if updates: 
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            
            sender = str(item["message"]["from"]["id"])
            sender_type = user_type(sender)
            
            # UNREGISTERED USERS:
            if sender_type == None:
                reply = make_reply("Sorry! We are unable to find you amongst our database,")
                reply = reply + make_reply("please contact the system admin at 12345678 to register")
                bot.send_message(reply, sender)
            
            # REGISTERED USERS:
            else:
                if message == "/start":
                    # ALL USERS: Welcome message upon starting the telegram bot
                    reply = make_reply("Thank you for subscribing to EaSy Delivery! To continue, please choose your desired action.")
                    bot.send_message(reply, sender)
                
                else:
                    if sender_type == "0": #CUSTOMERS
                        customer = sender
                        if message == "/order_status":
                            if accept_order == None:
                                reply = make_reply("Please wait a moment as we search for a delivery person for you.")
                                order_status = True

                                all_delivery_person = retrieve_users(1)["data"]
                                
                                for i in range(len(all_delivery_person)):
                                    person = all_delivery_person[i]["chatid"]
                                    notif = make_reply("There is a pending order!")
                                    delivery = person
                                    bot.send_message(notif, delivery)
                                    
                            else:
                                reply = make_reply("Great News! Your food has been picked up! Your driver will arrive in 15 - 20 minutes")
                        
                        elif message == "/pending_orders":
                            reply = make_reply("Operation not permitted. Please login as a delivery person to continue")
                        
                        else:
                            if delivery_person == None:
                                reply = make_reply("We are currently searching for a driver for your order, sorry for the inconvenience")
                            else:
                                sender = delivery_person
                                reply = message
                        
                        bot.send_message(reply, sender)
                    
                    else: #DELIVERY PEOPLE
                        if message == "/pending_orders":
                            if order_status == None:
                                reply = make_reply("There are no pending orders")
                            else:
                                reply_button = make_reply("Would you like to deliver the order?")
                                bot.display_button(reply_button, sender)
                                reply = make_reply("To continue, please indicate your choice")
                                
                        elif message == "Accept":
                            accept_order = True
                            if delivery_person == None:
                                delivery_person = sender
                                reply = make_reply("Order accepted successfully")
                            
                            else:
                                reply = make_reply("Sorry! Another driver has accepted the order")

                        elif message == "Reject":
                                accept_order = None
                                reply = make_reply("Action registered")
                        
                        elif message == "/order_status":
                            reply = make_reply("Operation not permitted. Please login as a customer to continue")

                        else:
                            sender = customer
                            reply = message

                        bot.send_message(reply, sender)
                    