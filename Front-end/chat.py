import streamlit as st
import time
from send import send_user_input_to_fastapi
from send import take_id_order

def chat():   
    if "id_orders" not in st.session_state or not st.session_state.id_orders:
        st.session_state.id_orders = take_id_order()

    id_orders = st.session_state.id_orders
 
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        initial_bot_message = "Welcome, what can I get you?"
        st.session_state.messages.append({"role": "assistant", "content": initial_bot_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if prompt := st.chat_input("It's nice to meet you!"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        assistant_response = send_user_input_to_fastapi(prompt, id_orders)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
