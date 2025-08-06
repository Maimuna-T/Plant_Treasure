import tkinter as tk
from tkinter import ttk, messagebox
from conn import create_connection

class BuyWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Buy Plants")
        self.root.geometry("600x400")

        # ---------- Input Fields ----------
        tk.Label(root, text="Plant Name:").grid(row=0, column=0, padx=10, pady=5)
        self.plant_name_entry = tk.Entry(root)
        self.plant_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Price:").grid(row=1, column=0, padx=10, pady=5)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(root, text="Submit", command=self.insert_data, bg="green", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

        # Show Table Button
        tk.Button(root, text="Show Table", command=self.show_table, bg="blue", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

        # Treeview for Display
        self.tree = ttk.Treeview(root, columns=("ID", "Plant_Name", "Price", "Quantity", "Total"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Plant_Name", text="Plant Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total", text="Total")

        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # -------- Insert Data into Database --------
    def insert_data(self):
        name = self.plant_name_entry.get()
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
