import os
import requests
from bot import telegram_chatbot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_KEY = os.environ['API_KEY'] 
bot = telegram_chatbot(API_KEY)

update_id = None
reregister_id = None
successful_register = {}

while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    
    if updates: 
        for item in updates:
            # ENSURES THAT THE NEWEST MESSAGE IS RETRIEVED
            update_id = item["update_id"]
            update_id = update_id + 1
            try:
                message = str(item["message"]["text"])
                message_id = item["message"]["message_id"]
            except:
                message = None
                message_id = None
            
            # RETRIEVE THE CHAT_ID OF THE SENDER OF THE MESSAGE (CAN BE NORMAL / REPLY MESSAGE)
            sender = str(item["message"]["from"]["id"])

            try:
                # MESSAGE ID OF A REPLY MESSAGE
                reply_message_id = item["message"]["reply_to_message"]["message_id"]
            except:
                reply_message_id = None

            # CHECK IF SENDER HAS REGISTER BEFORE
            if sender not in successful_register:            
                # CHECK IF THE INCOMING MESSAGE IS A REPLY TO A MESSAGE
                if reply_message_id != None:
                    username = message
                    bot.send_message("Registration Successful!", sender)
                    successful_register[sender] = username

                # IF INCOMING MESSAGE IS NOT A REPLY MESSAGE
                else:
                    # EXCEPTION --> WHEN USER STARTS THE BOT
                    if message == "/start":
                        bot.message_reply("Thank you for subscribing to EaSy Delivery! If you are a new user, please register by replying to this message.",
                                        sender)
                    
                    # USERS CANNOT REGISTER IF IT IS NOT A REPLY MESSAGE
                    else:
                        bot.message_reply("Sorry, this operation is not permitted. Please reply to this message to register", sender)
            
            # USERS WOULD LIKE TO EDIT THE REGISTERED USERNAME
            else:
                # REPLY TO MESSAGE --> YOU HAVE ALREADY REGISTERED ...
                if reply_message_id != None and reply_message_id == reregister_id:
                    successful_register[sender] = username
                    bot.send_message("Your username has been updated!", sender)
                else:
                    reregister = bot.message_reply("You have already registered. To edit your username, please reply to this message with your new username.", sender)
                    # CAPTURE THE MESSAGE ID OF ^THIS PROMPT
                    reregister_id = reregister["result"]["message_id"]
                