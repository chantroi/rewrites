from flask import Flask, Response, redirect, request
from rmq import Consumer, Deliver
from threading import Thread

app = Flask(__name__)
consumer = Consumer()
deliver = Deliver()
Thread(target=consumer.run).start()
Thread(target=deliver.run).start()

def test_chunk():
    import time
    while True:
        yield "Online"
        time.sleep(5)

@app.route("/")
def home():
    return Response(test_chunk(), mimetype="text/plain")
    
@app.route("/consumer")
def consumer_rt():
    return Response(consumer.get(), mimetype='text/plain')

@app.route("/producer", methods=["GET", "POST"])
def producer_rt():
    data = request.args.get('data') or request.form.get('data')
    if data:
        deliver.send(data)
    return redirect("/")