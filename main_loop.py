import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from dashboard import Dashboard
from customer import Customer
from database import *
from transaction import Transaction
from common import AppManager

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

def main():
    """Main function to run programme"""
    # Initialize the AppManager instead of using init_root
    app_manager = AppManager("900x700")
    
    # Initiate the user
    customer = Customer(app_manager=app_manager)
    customer.log_menu()
    
    # Start the main loop
    app_manager.get_root().mainloop()

if __name__ == "__main__":
    main()