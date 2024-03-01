from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from rmq import start_mq, consumer, deliver

app = FastAPI()
start_mq()

@app.get("/")
async def home():
    return StreamingResponse(consumer.get(), mimetype='text/plain')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer(data: str):
    deliver.send(data)
    return RedirectResponse("/")