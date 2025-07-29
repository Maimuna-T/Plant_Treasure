import tkinter as tk
from tkinter import ttk
from database import get_connection

def view_table(table_name):
    conn, cur = get_connection()
    top = tk.Toplevel()
    top.title(f"{table_name.capitalize()} Table")

    tree = ttk.Treeview(top, columns=("ID", "Name", "Price", "Quantity", "Total"), show="headings")
    tree.pack(fill="both", expand=True)

    for col in ("ID", "Name", "Price", "Quantity", "Total"):
        tree.heading(col, text=col)

    if table_name == "store":
        cur.execute("SELECT id, plant_name, quantity FROM store")
        for row in cur.fetchall():
            tree.insert("", "end", values=(row[0], row[1], "-", row[2], "-"))
    else:
        cur.execute(f"SELECT * FROM {table_name}")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
