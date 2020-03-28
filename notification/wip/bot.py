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

    def send_message(self, msg=None, chat_id=None):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        return json.loads(requests.get(url).text)

    def display_button(self, msg=None, chat_id=None):
        url = self.base + "sendMessage?chat_id={}&text={}&reply_markup=".format(chat_id, msg)
        url += '{"keyboard":[["Accept"]],"resize_keyboard":true,"one_time_keyboard":true}'
        return json.loads(requests.get(url).text)