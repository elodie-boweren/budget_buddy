import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from dashboard import Dashboard
from customer import Customer
from database import *
from transaction import *
from common import *

user=Customer()

load_dotenv("../.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

dashboard = Dashboard()

# def log_menu():
#     user.log_in()

if __name__ == "__main__" :
    user.log_menu()
    root.mainloop()        