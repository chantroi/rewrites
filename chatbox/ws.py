from websockets.sync.client import connect
import json
import os

def websocket(st):
    with connect(os.getenv('WS')) as websocket:
        websocket.send("Connected")
        while True:
            message = websocket.recv()
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