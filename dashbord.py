import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from conn import create_connection
import os
import subprocess
from buy import BuyWindow
 
class PT:
    def __init__(self,root):
        self.root=root
        self.root.title("Plant Treasury - Home")
        self.root.attributes('-fullscreen', True)
        
       # self.root.geometry("1350x700+50+50")
        self.root.configure(bg="#daf7da")
        
        #title
        title=Label(self.root,text="Plant Treasury ...!!!",padx=0, font=("goudy old style", 40, "bold"), bg="#cbf0d0", fg="#024B44").place(x=0,y=20,relwidth=1,height=100)

        #menu
        M_frame=LabelFrame(self.root,text="Categories 🌿",font=("goudy old style", 20, "bold"), bg="#cbf0d0",fg="#024B44")
        M_frame.place(x=50,y=190,width=270,height=400)
        btn_USER=Button(M_frame,text="User Log-in",font=("Arial", 15, "bold"),bd=5,relief=RIDGE,bg="white", fg="black",command=self.add_user).place(x=30,y=50,width=200,height=40)
        btn_BUY=Button(M_frame, text="Purchase Plants",font=("Arial", 15, "bold"),bd=5,relief=RIDGE,bg="white", fg="black", command=self.add_buy).place(x=30,y=110,width=200,height=40)
        btn_SELL=Button(M_frame, text="Supply Plants", font=("Arial", 15, "bold"),bd=5,relief=RIDGE,bg="white", fg="black",command=self.add_sell).place(x=30,y=170,width=200,height=40)
        btn_STORE=Button(M_frame, text="Treasure of Plants",font=("Arial", 15, "bold"),bd=5,relief=RIDGE,bg="white", fg="black",command=self.add_store).place(x=30,y=230,width=200,height=40)
        
        
        #btn_EXIT = Button(M_frame,text="Exit",font=("Arial", 15, "bold"),bg="red",fg="white",command=self.root.destroy)
        #btn_EXIT.place(x=20, y=500, width=180, height=40)
        # Exit Button 


        tk.Button(self.root, text="Exit", font=("goudy old style", 20, "bold"), command=self.root.destroy, bg="#CD5C5C", fg="white").place(x=100, y=690, width=150, height=40)


        # ==== image
        img_path = "E:\\L3S1\\softwareproject\\bg1.png"
        if os.path.exists(img_path):
            try:
                bg = Image.open(img_path)
                bg = bg.resize((950, 400), Image.LANCZOS)
                self.bg_img = ImageTk.PhotoImage(bg)
                # keep reference self.bg_img so it isn't garbage-collected
                self.lbl_bg = Label(self.root, image=self.bg_img)
                self.lbl_bg.place(x=400, y=190, width=950, height=400)
            except Exception as e:
                print("Error loading image:", e)
        else:
            print(f"Image not found at: {img_path}")

        #bottom features
        
        self.lbl_totalplants= Label(self.root,text="Total Plants\n[0]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#E6FFB3")
        self.lbl_totalplants.place(x=400,y=650,width=400,height=100)
        self.lbl_totalusers= Label(self.root,text="Total Users\n[0]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#038074")
        self.lbl_totalusers.place(x=900,y=650,width=400,height=100)
        self.update_totals()
        
    def update_totals(self):
        conn = create_connection()  # your DB connection function
        cur = conn.cursor()
        
        # count total plants
        cur.execute("SELECT SUM(Quantity) FROM store")
        total_plants = cur.fetchone()[0] or 0  # if no rows, return 0

        # count total users
        cur.execute("SELECT COUNT(*) FROM user")   # or your table name
        total_users = cur.fetchone()[0]

        # update label text
        self.lbl_totalplants.config(text=f"Total Plants\n[{total_plants}]")
        self.lbl_totalusers.config(text=f"Total Users\n[{total_users}]")

        conn.close()  

    def add_buy(self):
        subprocess.Popen(['python', r'E:\L3S1\softwareproject\buy.py'])

    def add_sell(self):
        subprocess.Popen(['python', r'E:\L3S1\softwareproject\sell.py'])

    def add_store(self):
        subprocess.Popen(['python', r'E:\L3S1\softwareproject\store.py'])

    def add_user(self):
        subprocess.Popen(['python', r'E:\L3S1\softwareproject\user.py'])

if __name__ == "__main__":
    root=Tk()
    obj=PT(root)
    root.mainloop()

