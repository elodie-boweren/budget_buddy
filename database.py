import mysql.connector
from dotenv import load_dotenv
import os
import customtkinter as ctk
from datetime import datetime

root = ctk.CTk()
root.geometry("800x600")

load_dotenv("../.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

#create tables
table_user = """
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255)
)
"""
cursor.execute(table_user)
mydb.commit()


table_account = """
CREATE TABLE IF NOT EXISTS account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("current", "savings"),
    balance INT,
    iban VARCHAR(34) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
)
"""
cursor.execute(table_account)
mydb.commit()


table_transaction = """
CREATE TABLE IF NOT EXISTS transaction (
    transaction_ref INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    amount INT NOT NULL,
    type ENUM("deposit", "withdrawal", "transfer"),
    description VARCHAR(100) NOT NULL,
    category ENUM("food", "house", "transport", "leasure", "health", "education"),
    iban VARCHAR(34) NOT NULL
)
"""
# cursor.execute(table_transaction)
# mydb.commit()

transactions = [
("23/03/2025", -350, "deposit", "Birthday present", "leasure", "FRWQETU4NYUKRK"),
("20/03/2025", -50, "withdrawal", "Groceries", "food", "FRWQETU4NYUKRK"),
("18/03/2025", -1000, "transfer", "Rent payment", "house", "FRWQETU4NYUKRK"),
("15/03/2025", +1200, "deposit", "Freelance income", "education", "FRWQETU4NYUKRK"),
("12/03/2025", -100, "withdrawal", "Gasoline", "transport", "FRWQETU4NYUKRK"),
("10/03/2025", +60, "deposit", "Refund from friend", "leasure", "FRWQETU4NYUKRK"),
("08/03/2025", -50, "withdrawal", "Restaurant outing", "food", "FRWQETU4NYUKRK"),
("05/03/2025", -450, "transfer", "Tuition fees", "education", "FRWQETU4NYUKRK"),
("03/03/2025", -200, "withdrawal", "Gym subscription", "health", "FRWQETU4NYUKRK"),
("01/03/2025", +3500, "deposit", "Salary", "house", "FRWQETU4NYUKRK"),
("27/02/2025", -273, "withdrawal", "Electricity bill", "house", "FRWQETU4NYUKRK"),
("25/02/2025", +250, "deposit", "Gift from family", "leasure", "FRWQETU4NYUKRK"),
("22/02/2025", -800, "transfer", "Loan repayment", "house", "FRWQETU4NYUKRK"),
("19/02/2025", -132, "withdrawal", "Car maintenance", "transport", "FRWQETU4NYUKRK"),
("17/02/2025", +650, "deposit", "Investment return", "education", "FRWQETU4NYUKRK"),
("15/02/2025", -25, "withdrawal", "Doctor appointment", "health", "FRWQETU4NYUKRK"),
("13/02/2025", -60, "transfer", "Subscription service", "leasure", "FRWQETU4NYUKRK"),
("11/02/2025", +550, "deposit", "Bonus at work", "house", "FRWQETU4NYUKRK"),
("09/02/2025", -30, "withdrawal", "Cinema tickets", "leasure", "FRWQETU4NYUKRK"),
("07/02/2025", +350, "deposit", "Online course refund", "education", "FRWQETU4NYUKRK")]

for date, amount, trans_type, description, category, iban in transactions:
    formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    query = """
        INSERT INTO transaction (date, amount, type, description, category, iban) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (formatted_date, amount, trans_type, description, category, iban)
    cursor.execute(query, values)
    mydb.commit()


