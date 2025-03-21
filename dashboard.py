import customtkinter as ctk
from dotenv import load_dotenv
import random
import string
from database import *
from common import *
from CTkMessagebox import CTkMessagebox


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

class Dashboard:
    def __init__(self):
        self.user_id = None
        self.balance = 0
        self.accounts = []
        self.selected_account_id = None

    def get_user_info(self):
        """Récupère les comptes de l'utilisateur"""
        cursor.execute("""
            SELECT user.id, user.first_name, user.name 
            FROM user
            WHERE user.id = %s
        """, (self.user_id,))
        user_info = cursor.fetchone()

        #test connexion id
        print(f"User ID: {self.user_id}")

        if user_info:
            self.user_id, self.first_name, self.name = user_info

            # Récupère tous les comptes avec ID et type
            cursor.execute("""
                SELECT id, type, balance FROM account WHERE user_id = %s
            """, (self.user_id,))
            self.accounts = cursor.fetchall()

            # Définit le premier compte comme sélectionné par défaut
            if self.accounts:
                self.selected_account_id = self.accounts[0][0]  # ID du premier compte
        else:
            self.user_id, self.first_name, self.name, self.accounts = None, None, None, []

    def update_account_info(self, choice):
        """Met à jour le solde et les transactions lorsqu'on change de compte"""
        selected_type = self.account_options.get()  # Récupère le type sélectionné

        # Associe le type de compte sélectionné à son ID
        for acc_id, acc_type, balance in self.accounts:
            if acc_type.capitalize() == selected_type:  # Compare avec la liste des comptes
                self.selected_account_id = acc_id
                self.balance_label.configure(text=f"Solde : {balance}€")
                self.display_transactions()
                break

    def add_savings_account(self):
        """Ajoute un compte épargne"""
        iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, self.user_id, "epargne"))

        mydb.commit()

        self.get_user_info()  # Rafraîchir les comptes

        success_label = ctk.CTkLabel(root, text="Compte épargne ajouté avec succès !", text_color="green", font=("Arial", 14))
        success_label.pack(pady=10)

        self.display_dashboard()  # Rafraîchir l'affichage

    def display_dashboard(self):
        """Affiche les informations de l'utilisateur et ses comptes"""
        self.get_user_info()
        clear_screen()

        if self.accounts:
            # Créer le menu déroulant avec les types de compte
            self.account_options = ctk.CTkComboBox(root, 
                                                   values=[acc_type.capitalize() for _, acc_type, _ in self.accounts],
                                                   command=self.update_account_info)
            self.account_options.place(relx=0.5, rely=0.2, anchor="center")
            self.account_options.set(self.accounts[0][1].capitalize())  # Sélection par défaut

            self.welcome = ctk.CTkLabel(root, text=f"Welcome {self.first_name} {self.name}", font=("Arial", 18))
            self.welcome.place(relx=0.5, rely=0.1, anchor="center")
            # Affichage du solde du compte sélectionné
            acc_id, acc_type, balance = self.accounts[0]
            self.balance_label = ctk.CTkLabel(root, text=f"Solde : {balance}€", font=("Arial", 16))
            self.balance_label.place(relx=0.5, rely=0.3, anchor="center")

            # Afficher les transactions
            self.display_transactions()

            # Bouton pour ajouter un compte épargne
            add_savings_button = ctk.CTkButton(root, text="Ajouter un compte épargne", command=self.confirm_action)
            add_savings_button.place(relx=0.5, rely=0.5, anchor="center")
        else:
            error_label = ctk.CTkLabel(root, text="Aucun compte trouvé.", text_color="red", font=("Arial", 16))
            error_label.place(relx=0.5, rely=0.4, anchor="center")

        back_button = ctk.CTkButton(root, text="Retour")
        back_button.place(relx=0.5, rely=0.7, anchor="center")

    def display_transactions(self):
        """Affiche les transactions du compte sélectionné"""
        cursor.execute("""
            SELECT date, description, reference, category.name
            FROM transaction
            JOIN category ON transaction.category_id = category.id
            WHERE transaction.type_id = %s
            ORDER BY date DESC
        """, (self.selected_account_id,))
        transactions = cursor.fetchall()

        # Efface la liste précédente des transactions
        for widget in root.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Solde" not in widget.cget("text"):
                widget.destroy()

        # Maintient le menu déroulant et le solde
        self.account_options.place(relx=0.5, rely=0.2, anchor="center")
        self.balance_label.place(relx=0.5, rely=0.3, anchor="center")

        if transactions:
            y_pos = 0.4
            for date, description, reference, category_name in transactions:
                transaction_text = f"{date} - {description} ({category_name}) - Réf: {reference}"
                trans_label = ctk.CTkLabel(root, text=transaction_text, font=("Arial", 12))
                trans_label.place(relx=0.5, rely=y_pos, anchor="center")
                y_pos += 0.05
        else:
            no_transaction_label = ctk.CTkLabel(root, text="Aucune transaction trouvée.", font=("Arial", 12))
            no_transaction_label.place(relx=0.5, rely=0.4, anchor="center")

    def confirm_action(self):
        msg = CTkMessagebox(title="Confirm", message="Do you really want to create a new account ?", icon="question", option_1="Yes", option_2="No")
        if msg.get() == "Yes":
            self.add_savings_account()
        else:
            CTkMessagebox(title="Canceled", message="Action canceled")
