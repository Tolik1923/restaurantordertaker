import streamlit as st
from chat import chat
from admin import admin_view

def main():
    st.title("Restaurant Order Taker")
    
    start_chat = st.checkbox("Start Chat")
    admin = st.checkbox("Admin")

    if "id_orders" not in st.session_state:
        st.session_state.id_orders = None

    if start_chat:
        chat()
    
    if admin:
        admin_view()
 
if __name__ == "__main__":
    main()
