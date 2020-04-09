"""
Notification Microservice - Telegram Bot Class

@author - Benjamin Wong Wei En, Hao Jun Poon, Belle Lee, Chen Ziyi, Masturah Binte Sulaiman, Low Louis
@team   - G3T4
"""

import json
import requests

class telegram_chatbot():

    def __init__(self, token):
        self.token = token
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    # SEND NORMAL MESSAGES
    def send_message(self, msg=None, chat_id=None):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        return json.loads(requests.get(url).text)

    # SEND MESSAGE WITH USERS GIVEN THE OPTION TO ACCEPT
    def display_button(self, msg=None, chat_id=None):
        url = self.base + "sendMessage?chat_id={}&text={}&reply_markup=".format(chat_id, msg)
        url += '{"keyboard":[["Accept"]],"resize_keyboard":true,"one_time_keyboard":true}'
        return json.loads(requests.get(url).text)
    