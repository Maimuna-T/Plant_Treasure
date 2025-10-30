import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# MySQL connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="plant_treasury"  # name of my data base
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

class SellWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sell Plants")
        self.root.geometry("1600x800+00+00")
        self.root.config(bg="#daf7da")

        # Title
        tk.Label(self.root, text="Sell Plants!", font=("Arial", 40, "bold"), bg="#024B44", fg="white").place(x=15, y=15, width=1500, height=70)

        # Plant Name
        tk.Label(self.root, text="Plant Name:", font=("goudy old style", 20, "bold"), bg="#daf7da")\
            .place(x=100, y=200, width=200, height=35)
        self.plant_name_entry = tk.Entry(self.root,font=("arial", 20))
        self.plant_name_entry.place(x=300, y=200, width=200, height=35)

        # Price
        tk.Label(self.root, text="Price:", font=("goudy old style", 20, "bold"), bg="#daf7da")\
            .place(x=100, y=300, width=200, height=35)
        self.price_entry = tk.Entry(self.root,font=("arial", 20))
        self.price_entry.place(x=300, y=300, width=200, height=35)

        # Quantity
        tk.Label(self.root, text="Quantity:", font=("goudy old style", 20, "bold"), bg="#daf7da")\
            .place(x=100, y=400, width=200, height=35)
        self.quantity_entry = tk.Entry(self.root,font=("arial", 20))
        self.quantity_entry.place(x=300, y=400, width=200, height=35)

        # Submit Button
        tk.Button(self.root, text="Submit", font=("goudy old style", 20, "bold"),
                  command=self.insert_data, bg="#14BC84", fg="white").place(x=100, y=500, width=150, height=40)

        # Show Table Button
        tk.Button(self.root, text="Show Table", font=("goudy old style", 20, "bold"),
                  command=self.show_data,bg="teal", fg="white").place(x=750, y=650, width=150, height=40)

        # Exit Button
        tk.Button(self.root, text="Exit", font=("goudy old style", 20, "bold"),
                  command=self.root.destroy, bg="#F08080", fg="white").place(x=100, y=690, width=150, height=40)

        # Treeview for Sell Table
        self.sell_tree = ttk.Treeview(
            self.root,
            columns=("ID", "Plant_Name", "Price", "Quantity", "Total"),
            show='headings'
        )
        self.sell_tree.heading("ID", text="ID")
        self.sell_tree.heading("Plant_Name", text="Plant Name")
        self.sell_tree.heading("Price", text="Price")
        self.sell_tree.heading("Quantity", text="Quantity")
        self.sell_tree.heading("Total", text="Total")

        # Column widths
        self.sell_tree.column("ID", width=50)
        self.sell_tree.column("Plant_Name", width=150)
        self.sell_tree.column("Price", width=100)
        self.sell_tree.column("Quantity", width=100)
        self.sell_tree.column("Total", width=100)

        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('goudy old style', 20), rowheight=30)  # table data font
        style.configure("mystyle.Treeview.Heading", font=('goudy old style', 20, 'bold'))  # heading font

        # Place Treeview
        self.sell_tree.place(x=700, y=200, width=650, height=400)

    # Insert data into 'sell' table
    def insert_data(self):
        plant_name = self.plant_name_entry.get().strip().capitalize()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if not plant_name or not price or not quantity:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            price = int(price)
            quantity = int(quantity)
            total = price * quantity
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be numbers!")
            return

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Check if plant exists in store
                cursor.execute("SELECT Quantity FROM store WHERE Plant_Name=%s", (plant_name,))
                result = cursor.fetchone()

                if result:
                    current_quantity = result[0]
                    if current_quantity >= quantity:
                        # Insert into sell
                        cursor.execute(
                            "INSERT INTO sell (Plant_Name, Price, Quantity, Total) VALUES (%s,%s,%s,%s)",
                            (plant_name, price, quantity, total)
                        )
                        # Update store
                        cursor.execute(
                            "UPDATE store SET Quantity = Quantity - %s WHERE Plant_Name = %s",
                            (quantity, plant_name)
                        )
                        conn.commit()
                        messagebox.showinfo("Success", "Data inserted into sell table and store updated.")
                    else:
                        messagebox.showerror("Error", f"Not enough stock in store. Current stock: {current_quantity}")
                else:
                    messagebox.showerror("Error", "Plant not found in store table.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    # Show sell data in Treeview
    def show_data(self):
        for row in self.sell_tree.get_children():
            self.sell_tree.delete(row)

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sell")
                rows = cursor.fetchall()
                for row in rows:
                    self.sell_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SellWindow(root)
    root.mainloop()
