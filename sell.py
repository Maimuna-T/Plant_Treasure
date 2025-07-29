from tkinter import messagebox
from database import get_connection

def add_sell(name, price, qty):
    conn, cur = get_connection()
    total = price * qty

    # Check store stock
    cur.execute("SELECT quantity FROM store WHERE plant_name=?", (name,))
    row = cur.fetchone()

    if not row or row[0] < qty:
        messagebox.showerror("Error", "Not enough stock in store!")
        return

    # Insert into sell
    cur.execute("INSERT INTO sell (plant_name, price, quantity, total) VALUES (?, ?, ?, ?)",
                (name, price, qty, total))
    conn.commit()

    # Update store
    cur.execute("UPDATE store SET quantity=? WHERE plant_name=?", (row[0] - qty, name))
    conn.commit()

    messagebox.showinfo("Success", "Plant sold and Store updated!")
