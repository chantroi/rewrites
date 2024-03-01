from flask import Flask, Response, redirect, request
from rmq import Consumer, Deliver
from threading import Thread

app = Flask(__name__)
consumer = Consumer()
deliver = Deliver()

@app.route("/")
def home():
    return "Ok"
    
@app.route("/consumer")
def consumer_rt():
    return Response(consumer.get(), mimetype='text/plain')

@app.route("/producer", methods=["GET", "POST"])
def producer_rt():
    data = request.args.get('data') or request.form.get('data')
    if data:
        deliver.send(data)
    return redirect("/")
    
Thread(target=consumer.run).start()
Thread(target=deliver.run).start()