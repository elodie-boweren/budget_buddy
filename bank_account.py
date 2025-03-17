import mysql.connector
from dotenv import load_dotenv
import os
import pygame
import sys

load_dotenv("c:/Users/arnau/Documents/La Plateforme/SQL/.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="bank_account"
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
    iban VARCHAR(100) NOT NULL,
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


class User():
    def __init__(self, username, passw):
        self.username = username 
        self.passw = passw
    def create_account(self):
        self.username = int(input("Enter your username :"))
        self.passw =int(input("Enter your password :"))
        cursor.execute("""
            INSERT INTO user (name, first_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (self.username, "First Name", "email@example.com", self.passw))
        mydb.commit()

    def connect_user(self):
        cursor.execute("SELECT id, password FROM user WHERE name = %s", (self.username,))
        result = cursor.fetchone()
        if result : 
            user_id = result[0]
            passw = result[1]
            if self.username == "admin":
                cursor.execute("SELECT * FROM account")
                accounts = cursor.fetchall()
            else :
                cursor.execute("SELECT * FROM account WHERE user_id = %s", (user_id,))
                accounts = cursor.fetchall()
        else : 
            print("Wrong password, try again")


user = User()
user.create_account()