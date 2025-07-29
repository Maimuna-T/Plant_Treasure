from tkinter import messagebox
from database import get_connection

def add_buy(name, price, qty):
    conn, cur = get_connection()
    total = price * qty

    # Insert into buy
    cur.execute("INSERT INTO buy (plant_name, price, quantity, total) VALUES (?, ?, ?, ?)",
                (name, price, qty, total))
    conn.commit()

    # Update store
    cur.execute("SELECT quantity FROM store WHERE plant_name=?", (name,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE store SET quantity=? WHERE plant_name=?", (row[0] + qty, name))
    else:
        cur.execute("INSERT INTO store (plant_name, quantity) VALUES (?, ?)", (name, qty))
    conn.commit()

    messagebox.showinfo("Success", "Plant added to Buy & Store!")
