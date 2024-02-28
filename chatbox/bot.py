from hydrogram import Client
import requests
import os

r = requests.get(os.getenv('SECRET')).json()
api_id = r["key"]["api_id"]
api_hash = r["key"]["api_hash"]
bot_token = r["bot"]["ai_tg"]

class Bot:
    def __init__(self):
        self.bot = Client("bot", api_id, api_hash, bot_token=bot_token)