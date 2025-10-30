
import tkinter as tk
from tkinter import ttk, messagebox
from conn import create_connection
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import os
#import subprocess

class BuyWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Buy Plants")
        self.root.geometry("1600x800+00+00")
        #self.root.attributes('-fullscreen', True)
        #self.root.state('zoomed')
        
        self.root.config(bg="#daf7da")
         #title
        title=Label(self.root,text=" Buy Plants! ",font=("Arial", 40, "bold"), bg="#024B44", fg="white").place(x=15,y=15,width=1500,height=55)

        # ---------- Input Fields ----------       
        lbl_plantname = Label(self.root, text="Plant Name:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_plantname.place(x=100, y=200, width=200, height=35)
        self.plant_name_entry = tk.Entry(self.root,font=("arial", 20))
        self.plant_name_entry.place(x=300, y=200, width=200, height=35)

        lbl_price = Label(self.root, text="Price:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_price.place(x=100, y=300, width=200, height=35)
        self.price_entry = tk.Entry(self.root,font=("arial", 20))
        self.price_entry.place(x=300, y=300, width=200, height=35)

        lbl_quantity = Label(self.root, text="Quantity:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_quantity.place(x=100, y=400, width=200, height=35)
        self.quantity_entry = tk.Entry(self.root,font=("arial", 20))
        self.quantity_entry.place(x=300, y=400, width=200, height=35)

        '''# --- Search Bar ---
        search_frame = tk.Frame(self.root, bg="#cbf0d0")
        search_frame.place(x=400, y=100, width=350, height=40)
        tk.Label(search_frame, text="🔍 Search Plant:", bg="#cbf0d0",font=("Goudy Old Style", 16, "bold")).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("times new roman", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(search_frame, text="Search", bg="#66bb6a", fg="white",font=("times new roman", 11, "bold"), cursor="hand2",command=self.search_plant).pack(side=tk.LEFT, padx=10)
        '''
        # Submit Button
        tk.Button(self.root, text="Submit",font=("goudy old style", 20, "bold"), command=self.insert_data, bg="#14BC84", fg="white").place(x=100, y=550, width=150, height=40)

        # Show Table Button
        tk.Button(self.root, text="Show Table",font=("goudy old style", 20, "bold"), command=self.show_table, bg="teal", fg="white").place(x=750, y=200, width=150, height=40)
        
        # Exit Button 
        tk.Button(self.root, text="Exit", font=("goudy old style", 20, "bold"), command=self.root.destroy, bg="#F08080", fg="white").place(x=100, y=690, width=150, height=40)

        # Treeview for Display
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Plant_Name", "Price", "Quantity", "Total"),
            show='headings'
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Plant_Name", text="Plant Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total", text="Total")

        # Set column widths for better layout
        self.tree.column("ID", width=50)
        self.tree.column("Plant_Name", width=150)
        self.tree.column("Price", width=100)
        self.tree.column("Quantity", width=100)
        self.tree.column("Total", width=100)

        # Use .place() instead of .grid()
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('goudy old style', 20), rowheight=30)  # table data font
        style.configure("mystyle.Treeview.Heading", font=('goudy old style', 20, 'bold'))  # heading font

        self.tree.place(x=750, y=300, width=650, height=400)
        # Load table initially
        self.show_table()

    

    # -------- Insert Data into Database --------
    def insert_data(self):
        name = self.plant_name_entry.get().strip().capitalize()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if not name or not price or not quantity:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            price = int(price)
            quantity = int(quantity)
            total = price * quantity

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO buy (Plant_Name, Price, Quantity, Total) VALUES (%s, %s, %s, %s)",
                           (name, price, quantity, total))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Data inserted successfully!")
            self.clear_entries()
            self.show_table()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # -------- Show Data in Treeview --------
    def show_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buy")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        conn.close()

    #search 
    def search_plant(self):
        search_term = self.search_entry.get().strip().lower()
        conn = create_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute("SELECT * FROM store WHERE LOWER(Plant_Name) LIKE %s", (f"%{search_term}%",))
        else:
            cursor.execute("SELECT * FROM store")
        rows = cursor.fetchall()
        conn.close()

        # Clear previous data
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))

    # -------- Clear Entry Fields --------
    def clear_entries(self):
        self.plant_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


# ----------- Run This File Directly -----------
if __name__ == "__main__":
    root = tk.Tk()
    app = BuyWindow(root)
    root.mainloop()
