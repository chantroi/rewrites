from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from rmq import MQ

app = FastAPI()
MQ.start()

@app.get("/")
async def home():
    return StreamingResponse(MQ.get(), mimetype='text/plain')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer(data: str):
    MQ.send(data)
    return RedirectResponse("/")