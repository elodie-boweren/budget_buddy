import mysql.connector
from dotenv import load_dotenv
import os
import customtkinter
import matplotlib.pyplot as plt
import numpy as np

load_dotenv("./.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy",
    autocommit = False
)

cursor = mydb.cursor()

table_user = """
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100)
)
"""
cursor.execute(table_user)
mydb.commit()


table_account = """
CREATE TABLE IF NOT EXISTS account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    balance INT NOT NULL,
    iban VARCHAR(34) NOT NULL,
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
)
"""
cursor.execute(table_account)
mydb.commit()


table_type = """
CREATE TABLE IF NOT EXISTS type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    deposit INT NOT NULL,
    withdrawal INT NOT NULL,
    incoming_transfert INT NOT NULL,
    outcoming_transfert INT NOT NULL
)
"""
cursor.execute(table_type)
mydb.commit()


table_category = """
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)
"""
cursor.execute(table_category)
mydb.commit()


table_transaction = """
CREATE TABLE IF NOT EXISTS transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    description VARCHAR(100) NOT NULL,
    reference VARCHAR(100) NOT NULL,
    type_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (type_id) REFERENCES type(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
)
"""
cursor.execute(table_transaction)

mydb.commit()

# customers = """
# INSERT IGNORE INTO user (name, first_name, email, password)
#     VALUES("Dupont", "Pierre", "pierre.dupont@email.com", "p@ssw0rd123"),
#     ("Martin", "Sophie", "sophie.martin@email.com", "S0ph!eM2025"),
#     ("Durand", "Julien", "julien.durand@email.com", "Jule$$1234"),
#     ("Lefevre", "Emma", "emma.lefevre@email.com", "Emm@2025!"),
#     ("Moreau", "Lucas", "lucas.moreau@email.com", "Luc@z456"),
#     ("Rousseau", "Clara", "clara.rousseau@email.com", "C1araR0ck$")
# """
# cursor.execute(customers)
# mydb.commit()

# accounts = """
# INSERT IGNORE INTO account(iban)
#     VALUES("FR76 3000 6000 0112 3456 7890 189"),
#     ("FR18 2004 1000 0501 2345 6789 013"),
#     ("FR92 1010 7000 0123 4567 8910 567"),
#     ("FR41 3078 8000 0400 1234 5678 901"),
#     ("FR62 3007 6070 0112 3456 7890 234"),
#     ("FR83 2004 1010 0520 4567 8910 678")"""

# cursor.execute(accounts)
# mydb.commit()
