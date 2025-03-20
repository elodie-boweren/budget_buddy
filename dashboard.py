import customtkinter as ctk
from dotenv import load_dotenv
# import mysql.connector
import random
import string
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
        """Gets customer's accounts"""
        cursor.execute("""
            SELECT user.id, user.first_name, user.name 
            FROM user
            WHERE user.id = %s
        """, (self.user_id,))
        user_info = cursor.fetchone()

        if user_info:
            self.user_id, self.first_name, self.name = user_info

            # gets every accounts
            cursor.execute("""
                SELECT id, type, balance, iban FROM account WHERE user_id = %s
            """, (self.user_id,))
            self.accounts = cursor.fetchall()
        else:
            self.user_id, self.first_name, self.name, self.accounts = None, None, None, []


    def get_transactions(self):
        """Gets transaction list"""
        cursor.execute("""
            SELECT transaction.date, transaction.description, transaction.reference, category.name 
            FROM transaction
            JOIN category ON transaction.category_id = category.id
            JOIN account ON account.id = transaction.type_id
            WHERE account.user_id = %s
            ORDER BY transaction.date DESC
        """, (self.user_id,))
        return cursor.fetchall()
    
    def add_savings_account(self):
        """add a savings account to customer"""
        iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, self.user_id, "epargne"))
        
        mydb.commit()

        self.get_user_info()

        success_label = ctk.CTkLabel(root, text="Compte épargne ajouté avec succès !", text_color="green", font=("Arial", 14))
        success_label.pack(pady=10)

        # Refresh dashboard
        self.display_dashboard()

    

    def display_dashboard(self):
        """Show customers infos"""
        self.get_user_info()
        
        clear_screen()

        for acc_id, acc_type, balance, iban in self.accounts:
            acc_label = ctk.CTkLabel(root, text=f"Compte {acc_type.capitalize()} ({iban}) : {balance}€", font=("Arial", 14))
            acc_label.pack(pady=5)

        if self.user_id:
            # Print name and balance
            welcome_label = ctk.CTkLabel(root, text=f"Bienvenue {self.first_name} {self.name}", font=("Arial", 18))
            welcome_label.pack(pady=5)
            
            balance_label = ctk.CTkLabel(root, text=f"Votre solde actuel : {self.balance}€", font=("Arial", 16))
            balance_label.pack(pady=5)

            add_savings_button = ctk.CTkButton(root, text="Ajouter un compte épargne", command=self.add_savings_account)
            add_savings_button.pack(pady=5)


            # print transactions
            transactions = self.get_transactions()
            if transactions:
                transaction_label = ctk.CTkLabel(root, text="Historique des transactions :", font=("Arial", 14))
                transaction_label.pack(pady=5)

                for transaction in transactions:
                    date, description, reference, category_name = transaction
                    transaction_text = f"{date} - {description} ({category_name}) - Réf: {reference}"
                    trans_label = ctk.CTkLabel(root, text=transaction_text, font=("Arial", 12))
                    trans_label.pack()

            else:
                no_transaction_label = ctk.CTkLabel(root, text="Aucune transaction trouvée.", font=("Arial", 12))
                no_transaction_label.pack()
        
        else:
            error_label = ctk.CTkLabel(root, text="Utilisateur introuvable.", text_color="red", font=("Arial", 16))
            error_label.pack(pady=10)
        
        back_button = ctk.CTkButton(root, text="Retour")
        back_button.pack(pady=20)

