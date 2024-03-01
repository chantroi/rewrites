from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from rmq import Consumer, Deliver
from threading import Thread

app = FastAPI()
consumer = Consumer()
deliver = Deliver()
Thread(target=consumer.run).start()

@app.get("/")
async def home():
    return StreamingResponse(consumer.get(), mimetype='text/event-stream')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer(data: str):
    deliver.send(data)
    return "Done"