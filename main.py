from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from rmq import Consumer, publish
from threading import Thread

app = FastAPI()
consumer = Consumer()
Thread(target=consumer.run).start()

@app.get("/")
async def home():
    return "OK"

@app.get("/consumer")
async def consumer_rt():
    return StreamingResponse(consumer.get(), mimetype='text/event-stream')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer_rt(data: str):
    publish(data)
    return {"status": "OK", "message": data}