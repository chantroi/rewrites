from quart import Quart, request, make_response
from quart_cors import cors
from util.sse import ServerSentEvent
from rmq import Consumer, publish
from threading import Thread

app = Quart()
cors(app, allow_origin=["*"])
consumer = Consumer()
Thread(target=consumer.run).start()

@app.get("/")
async def home():
    return "OK"

@app.get("/sse")
async def sse():
    async def send_events():
        while True:
            data = consumer.get()
            event = ServerSentEvent(data)
            yield event.encode()
            
    response = await make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response
    
@app.route("/producer", methods=["GET", "POST"])
async def producer_rt():
    data = request.args.get("data")
    publish(data)
    return {"status": "OK", "message": data}