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


admin_email = ["Budgetbuddy1@laplateforme.io","Budgetbuddy2@laplateforme.io","Budgetbuddy3@laplateforme.io","Budgetbuddy4@laplateforme.io","Budgetbuddy5@laplateforme.io"]

class User():
    def __init__(self, email, passw):
        self.email = email
        self.passw = passw

    def correct_password(self, passw):
        correct_password = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$')
        if correct_password.match(passw):
            return True
        return False
    

    def info_check(self):
        while True:
            self.email = input("Enter your email :")
            cursor.execute("SELECT * FROM user WHERE email = %s", (self.email,))
            if cursor.fetchone():
                print("This email is already taken, please choose another one.")
                self.info_check()
            else :
                self.passw =input("Enter your password :")
                if self.correct_password(self.passw):
                    cursor.execute("""
                        INSERT INTO user (name, first_name, email, password)
                        VALUES (%s, %s, %s, %s)
                        """, (self.name, self.first_name, self.email , self.passw))
                    mydb.commit()
                else :
                    print("Invalide password, please try an other one")
                    self.info_check()


    def create_account(self):
        self.name = input("Enter your name :")
        self.first_name = input("Enter your first name:")

        self.info_check()

        cursor.execute("""
            INSERT INTO user (name, first_name, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.name, self.first_name, self.email , self.passw))
        mydb.commit()
            

    def log_in(self):
        self.enter_email = input("Enter your email :")
        self.enter_password = input("Enter your password :")
        cursor.execute("SELECT id FROM user WHERE email = %s", (self.enter_email,))
        self.user_id = cursor.fetchall()
        cursor.execute("SELECT password FROM user WHERE email = %s", (self.enter_email,))
        self.user_password = cursor.fetchone()
        cursor.execute("SELECT email FROM user")
        self.list_email = [cursor.fetchall]
        if self.enter_password == self.user_password and self.enter_email in self.list_email:
            if self.email in admin_email :
                cursor.execute("SELECT * FROM account")
                cursor.fetchall()
                mydb.commit()
            else :
                cursor.execute("SELECT * FROM account WHERE user_email = %s", (self.enter_email,))
                cursor.fetchall()
                mydb.commit()
        else : 
            print("Wrong password, try again")
            self.log_in()


user = User()

class Transaction():
    def __init__(self):
        self.user_id = ("SELECT id FROM user WHERE email = %s" (user.email))
        self.user_balance = ("SELECT balance FROM amount WHERE user_id = %s", (self.user_id) )

    def deposit(self, amount):
        self.amount = amount
        new_balance = self.user_balance + self.amount

    def withdrawal(self, amount):
        self.amount = amount
        new_balance = self.user_balance - self.amount

    def outcoming_transfert(self):
        amount = input ("Insert amount to transfert :")
        iban = input ("Enter IBAN : ")
        cursor.execute("SELECT iban from account")
        iban_list = [cursor.fetchall]
        if iban in iban_list :
            cursor.execute("SELECT id FROM user WHERE iban = %s" (iban))
            self.outcoming_name = cursor.fetchall()
            cursor.execute("SELECT balance FROM account WHERE user_id = %s" (self.outcoming_name))
            self.outcoming_balance = cursor.fetchall()
            cursor.execute("SELECT balance FROM account WHERE user_id = %s" (self.user_id))
            self.balance = cursor.fetchall()
            if self.balance > amount :
                self.balance - amount
                self.outcoming_balance + amount


        