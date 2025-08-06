import tkinter as tk
from tkinter import messagebox
import mysql.connector
from conn import create_connection  # নিশ্চিত করো conn.py-তে create_connection আছে

class UserWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")

        tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=1, column=1)

        tk.Label(root, text="Password").grid(row=2, column=0, padx=10, pady=5)
        self.pass_entry = tk.Entry(root, show="*")
        self.pass_entry.grid(row=2, column=1)

        tk.Button(root, text="Register", command=self.register_user).grid(row=3, columnspan=2, pady=10)

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.pass_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO user (Name, Email, Password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = UserWindow(root)
    root.mainloop()
