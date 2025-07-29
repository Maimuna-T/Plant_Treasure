print("Main file running...")

import tkinter as tk
from buy import add_buy
from sell import add_sell
from view_tables import view_table
from database import init_db

# Initialize DB
init_db()

# GUI
root = tk.Tk()
root.title("Plant Treasure")
root.geometry("400x300")

tk.Label(root, text="Plant Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Price").pack()
entry_price = tk.Entry(root)
entry_price.pack()

tk.Label(root, text="Quantity").pack()
entry_qty = tk.Entry(root)
entry_qty.pack()

# Buy button
tk.Button(root, text="Buy", command=lambda: add_buy(entry_name.get(),
                                                   float(entry_price.get()),
                                                   int(entry_qty.get()))).pack(pady=5)

# Sell button
tk.Button(root, text="Sell", command=lambda: add_sell(entry_name.get(),
                                                     float(entry_price.get()),
                                                     int(entry_qty.get()))).pack(pady=5)

# View buttons
tk.Button(root, text="View Buy Table", command=lambda: view_table("buy")).pack(pady=5)
tk.Button(root, text="View Sell Table", command=lambda: view_table("sell")).pack(pady=5)
tk.Button(root, text="View Store Table", command=lambda: view_table("store")).pack(pady=5)

print("Tkinter window should now open")

root.mainloop()
