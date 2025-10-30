import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # if password has saved
            database="plant_treasury"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
