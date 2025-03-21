import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import random
import string
import os
# import re
# import bcrypt
from customer import Customer
from database import *
from common import *

user = Customer()

load_dotenv("c:/Users/arnau/Documents/La Plateforme/SQL/.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")


def main_menu():
    clear_screen()
    create_account = ctk.CTkButton(root, text="Create account", command=user.create_account)
    create_account.place(relx=0.5, rely=0.5, anchor="center")

    log_in = ctk.CTkButton(root, text="Log in", command=user.log_in)
    log_in.place(relx=0.5, rely=0.6, anchor="center")
    

if __name__ == "__main__" :
    main_menu()
    root.mainloop()        
