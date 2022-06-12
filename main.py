import streamlit as st
import pandas as pd
import numpy as np
from scrape import find_the_trades

st.title('The Arbitrage Bot')
st.write(" ------ ")


def main():
    trades = find_the_trades()
    st.write("Arbitrage is possible for the following coins:")
    st.write(trades)


main()
