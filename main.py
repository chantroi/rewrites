from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from rmq import Consumer, publish
from threading import Thread

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)
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