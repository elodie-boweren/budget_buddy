import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import random
import string
import os
# import re
# import bcrypt
from dashboard import Dashboard
from user import User
from database import *

user=User()

load_dotenv("./.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

admin_email = ["Budgetbuddy1@laplateforme.io","Budgetbuddy2@laplateforme.io","Budgetbuddy3@laplateforme.io","Budgetbuddy4@laplateforme.io","Budgetbuddy5@laplateforme.io"]

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("800x600")

dashboard = Dashboard()


iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def main_menu():
    clear_screen()

    label = ctk.CTkLabel(root, text = "Budget Buddy")
    label.pack(pady=10)

    button1 = ctk.CTkButton(root, text="Sign in", command = user.log_in)
    button2 = ctk.CTkButton(root, text = "Sign up", command = user.create_account)

    button1.place(relx = 0.5, rely = 0.4, anchor = "center")
    button2.place(relx = 0.5, rely = 0.6, anchor = "center")


def user_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Utilisateur")
    label.pack(pady=10)

def admin_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Administrateur")
    label.pack(pady=10)



if __name__ == "__main__" :
    main_menu()
    root.mainloop()

        
#bcrypt
