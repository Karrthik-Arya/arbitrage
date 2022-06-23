import streamlit as st
import pandas as pd
import numpy as np
from scrape import find_the_trades

st.title('The Arbitrage Bot')
st.write(" ------ ")


def main():
    ex_1 = st.sidebar.selectbox("Please select the exchange", ['kcs','wazirx', 'binance', 'coindcx', 'wazirx'], key='1')
    ex_2 = st.sidebar.selectbox("Please select the exchange", ['wazirx','kcs', 'binance', 'coindcx', 'wazirx'], key='2')
    trades = find_the_trades(ex_1, ex_2)
    st.write("Arbitrage is possible for the following coins:")
    st.write(trades)


main()
