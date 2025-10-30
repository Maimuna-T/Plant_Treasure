import tkinter as tk
from tkinter import ttk
from conn import create_connection
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import os


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
    win.geometry("1600x800+00+00")
    win.configure(bg="#e8f5e9")

    title_label = tk.Label(
        win,
        text="🌱 Current Store Inventory 🌱 ",
        font=("Helvetica", 18, "bold"),
        bg="#e8f5e9",
        fg="#2e7d32"
    )
    title_label.pack(pady=15)

    # ---------- Table Styling ----------
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#f9fff9",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="#f9fff9",
                    font=("Segoe UI", 11))
    style.configure("Treeview.Heading",
                    background="#388e3c",
                    foreground="white",
                    font=("Segoe UI", 12, "bold"))
    style.map('Treeview', background=[('selected', '#a5d6a7')])

    # Create Treeview
    cols = ("ID", "Plant Name", "Quantity")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)

    # Add striped row tags
    tree.tag_configure('oddrow', background="#f1f8e9")
    tree.tag_configure('evenrow', background="#ffffff")

    # Insert data
    data = fetch_store_data()
    for i, row in enumerate(data):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=row, tags=(tag,))

    # Scrollbar
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    # Close button
    tk.Button(
        win,
        text="Close",
        command=win.destroy,
        bg="#66bb6a",
        fg="white",
        font=("Helvetica", 12, "bold"),
        relief="flat",
        padx=20,
        pady=5,
        activebackground="#43a047"
    ).pack(pady=15)

    win.mainloop()


if __name__ == "__main__":
    store_window()
