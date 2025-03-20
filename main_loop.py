import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import random
import string
import os
# import re
# import bcrypt
from dashboard import Dashboard
from customer import Customer
from database import *
from transaction import *
from common import *

user=Customer()

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

dashboard = Dashboard()


def main_menu():

    user.log_menu()


if __name__ == "__main__" :
    main_menu()
    root.mainloop()

        
