import streamlit as st
from util import session_state, reload_messages, prompt
from bot import Bot

bot = Bot()
bot.run()
bot = bot.instance()

if name := st.text_input("Hãy nhập tên của bạn"):
    session_state(st)
    reload_messages(st)
    prompt(name, st)