import streamlit as st
from sec_data import show_all_companies

st.set_page_config(
    'Fundamentalytics',
    page_icon='favicon.png'
)

company = st.selectbox(
    '',
    show_all_companies(),
    None,
    placeholder='Choose a company',
    label_visibility='collapsed'
)

st.write('You selected:', company)