import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt
from datetime import datetime
import random
import string

# Chargement des variables d'environnement
load_dotenv()

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

# Fenêtre principale
root = ctk.CTk()
root.geometry("900x600")
ctk.set_appearance_mode("dark")

class BudgetBuddy:
    def __init__(self):
        self.user_id = None
        self.show_login()

    def clear_screen(self):
        for widget in root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        
        label = ctk.CTkLabel(root, text="Connexion à Budget Buddy", font=("Arial", 20))
        label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(root, width=300, placeholder_text="Email")
        self.email_entry.pack(pady=5)
        self.password_entry = ctk.CTkEntry(root, width=300, placeholder_text="Mot de passe", show="*")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(root, text="Se connecter", command=self.login)
        login_button.pack(pady=10)

        register_button = ctk.CTkButton(root, text="Créer un compte", command=self.show_register)
        register_button.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        cursor.execute("SELECT id, password FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            self.user_id = user[0]
            self.show_dashboard()
        else:
            error_label = ctk.CTkLabel(root, text="Email ou mot de passe incorrect", text_color="red")
            error_label.pack()

    def show_dashboard(self):
        self.clear_screen()
        label = ctk.CTkLabel(root, text=f"Bienvenue !", font=("Arial", 20))
        label.pack(pady=20)
        
        cursor.execute("SELECT balance, iban FROM account WHERE user_id = %s", (self.user_id,))
        account_info = cursor.fetchone()
        balance_text = f"Solde : {account_info[0]} €" if account_info else "Aucun compte trouvé"
        balance_label = ctk.CTkLabel(root, text=balance_text, font=("Arial", 16))
        balance_label.pack(pady=10)

        iban_text = f"IBAN : {account_info[1]}" if account_info else "Pas d'IBAN attribué"
        iban_label = ctk.CTkLabel(root, text=iban_text, font=("Arial", 14))
        iban_label.pack(pady=5)
        
        deposit_button = ctk.CTkButton(root, text="Déposer de l'argent", command=self.deposit_money)
        deposit_button.pack(pady=10)
        
        transfer_button = ctk.CTkButton(root, text="Effectuer un transfert", command=self.transfer_money)
        transfer_button.pack(pady=10)
        
        logout_button = ctk.CTkButton(root, text="Déconnexion", command=self.show_login)
        logout_button.pack()
    
    def deposit_money(self):
        self.clear_screen()
        amount_entry = ctk.CTkEntry(root, width=300, placeholder_text="Montant à déposer")
        amount_entry.pack(pady=5)

        def confirm_deposit():
            amount = float(amount_entry.get())
            cursor.execute("UPDATE account SET balance = balance + %s WHERE user_id = %s", (amount, self.user_id))
            mydb.commit()
            self.show_dashboard()
        
        confirm_button = ctk.CTkButton(root, text="Confirmer", command=confirm_deposit)
        confirm_button.pack(pady=10)
    
    def transfer_money(self):
        self.clear_screen()
        iban_entry = ctk.CTkEntry(root, width=300, placeholder_text="IBAN du destinataire")
        iban_entry.pack(pady=5)
        amount_entry = ctk.CTkEntry(root, width=300, placeholder_text="Montant à transférer")
        amount_entry.pack(pady=5)

        def confirm_transfer():
            recipient_iban = iban_entry.get()
            amount = float(amount_entry.get())
            cursor.execute("SELECT id FROM account WHERE iban = %s", (recipient_iban,))
            recipient = cursor.fetchone()
            
            if recipient:
                recipient_id = recipient[0]
                cursor.execute("UPDATE account SET balance = balance - %s WHERE user_id = %s", (amount, self.user_id))
                cursor.execute("UPDATE account SET balance = balance + %s WHERE id = %s", (amount, recipient_id))
                mydb.commit()
                self.show_dashboard()
        
        confirm_button = ctk.CTkButton(root, text="Confirmer", command=confirm_transfer)
        confirm_button.pack(pady=10)

app = BudgetBuddy()
root.mainloop()
