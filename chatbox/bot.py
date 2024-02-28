from hydrogram import Client
from util import handle_text, handle_video, handle_image, handle_audio
import requests
import os

r = requests.get(os.getenv('SECRET')).json()
api_id = r["key"]["api_id"]
api_hash = r["key"]["api_hash"]
bot_token = r["bot"]["ai_tg"]

class Bot:
    def __init__(self):
        self.bot = Client("bot", api_id, api_hash, bot_token=bot_token)
    
    def commands(self):
        @self.bot.on_message()
        def on_message(c, m):
            if m.text:
                handle_text(m)
            elif m.video:
                handle_video(m)
            elif m.photo:
                handle_image(m)
            elif m.audio:
                handle_audio(m)
            elif m.sticker:
                handle_image(m)
                
    def instance(self):
        return self.bot
                
    def run(self):
        self.commands()
        self.bot.run()