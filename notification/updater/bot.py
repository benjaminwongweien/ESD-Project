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

    def get_updates(self, offset=None):
        offset = "&offset={}".format(offset) if offset else ""
        url = self.base + "getUpdates?timeout=100" + offset
        return json.loads(requests.get(url).text)
    