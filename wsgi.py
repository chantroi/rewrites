from flask import Flask, Response, redirect, request
from rmq import MQ

app = Flask(__name__)
mq = MQ()
mq.run()

@app.route("/")
def home():
    return Response(mq.get(), mimetype='text/plain')

@app.route("/producer", methods=["GET", "POST"])
def producer():
    data = request.args.get('data') or request.form.get('data')
    if data:
        mq.send(data)
    return redirect("/")