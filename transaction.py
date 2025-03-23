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


class Transaction():
    def __init__(self, user_id):
        # cursor.execute("SELECT id FROM user WHERE email = %s", (self.email))
        self.user_id = user_id
        cursor.fetchall()
        cursor.execute("SELECT balance FROM account WHERE user_id = %s", (self.user_id,) )
        self.user_balance = cursor.fetchall()
    
    def deposit(self):
        clear_screen()

        entry_amount = ctk.CTkEntry(root, width=220, placeholder_text="How much do you want to deposit ?")
        entry_amount.place(relx=0.5, rely=0.4, anchor="center")

        def validate_deposit():
            self.amount = self.enter_amount.get()
            new_balance = self.user_balance + self.amount
            cursor.execute("UPDATE accout SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
            mydb.commit()
            self.user_balance = new_balance

        validate_button = ctk.CTkButton(root, text="Deposit", command =lambda: validate_deposit())
        validate_button.place(relx=0.5, rely=0.5, anchor = "center")

    def withdrawal(self):
        clear_screen()

        entry_withdrawal = ctk.CTkEntry(root, width=220, placeholder_text="How much do you want to withdraw ?")
        entry_withdrawal.place(relx=0.5, rely=0.4, anchor="center")

        def validate_withdrawal():
            self.amount = self.entry_withdrawal
            new_balance = self.user_balance - self.amount
            cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
            mydb.commit()
            self.user_balance = new_balance

        validate_button = ctk.CTkButton(root, text="Deposit", command =lambda: validate_withdrawal())
        validate_button.place(relx=0.5, rely=0.5, anchor = "center")

    def display_transaction(self):
        clear_screen()

        deposit_button = ctk.CTkButton(root, text="Make a deposit", command=self.deposit)
        deposit_button.place(relx=0.5, rely=0.3, anchor="center")

        withdrawal_button = ctk.CTkButton(root, text="Make a withdrawal", command=self.withdrawal)
        withdrawal_button.place(relx=0.5, rely=0.4)

        
    #def outcoming_transfert(self):
        #amount = int(input ("Insert amount to transfert :"))
        #iban = input ("Enter IBAN : ")
        #cursor.execute("SELECT iban from account")
        #iban_list = [cursor.fetchall]
        #if iban in iban_list :
            #cursor.execute("SELECT id FROM user WHERE iban = %s", (iban,))
            #self.outcoming_name = cursor.fetchone()[0]
            #cursor.execute("SELECT balance FROM account WHERE user_id = %s", (self.outcoming_name))
            #self.outcoming_balance = cursor.fetchone()[0]
            #cursor.execute("SELECT balance FROM account WHERE user_id = %s", (self.user_id))
            #self.balance = cursor.fetchall()
            #if self.balance > amount :
                #self.balance -= amount
                #self.outcoming_balance += amount
                #cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.balance, self.user_id))
                #cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.outcoming_balance, self.outcoming_name))
                #mydb.commit()
