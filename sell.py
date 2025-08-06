import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="plant_treasury"   # তোমার DB নাম
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


class SellWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sell Product")
        self.root.geometry("400x400")

        # Plant Name
        tk.Label(root, text="Plant Name").pack(pady=5)
        self.plant_name_entry = tk.Entry(root)
        self.plant_name_entry.pack(pady=5)

        # Price
        tk.Label(root, text="Price").pack(pady=5)
        self.price_entry = tk.Entry(root)
        self.price_entry.pack(pady=5)

        # Quantity
        tk.Label(root, text="Quantity").pack(pady=5)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack(pady=5)

        # Submit button
        tk.Button(root, text="Submit", command=self.insert_data).pack(pady=10)

        # Show button
        tk.Button(root, text="Show Data", command=self.show_data).pack(pady=10)

        # Text box for showing data
        self.output_box = tk.Text(root, width=40, height=10)
        self.output_box.pack(pady=10)

    # Insert data into 'sell' table
    def insert_data(self):
        plant_name = self.plant_name_entry.get()
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

    # Show sell table
    def show_data(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sell")
                rows = cursor.fetchall()

                self.output_box.delete("1.0", tk.END)  # Clear previous text
                for row in rows:
                    self.output_box.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}, Qty: {row[3]}, Total: {row[4]}\n")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SellWindow(root)
    root.mainloop()
