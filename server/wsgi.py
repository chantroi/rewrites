from flask import Flask, redirect, request, make_response
from util.mq import Consumer, publish
from util.sse import ServerSentEvent
from threading import Thread
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")
consumer = Consumer()
Thread(target=consumer.run).start()

@app.route("/")
def home():
    return "Ok"
    
@app.route("/sse")
def consumer_rt():
    def event_source():
        for chunk in consumer.get():
            event = ServerSentEvent(chunk)
            yield str({"message": event.encode()})
    response = make_response(
        event_source(),
        {
            'Content-Type': 'text/event-stream; charset=utf-8',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
            'Event-Source': 'Tran Khanh Han'
        },
    )
        
    return response

@app.route("/producer", methods=["GET", "POST"])
def producer_rt():
    data = request.args.get('data') or request.form.get('data')
    publish(data)
    return {"status": "OK", "message": data}