import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
# import random
# import string
# import os
# import re
import bcrypt
from database import *
from common import *
from config import *


class Transaction():
    def __init__(self):
        
        cursor.execute("SELECT id FROM user WHERE email = %s", (user_email))
        self.user_id = cursor.fetchone()[0]
        cursor.execute("SELECT balance FROM amount WHERE user_id = %s", (self.user_id) )
        self.user_balance = cursor.fetchone()[0]

    def deposit(self, amount):
        amount = ctk.CTkEntry(root, placeholder_text = "Amount")
        amount.place(relx = 0.5, rely = 0.45, anchor = "center")
        self.amount = amount
        new_balance = self.user_balance + self.amount
        cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
        mydb.commit()
        self.user_balance = new_balance

    def withdrawal(self, amount):
        amount = ctk.CTkEntry(root, placeholder_text = "Amount")
        amount.place(relx = 0.5, rely = 0.45, anchor = "center")
        self.amount = amount
        new_balance = self.user_balance - self.amount
        cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
        mydb.commit()
        self.user_balance = new_balance

    def transfer(self):
        amount = ctk.CTkEntry(root, placeholder_text = "Amount")
        amount.place(relx = 0.5, rely = 0.5, anchor = "center")

        iban = ctk.CTkEntry(root, placeholder_text = "IBAN")
        iban.place(relx = 0.5, rely = 0.6, anchor = "center")
    
        cursor.execute("SELECT iban from account")
        iban_list = [cursor.fetchall]
        if iban in iban_list :
            cursor.execute("SELECT id FROM user WHERE iban = %s", (iban,))
            self.outcoming_name = cursor.fetchone()[0]
            cursor.execute("SELECT balance FROM account WHERE user_id = %s", (self.outcoming_name))
            self.outcoming_balance = cursor.fetchone()[0]
            cursor.execute("SELECT balance FROM account WHERE user_id = %s", (self.user_id))
            self.balance = cursor.fetchall()
            if self.balance > amount :
                self.balance -= amount
                self.outcoming_balance += amount
                cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.balance, self.user_id))
                cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.outcoming_balance, self.outcoming_name))
                mydb.commit()
