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
    print("Server is running")
    while True:
        conn, client = server.accept()
        bytes_data = conn.recv(10*1024*1024)
        text_data = bytes_data.decode('utf-8', errors='replace')
        data = json.loads(text_data)
        if data["type"] == "connect":
            client = conn
        else:
            text = data["content"]
            await bot.send_message("share_v2ray_file", text)
        
@bot.on_message()
async def on_message(c, m):
    if m.text:
        data = dict(
            user=m.from_user.first_name,
            content=m.text,
            type="text"
        )
    elif m.video:
        content = await c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="video"
        )
    elif m.photo:
        content = await c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="image"
        )
    elif m.audio:
        content = await c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="audio"
        )
    elif m.sticker:
        content = await c.download_media(m)
        data = dict(
            user=m.from_user.first_name,
            content=content,
            type="image"
        )
        data = str(data).encode('utf-8')
    await client.send(data)

if __name__ == "__main__":
    uvicorn_thread = Thread(target=tcp)
    uvicorn_thread.start()
    print("bot running")
    bot.run()