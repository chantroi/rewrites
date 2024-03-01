from quart import Quart, Response, request
from quart_cors import cors
from rmq import Consumer, publish
from threading import Thread

app = Quart()
cors(app, allow_origin=["*"])
consumer = Consumer()
Thread(target=consumer.run).start()

@app.get("/")
async def home():
    return "OK"

@app.get("/consumer")
async def consumer_rt():
    return Response(consumer.get(), mimetype='text/event-stream')
    
@app.route("/producer", methods=["GET", "POST"])
async def producer_rt():
    data = request.args.get("data")
    publish(data)
    return {"status": "OK", "message": data}