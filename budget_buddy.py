import mysql.connector
from dotenv import load_dotenv
import os
import pygame
import sys
import re

load_dotenv("c:/Users/arnau/Documents/La Plateforme/SQL/.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

table_user = """
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE,
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

    def correct_password(self, password):
        correct_password = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$')
        if correct_password.match(password):
            return True
        return False
    
    def enter_password(self):
        while True:
            self.passw =int(input("Enter your password :"))
            if self.correct_password(self.passw):
                cursor.execute("""
                    INSERT INTO user (name, first_name, username, email, password)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (self.name, self.first_name, self.username, self.email , self.passw))
                mydb.commit()
            else :
                print("Invalide password, please try an other one")
                self.enter_password()

    def enter_username(self):
        while True :
            cursor.execute("SELECT * FROM user WHERE username = %s", (self.username,))
            if cursor.fetchone():
                print("This username is already taken, please choose another one.")
                self.enter_username()
            else :
                break

    def create_account(self):
        self.name = int(input("Enter your name :"))
        self.first_name =int(input("Enter your first name:"))
        self.username = int(input("Enter your username :"))

        self.enter_username()
        
        self.email = int(input("Enter your email :"))

        self.enter_password()

        cursor.execute("""
            INSERT INTO user (name, first_name, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.name, self.first_name, self.username, self.email , self.passw))
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
            self.connect_user()

