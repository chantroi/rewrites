#!/usr/bin/bash

cd bot
python -u main.py &
cd ..
cd chatbox
streamlit run main.py --server.port=8080
--server.address=0.0.0.0