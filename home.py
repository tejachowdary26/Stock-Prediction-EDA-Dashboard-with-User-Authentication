import urllib
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from database_connection import create_connection, check_user
from authentication import hash_password

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/Lakshya-Ag/Streamlit-Dashboard/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

def main():
    connection = create_connection()
    st.sidebar.title("User Authentication")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Login"):
            if check_user(connection, username, hash_password(password)):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.sidebar.success("Logged In Successfully as " + username)
            else:
                st.sidebar.error("Incorrect Username or Password")

    if st.session_state['logged_in']:
        st.sidebar.success("Logged In as " + st.session_state['username'])
        box = st.selectbox("Information", ["Stock Market Info", "Covid-19 impact"])
        if box == "Stock Market Info":
            st.markdown(get_file_content_as_string("README.md"))
        elif box == "Covid-19 impact":
            display_covid_impact()

def display_covid_impact():
    st.header("Impact of COVID-19 on Indian Stock Market")
    df1 = pd.read_csv("data nifty50.csv", index_col='Date', parse_dates=True)
    fig = go.Figure(data=[go.Candlestick(x=df1.index,
                                         open=df1['Open'],
                                         high=df1['High'],
                                         low=df1['Low'],
                                         close=df1['Close'],
                                         name='Market Data')])
    fig.update_layout(
        title='Nifty 50 volatility in 2020',
        yaxis_title='Stock Price (in Rs.)', width=800, height=550)
    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector=dict(
                         buttons=list([
                             dict(count=30, label="30D", step="day", stepmode="backward"),
                             dict(count=60, label="60D", step="day", stepmode="backward"),
                             dict(count=90, label="90D", step="day", stepmode="backward"),
                             dict(count=180, label="180D", step="day", stepmode="backward"),
                             dict(count=270, label="270D", step="day", stepmode="backward"),
                             dict(step="all")
                         ])
                     ))
    st.plotly_chart(fig)
    st.markdown(get_file_content_as_string("Covid.md"))

if __name__ == "__main__":
    main()
