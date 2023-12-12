import yfinance as yf
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
           host="127.0.0.1",
            user="root",
            passwd="workspace4321",
            database="stockapp"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
def hash_password(password):
    # Using hashlib for password hashing. You can also use bcrypt for more security.
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, email, role):
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO users (username, password, email, role, is_verified, verification_token)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, hashed_password, email, role))
        connection.commit()
        return True
    except Error as e:
        print(f"Error adding new user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def check_user(username, password):
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Error checking user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def fetch_user_role(connection, username):
    try:
        cursor = connection.cursor()
        query = "SELECT role FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"Error fetching user role: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def add_verification_token(username, token):
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "UPDATE users SET verification_token = %s WHERE username = %s"
        cursor.execute(query, (token, username))
        connection.commit()
        return True
    except Error as e:
        print(f"Error updating user with verification token: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def verify_user(token):
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "UPDATE users SET is_verified = True WHERE verification_token = %s"
        cursor.execute(query, (token,))
        affected_rows = cursor.rowcount
        connection.commit()
        return affected_rows > 0
    except Error as e:
        print(f"Error verifying user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def download_and_store_stock_data(connection, symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    cursor = connection.cursor()
    for index, row in data.iterrows():
        cursor.execute(
            "INSERT INTO stock_table (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (symbol, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
        )
    connection.commit()

