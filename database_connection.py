import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="your_host",  # Replace with your database host
            user="your_username",  # Replace with your database username
            password="your_password",  # Replace with your database password
            database="your_database_name"  # Replace with your database name
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def add_user(username, password, email, role):
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, email, role))
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
