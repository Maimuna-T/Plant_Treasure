import tkinter as tk
from tkinter import messagebox
import mysql.connector
from conn import create_connection 

from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import os
import subprocess

class UserWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")
        self.root.geometry("1600x800+00+00")
        self.root.config(bg="#daf7da")
         #title
        title=Label(self.root,text="User Registration",font=("Arial", 40, "bold"), bg="white", fg="#024B44").place(x=10,y=15,width=1510,height=70)

        # ---------- Input Fields ----------       

        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_name.place(x=100, y=200, width=200, height=35)
        self.name_entry = tk.Entry(self.root,font=("arial", 20))
        self.name_entry.place(x=300, y=200, width=300, height=35)

        lbl_email = Label(self.root, text="Email:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_email.place(x=100, y=300, width=200, height=35)
        self.email_entry = tk.Entry(self.root,font=("arial", 20))
        self.email_entry.place(x=300, y=300, width=300, height=35)

        lbl_pass = Label(self.root, text="Password:", font=("goudy old style", 20, "bold"), bg="#daf7da")
        lbl_pass.place(x=100, y=400, width=200, height=35)
        self.pass_entry = tk.Entry(self.root, show="*",font=("arial", 20))
        self.pass_entry.place(x=300, y=400, width=300, height=35)

        tk.Button(root, text="Register", font=("goudy old style", 20, "bold"),command=self.register_user,bg="#14BC84",fg="white").place(x=120, y=500, width=150, height=40)
        # Exit Button (closes
        tk.Button(self.root, text="Exit", font=("goudy old style", 20, "bold"), command=self.root.destroy, bg="#F08080", fg="white").place(x=100, y=690, width=150, height=40)
    # ==== image
        img_path = "E:\\L3S1\\softwareproject\\plant_buyers.png"
        if os.path.exists(img_path):
            try:
                bg = Image.open(img_path)
                bg = bg.resize((750, 400), Image.LANCZOS)
                self.bg_img = ImageTk.PhotoImage(bg)
                # keep reference self.bg_img so it isn't garbage-collected
                self.lbl_bg = Label(self.root, image=self.bg_img)
                self.lbl_bg.place(x=700, y=200, width=750, height=400)
            except Exception as e:
                print("Error loading image:", e)
        else:
            print(f"Image not found at: {img_path}")

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
