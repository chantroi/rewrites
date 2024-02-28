from websockets.sync.client import connect
import json
import os

ws = connect("ws://localhost:8000/ws")

def websocket(st):
    with ws:
        ws.send('{"type": "connect"}')
        print("Websocket connected")
        while True:
            message = ws.recv()
            m = json.loads(message)
            st.session_state.messages.append(m)
            with st.chat_message(m["user"]):
                if m["type"] == "video":
                    st.video(m["content"])
                elif m["type"] == "image":
                    st.image(m["content"])
                elif m["type"] == "audio":
                    st.audio(m["content"])