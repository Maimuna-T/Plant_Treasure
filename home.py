import tkinter as tk
from tkinter import ttk

def open_buy():
    import buy
def open_sell():
    import sell
def open_store():
    import store
def open_user():
    import user

def home_window():
    root = tk.Tk()
    root.title("Plant Treasury - Home")
    root.geometry("600x400")
    root.configure(bg="#b2f2bb")

    tk.Label(root, text="Plant Treasury ...!!!", font=("Helvetica", 20, "bold"), bg="#b2f2bb", fg="green").pack(pady=20)

    btn_frame = tk.Frame(root, bg="#b2f2bb")
    btn_frame.pack(pady=20)

    ttk.Button(btn_frame, text="Purchase Plants", command=open_buy).grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(btn_frame, text="Supply Plants", command=open_sell).grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(btn_frame, text="Treasure of Plants", command=open_store).grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(btn_frame, text="Users", command=open_user).grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    home_window()
