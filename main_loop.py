import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from dashboard import Dashboard
from customer import Customer
from database import *
from transaction import Transaction
from common import *

# load variables
load_dotenv("../.env")

# Connect to the database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD"),
        database="budget_buddy"
    )
    cursor = mydb.cursor(buffered=True)
    print("Connexion to the database successful!")
except mysql.connector.Error as err:
    print(f"Problem connecting to the database: {err}")
    exit(1)

# Interface
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

# Main window
root = init_root("900x700")
root.title("Budget Buddy - Your financial ally")

def main():
    """Main function to run programme"""
    # Initiate the user
    customer = Customer()
   
    # Display log-in page
    customer.log_menu()

if __name__ == "__main__":
    main()
    root.mainloop()