import streamlit as st
import pandas as pd
from send import take_ststs

def admin_view():
    st.subheader("The list of all submitted orders")

    s_1, s_2 = take_ststs()

    s_1_str = {key: str(value) for key, value in s_1.items()}

    df = pd.DataFrame.from_dict(s_1_str, orient='index', columns=['-------------------------------------------------Values-------------------------------------------------'])
    st.write(df)

    st.subheader("The general order stats")
  
    s_2_str = {key: str(value) for key, value in s_2.items()}

    df = pd.DataFrame.from_dict(s_2_str, orient='index', columns=['-------------------------------------------------Values-------------------------------------------------'])
    st.write(df)


    