from flask import Flask, Response, redirect, request
from rmq import Consumer, publish
from threading import Thread

app = Flask(__name__)
consumer = Consumer()
Thread(target=consumer.run).start()

@app.route("/")
def home():
    return "Ok"
    
@app.route("/consumer")
def consumer_rt():
    return Response(consumer.get(), mimetype='text/event-stream')

@app.route("/producer", methods=["GET", "POST"])
def producer_rt():
    data = request.args.get('data') or request.form.get('data')
    publish(data)
    return {"status": "OK", "message": data}