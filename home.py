import urllib
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from database_connection import create_connection, check_user
from authentication import hash_password
#import pandas as pd
#import streamlit as st
#import plotly.graph_objs as go
from database_connection import create_connection, check_user, get_stock_data, download_and_store_stock_data
# from authentication import hash_password


# Function to get the content of a file from a URL
def get_file_content_as_string(path):
    try:
        url = 'https://raw.githubusercontent.com/tejachowdary26/Stock-Prediction-EDA-Dashboard-with-User-Authentication/master/' + path
        response = urllib.request.urlopen(url)
        return response.read().decode("utf-8")
    except Exception as e:
        st.error("Error fetching file content: " + str(e))
        return ""

# Function to display stock data
def display_stock_data(stock_symbol):
    connection = create_connection()
    if not connection:
        st.error("Failed to connect to the database.")
        return

    stock_data = get_stock_data(connection, stock_symbol)

    if stock_data:
        # Assuming stock_data is a DataFrame
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'])])
        fig.update_layout(title=f'{stock_symbol} Stock Data', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)
    else:
        # Prompt user for new input
        new_stock_symbol = st.text_input("Enter Stock Symbol", value="AAPL")
        start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
        end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))
        
        if st.button("Fetch and Store Data"):
            download_and_store_stock_data(connection, new_stock_symbol, start_date, end_date)
            st.success("Data downloaded and stored in the database.")

# Main function
def main():
    st.sidebar.title("User Authentication")
    connection = create_connection()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.button("Login"):
            if check_user(connection, username, hash_password(password)):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.sidebar.success(f"Logged In Successfully as {username}")
            else:
                st.sidebar.error("Incorrect Username or Password")

    if st.session_state['logged_in']:
        st.sidebar.success(f"Logged In as {st.session_state['username']}")
        st.title("Stock Market Dashboard")
        stock_symbol = st.text_input("Enter Stock Symbol", value="AAPL")
        display_stock_data(stock_symbol)

if __name__ == "__main__":
    main()
