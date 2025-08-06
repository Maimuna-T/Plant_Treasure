import tkinter as tk
from tkinter import ttk
from conn import create_connection


def fetch_store_data():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Plant_Name, Quantity FROM store")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def store_window():
    win = tk.Tk()
    win.title("Store Inventory")
    win.geometry("500x400")
    win.configure(bg="#f0fff0")

    cols = ("ID", "Plant Name", "Quantity")
    tree = ttk.Treeview(win, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    # Load data
    data = fetch_store_data()
    for row in data:
        tree.insert("", tk.END, values=row)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    win.mainloop()

if __name__ == "__main__":
    store_window()
