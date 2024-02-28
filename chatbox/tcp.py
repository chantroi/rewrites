import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def tcp(st):
    client.connect(("127.0.0.1", 8000))
    while True:
        data_bytes = client.recv(1024*1024*1024*1024)
        data_text = data_bytes.decode('utf-8', errors='replace')
        m = json.loads(data_text)
        st.session_state.messages.append(m)
        with st.chat_message(m["user"]):
            if m["type"] == "video":
                st.video(m["content"])
            elif m["type"] == "image":
                st.image(m["content"])
            elif m["type"] == "audio":
                st.audio(m["content"])
    