import streamlit as st
from sec_data import get_all_companies, get_company_facts

st.set_page_config(
    'Fundamentalytics',
    page_icon='favicon.png'
)

company = st.selectbox(
    '',
    get_all_companies(),
    None,
    placeholder='Choose a company',
    label_visibility='collapsed',
)

if company is not None:
    temp = company.split(' ')
    ticker, title, cik_str = temp[0], ' '.join(temp[1:-1]), temp[-1]

    st.write('# ', title)
    st.write(ticker, cik_str)

    all_facts = get_company_facts(cik_str)
    for key, value in all_facts['facts'].items():
        st.write('##' + value['label'])
        st.write(value['unit'] + value['description'])
        st.dataframe(value['data'])