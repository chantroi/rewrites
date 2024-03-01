from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from rmq import MQ

app = FastAPI()
mq = MQ()
mq.start()

@app.get("/")
async def home():
    return StreamingResponse(mq.get(), mimetype='text/plain')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer(data: str):
    mq.send(data)
    return RedirectResponse("/")