import streamlit as st
from util import session_state, reload_messages, prompt

if name := st.text_input("Hãy nhập tên của bạn"):
    session_state(st)
    reload_messages(st)
    prompt(name, st)