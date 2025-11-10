from audiorecorder import audiorecorder
import streamlit as st

from st_utils import agent_loader

agent = agent_loader()

"""
# Ragaton Voice Assistant
Ask anything via voice and get the answer.
"""

audio = audiorecorder("Ask anything via voice", "Click to stop recording")
if audio:
    st.audio(audio.export().read())

    with st.spinner("Listening..."):
        for index, message in enumerate(agent.query_audio(audio)):
            if index:
                st.chat_message("assistant").write(message)
            else:
                st.chat_message("user").write(message)
