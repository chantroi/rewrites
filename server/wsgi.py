from flask import Flask, redirect, request, make_response, render_template
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
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat App</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
        }
        #chatBox {
            display: flex;
            flex-direction: column;
            width: 80%;
            max-width: 500px;
            height: 70vh;
            border: 1px solid #dddddd;
            border-radius: 15px;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 15px;
            background-color: #ffffff;
        }
        #chatBox p {
            margin: 5px 0;
        }
        #messageForm {
            display: flex;
            width: 80%;
            max-width: 500px;
        }
        #messageForm input {
            flex-grow: 1;
            border: 1px solid #dddddd;
            border-radius: 15px;
            padding: 7px 10px;
            margin-right: 10px;
        }
        #messageForm button {
            background-color: #0099ff;
            border: none;
            border-radius: 15px;
            color: #ffffff;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.2s linear;
        }
        #messageForm button:hover {
            background-color: #007acc;
        }
    </style>
</head>
<body>

    <div id="chatBox">
        <!-- Chat messages will be dynamically added here -->
    </div>

    <form id="messageForm">
        <input type="text" id="messageInput" placeholder="Type a message">
        <button type="submit">Send</button>
    </form>

    <script type="module">
        const sseSource = new EventSource('/sse');
        sseSource.onmessage = function(event) {
        const dataDiv = document.getElementById('chatBox');
        dataDiv.insertAdjacentHTML('beforeend', event.data + '<br>');
    };
    </script>

</body>
</html>
    """
    
@app.route("/sse")
def consumer_rt():
    def event_source():
        for chunk in consumer.get():
            event = ServerSentEvent(chunk)
            yield event.encode()
            
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