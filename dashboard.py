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
from transaction import *

transaction = Transaction()

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

class Dashboard:
    def __init__(self):
        self.user_id = None
        self.balance = 0

    def get_user_info(self):
        """Récupère l'ID et le solde de l'utilisateur"""
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
        """Récupère la liste des transactions de l'utilisateur"""
        cursor.execute("""
            SELECT transaction.date, transaction.description, transaction.reference, category.name 
            FROM transaction
            JOIN category ON transaction.category_id = category.id
            JOIN account ON account.id = transaction.type_id
            WHERE account.user_id = %s
            ORDER BY transaction.date DESC
        """, (self.user_id,))
        return cursor.fetchall()
    
    def make_transaction(self):
        clear_screen()

        self.enter_date = ctk.CTkEntry(root, width=220, placeholder_text="Date")
        self.enter_description = ctk.CTkEntry(root, width=220, placeholder_text="Description")
        self.enter_reference = ctk.CTkEntry(root, width=220, placeholder_text="Reference")
        
        list_type = ["Deposit", "Withdrawal", "Transfer"]
        self.enter_type = ctk.CTkComboBox(root, width=220, values=list_type)
        self.enter_type.set("Type")
        
        list_category = ["Leisure", "Food", "Housing", "Transportation", "Health", "Education", "Other"]
        self.enter_category = ctk.CTkComboBox(root, width=220, values=list_category)
        self.enter_category.set("Category")

        self.enter_date.place(relx=0.5, rely=0.3, anchor="center")
        self.enter_description.place(relx=0.5, rely=0.4, anchor="center")
        self.enter_reference.place(relx=0.5, rely=0.5, anchor="center")
        self.enter_type.place(relx=0.5, rely=0.6, anchor="center")
        self.enter_category.place(relx=0.5, rely=0.7, anchor="center")
    
        error_label = ctk.CTkLabel(root, text="", text_color="red")
        error_label.place(relx=0.5, rely=0.75, anchor="center")

        def validate():
            date = self.enter_date.get()
            description = self.enter_description.get()
            reference = self.enter_reference.get()
            entered_type = self.enter_type.get()
            category = self.enter_category.get()

            if not all([date, description, reference, entered_type, category]):
                error_label.configure(text="All fields are required!")
            else :
                if entered_type == "Deposit":
                    transaction.deposit()
                    back_button = ctk.CTkButton(root, text="Back", command = self.make_transaction)
                    back_button.place(relx = 0.5, rely = 0.7, anchor = "center")

                if entered_type == "Withdrawal":
                    transaction.withdrawal()
                    back_button = ctk.CTkButton(root, text="Back", command = self.make_transaction)
                    back_button.place(relx = 0.5, rely = 0.7, anchor = "center")

                if entered_type == "Transfer" :
                    transaction.transfer()
                    back_button = ctk.CTkButton(root, text="Back", command = self.make_transaction)
                    back_button.place(relx = 0.5, rely = 0.7, anchor = "center")

        validate_button = ctk.CTkButton(root, text="Validate", command = validate)
        back_button = ctk.CTkButton(root, text="Back", command = self.display_dashboard)
        validate_button.place(relx = 0.5, rely = 0.8, anchor = "center")
        back_button.place(relx = 0.5, rely = 0.9, anchor = "center")
            

    def display_dashboard(self):
        """Affiche les informations utilisateur et les transactions"""
        self.get_user_info()
        
        clear_screen()

        if self.user_id:
            welcome_label = ctk.CTkLabel(root, text=f"Bienvenue {self.first_name} {self.name}", font=("Arial", 18))
            welcome_label.pack(pady=10)
            
            balance_label = ctk.CTkLabel(root, text=f"Votre solde actuel : {self.balance}€", font=("Arial", 16))
            balance_label.pack(pady=10)

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
        
        transaction_button = ctk.CTkButton(root, text="Make a transaction", command=self.make_transaction)
        transaction_button.place(relx=0.5, rely=0.7, anchor="center")

        back_button = ctk.CTkButton(root, text="Disconnect")
        back_button.place(relx=0.5, rely=0.9, anchor="center")

