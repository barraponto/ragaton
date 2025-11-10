from audiorecorder import audiorecorder
import streamlit as st

from eleven import generate_speech
from st_utils import agent_loader

agent = agent_loader()

"""
# Ragaton Voice Assistant
Ask anything via voice and get the answer.
"""

audio = audiorecorder("Ask anything via voice", "Click to stop recording")
if audio:
    with st.spinner("Listening..."):
        for index, message in enumerate(agent.query_audio(audio)):
            if index:
                st.chat_message("assistant").write(message)
                with generate_speech(message) as path:
                    st.audio(path)
            else:
                st.chat_message("user").write(message)
