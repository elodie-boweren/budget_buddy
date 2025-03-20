import customtkinter as ctk
from dotenv import load_dotenv
# import mysql.connector
# import random
# import string
# import os
# import re
# import bcrypt
from database import *
from common import *


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

class Dashboard:
    def __init__(self):
        self.user_id = None
        self.balance = 0

    def get_user_info(self):
        """gets id and user balance"""
        cursor.execute("""
            SELECT user.id, user.first_name, user.name, account.balance 
            FROM user
            JOIN account ON user.id = account.user_id
            WHERE user.id = %s
        """, (self.user_id,))
        user_info = cursor.fetchone()

        if user_info:
            self.user_id, self.first_name, self.name, self.balance = user_info
        else:
            self.user_id, self.first_name, self.name, self.balance = None, None, None, 0

    def get_transactions(self):
        """gets the user's list of transactionsr"""
        cursor.execute("""
            SELECT transaction.date, transaction.description, transaction.reference, category.name 
            FROM transaction
            JOIN category ON transaction.category_id = category.id
            JOIN account ON account.id = transaction.type_id
            WHERE account.user_id = %s
            ORDER BY transaction.date DESC
        """, (self.user_id,))
        return cursor.fetchall()

    def display_dashboard(self):
        """Displays user's balance and information"""
        self.get_user_info()
        
        clear_screen()

        if self.user_id:
            # Affichage du nom et du solde
            welcome_label = ctk.CTkLabel(root, text=f"Welcome {self.first_name} {self.name}", font=("Arial", 18))
            welcome_label.pack(pady=10)
            
            balance_label = ctk.CTkLabel(root, text=f"Your current balance : {self.balance}€", font=("Arial", 16))
            balance_label.pack(pady=10)

            # Affichage des transactions
            transactions = self.get_transactions()
            if transactions:
                transaction_label = ctk.CTkLabel(root, text="Past transactions :", font=("Arial", 14))
                transaction_label.pack(pady=5)

                for transaction in transactions:
                    date, description, reference, category_name = transaction
                    transaction_text = f"{date} - {description} ({category_name}) - Réf: {reference}"
                    trans_label = ctk.CTkLabel(root, text=transaction_text, font=("Arial", 12))
                    trans_label.pack()

            else:
                no_transaction_label = ctk.CTkLabel(root, text="No transaction.", font=("Arial", 12))
                no_transaction_label.pack()
        
        else:
            error_label = ctk.CTkLabel(root, text="Customer not found.", text_color="red", font=("Arial", 16))
            error_label.pack(pady=10)
        
        back_button = ctk.CTkButton(root, text="Back")
        back_button.pack(pady=20)

