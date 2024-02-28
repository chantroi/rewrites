from websockets.sync.client import connect
import json
import os

ws = connect(os.getenv('WS'))

def websocket(st):
    with ws:
        ws.send("Connected")
        while True:
            message = ws.recv()
            m = json.loads(message)
            st.session_state.messages.append({"user": m["name"], "content":
            m["content"], "type": m["type"]})
            with st.chat_message(m["name"]):
                if m["type"] == "video":
                    st.video(m["content"])
                elif m["type"] == "image":
                    st.image(m["content"])
                elif m["type"] == "audio":
                    st.audio(m["content"])