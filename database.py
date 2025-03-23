import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("../.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor(buffered=True)

# Table creation
# User table
table_user = """
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
)
"""
cursor.execute(table_user)
mydb.commit()

# Account table
table_account = """
CREATE TABLE IF NOT EXISTS account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0,
    iban VARCHAR(34) NOT NULL,
    user_id INT NOT NULL,
    type VARCHAR(50) DEFAULT 'courant',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
)
"""
cursor.execute(table_account)
mydb.commit()

# Category table
table_category = """
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)
"""
cursor.execute(table_category)
mydb.commit()

# Check if categories exist
cursor.execute("SELECT COUNT(*) FROM category")
category_count = cursor.fetchone()[0]

# If no category exists, create one by default
if category_count == 0:
    default_categories = [
        "Food", "Housing", "Transport", "Leisure", 
        "Health", "Education", "Wages", "Gifts", "Other"
    ]
    for category in default_categories:
        cursor.execute("INSERT INTO category (name) VALUES (%s)", (category,))
    mydb.commit()

# Transaction table
table_transaction = """
CREATE TABLE IF NOT EXISTS transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    description VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    reference VARCHAR(100) NOT NULL,
    account_id INT NOT NULL,
    category_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'incoming_transfer', 'outgoing_transfer') NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id)
)
"""
cursor.execute(table_transaction)
mydb.commit()

# Check if administrators exist
cursor.execute("SELECT COUNT(*) FROM user WHERE is_admin = 1")
admin_count = cursor.fetchone()[0]

# Create an admin by default if none exist
if admin_count == 0:
    import bcrypt
    default_password = "Admin@2023"
    hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute("""
        INSERT INTO user (name, first_name, email, password, is_admin)
        VALUES (%s, %s, %s, %s, %s)
    """, ("Admin", "Budget Buddy", "budgetbuddy@laplateforme.io", hashed_password, True))
    mydb.commit()