import mysql.connector
from dotenv import load_dotenv
import os
import customtkinter as ctk

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
    id INT AUTO_INCREMENT PRIMARY KEY,
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
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM("current", "savings")
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
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    type ENUM("deposit", "withdrawal", "transfer"),
    description VARCHAR(100) NOT NULL,
    category ENUM("food", "house", "transport", "leasure", "health", "education")
)
"""
cursor.execute(table_transaction)
mydb.commit()

