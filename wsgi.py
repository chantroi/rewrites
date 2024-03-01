from flask import Flask, Response, redirect, request
from rmq import Consumer, Deliver
from threading import Thread

app = Flask(__name__)
consumer = Consumer()
deliver = Deliver()
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
    if data:
        deliver.send(data)
    return "Done"