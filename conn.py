import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # পাসওয়ার্ড যদি সেট করা থাকে তাহলে এখানে দাও
            database="plant_treasury"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
