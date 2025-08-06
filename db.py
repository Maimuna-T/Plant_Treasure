import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def connect_db():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="plant_treasury"  # তোমার ডাটাবেজের নাম
        )
        return conn
    except Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None
