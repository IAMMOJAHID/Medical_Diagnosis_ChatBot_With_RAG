
import streamlit as st
import time
from app import process_answer

# with st.container():
    # st.title("Welcome To Medical Diagnosis Chatbot")
    # st.write("Note: This ChatBot is in developing face. Clearly input your problem (ChartBot may not recognize partial question)")

st.write(
    """
    <div>
        <h2 style="text-align: center;">Welcome To Medical Diagnosis Chatbot</h2>
        <p style="text-align: center;">Note: We are in developing face. Input multiple symptoms.</p>
    </div>
    """,
    unsafe_allow_html=True
)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

ModelOutput=""""""
def stream_data():
    for word in ModelOutput.split(" "):
        yield word + " "
        time.sleep(0.02)
        
        
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if(prompt=="""Hi""" or prompt=="""hi""" or prompt=="""Hello""" or prompt=="""hello"""):
            ModelOutput="""Hi, Let me know your symptoms if you experiencing any. I'll predict the disease based on them. In serious case, Concern with healthcare professionals experienced."""
        else:
            ModelOutput, Generator=process_answer(prompt)

        response = st.write_stream(stream_data)
    st.session_state.messages.append({"role": "assistant", "content": response})
