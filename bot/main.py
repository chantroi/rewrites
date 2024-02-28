from hydrogram import Client
from threading import Thread
import socket
import requests
import json
import os

res = requests.get(os.getenv('SECRET')).json()
api_id = res["key"]["api_id"]
api_hash = res["key"]["api_hash"]
bot_token = res["bot"]["ai_tg"]

bot = Client("bot", api_id, api_hash, bot_token=bot_token, in_memory=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8000))
client = None

def tcp():
    global client
    server.listen()
    print("TCP Server is running")
    while True:
        conn, client = server.accept()
        bytes_data = conn.recv(10*1024*1024)
        text_data = bytes_data.decode('utf-8', errors='replace')
        bot.send_message("share_v2ray_file", text_data)
        
@bot.on_message()
def on_message(c, m):
    if m.text:
        data = dict(
            user=m.from_user.first_name,
            content=m.text,
            type="text"
        )
    elif m.video:
        content = c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="video"
        )
    elif m.photo:
        content = c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="image"
        )
    elif m.audio:
        content = c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="audio"
        )
    elif m.sticker:
        content = c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="image"
        )
        data = str(data).encode('utf-8', errors='replace')
    client.send(data)

if __name__ == "__main__":
    thread = Thread(target=tcp)
    thread.start()
    print("bot running")
    bot.run()