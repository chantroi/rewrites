from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from queue import MQ

app = FastAPI()
mq = MQ()
mq.run()

@app.get("/")
async def home():
    return StreamingResponse(mq.get(), mimetype='text/plain')