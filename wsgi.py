from flask import Flask, Response, redirect, request
from rmq import start_mq, consumer, deliver

app = Flask(__name__)
start_mq()

@app.route("/")
def home():
    return Response(consumer.get(), mimetype='text/plain')

@app.route("/producer", methods=["GET", "POST"])
def producer():
    data = request.args.get('data') or request.form.get('data')
    if data:
        deliver.send(data)
    return redirect("/")