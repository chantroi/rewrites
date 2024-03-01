from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from queue import MQ

app = FastAPI()
mq = MQ()
mq.run()

@app.get("/")
async def home():
    return StreamingResponse(mq.get(), mimetype='text/plain')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer(data: str):
    mq.send(data)
    return RedirectResponse("/")