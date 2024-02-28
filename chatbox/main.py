import streamlit as st
from ws import ws, websocket
from threading import Thread

Thread(target=websocket, args=(st,)).start()

if name := st.text_input("Hãy nhập tên của bạn"):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        user = st.chat_message(m["user"])
        if m["type"] == "text":
            user.write(m["content"])
        elif m["type"] == "video":
            user.video(m["content"], height=60)
        elif m["type"] ==  "image":
            user.image(m["content"], height=60)
        elif m["type"] == "audio":
            user.audio(m["content"])
           
    if text := st.chat_input("Write"):
        msg = {"user": name, "content": text, "type": "text"}
        st.session_state.messages.append(msg)
        ws.send(str(msg))
        with st.chat_message(name):
            st.write(text)