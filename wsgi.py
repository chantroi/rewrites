from flask import Flask, Response, redirect, request
from rMQ import MQ

app = Flask(__name__)
MQ.start()

@app.route("/")
def home():
    return Response(MQ.get(), mimetype='text/plain')

@app.route("/producer", methods=["GET", "POST"])
def producer():
    data = request.args.get('data') or request.form.get('data')
    if data:
        MQ.send(data)
    return redirect("/")