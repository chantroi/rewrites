#####
def session_state(st):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = []
       
def reload_messages(st):
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
            
def prompt(name, st):
    if text := st.chat_input("Write"):
        st.session_state.messages.append({"user": name, "content": text})
        with st.chat_message(name):
            st.write(text)
            