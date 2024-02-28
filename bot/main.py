from hydrogram import Client
from fastapi import FastAPI, Request, WebSocket
from threading import Thread
import uvicorn
import requests
import os

res = requests.get(os.getenv('SECRET')).json()
api_id = res["key"]["api_id"]
api_hash = res["key"]["api_hash"]
bot_token = res["bot"]["ai_tg"]

bot = Client("bot", api_id, api_hash, bot_token=bot_token)
app = FastAPI()
client: WebSocket = None


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global client
    await ws.accept()
    while True:
        data = await ws.receive_json()
        if data["type"] == "connect":
            client = ws
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
    await client.send_json(data)
    
def run_uvicorn():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    uvicorn_thread = Thread(target=run_uvicorn)
    uvicorn_thread.start()
    bot.run()