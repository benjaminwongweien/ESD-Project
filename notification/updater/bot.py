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
    