import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
import sys
import re

load_dotenv("./.env")

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

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("800x600")



def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def main_menu():
    clear_screen()

    label = ctk.CTkLabel(root, text = "Budget Buddy")
    label.pack(pady=10)

    button1 = ctk.CTkButton(root, text="Sign in", command = user.log_in)
    button2 = ctk.CTkButton(root, text = "Sign up", command = user.create_account)

    button1.place(relx = 0.5, rely = 0.4, anchor = "center")
    button2.place(relx = 0.5, rely = 0.6, anchor = "center")

def user_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Utilisateur")
    label.pack(pady=10)

def admin_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Administrateur")
    label.pack(pady=10)

# class Transaction():
#     def __init__(self):
#         cursor.execute("SELECT id FROM user WHERE email = %s", (user.email))
#         self.user_id = cursor.fetchall()
#         cursor.execute("SELECT balance FROM amount WHERE user_id = %s", (self.user_id) )
#         self.user_balance = cursor.fetchall()
#     def deposit(self, amount):
#         self.amount = amount
#         new_balance = self.user_balance + self.amount
#         cursor.execute("UPDATE accout SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
#         mydb.commit()
#         self.user_balance = new_balance

#     def withdrawal(self, amount):
#         self.amount = amount
#         new_balance = self.user_balance - self.amount
#         cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
#         mydb.commit()
#         self.user_balance = new_balance

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

class Dashboard:
    def __init__(self, user_email):
        self.user_email = user_email
        self.user_id = None
        self.balance = 0

    def get_user_info(self):
        """Récupère l'ID et le solde de l'utilisateur"""
        cursor.execute("""
            SELECT user.id, user.first_name, user.name, account.balance 
            FROM user
            JOIN account ON user.id = account.user_id
            WHERE user.email = %s
        """, (self.user_email,))
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

    def display_dashboard(self):
        """Affiche les informations utilisateur et les transactions"""
        self.get_user_info()
        
        clear_screen()

        if self.user_id:
            # Affichage du nom et du solde
            welcome_label = ctk.CTkLabel(root, text=f"Bienvenue {self.first_name} {self.name}", font=("Arial", 18))
            welcome_label.pack(pady=10)
            
            balance_label = ctk.CTkLabel(root, text=f"Votre solde actuel : {self.balance}€", font=("Arial", 16))
            balance_label.pack(pady=10)

            # Affichage des transactions
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
        
        back_button = ctk.CTkButton(root, text="Retour", command=user_menu)
        back_button.pack(pady=20)


dashboard = Dashboard("%s")

class User():
    def __init__(self, email=None, passw=None):
        self.email = email
        self.passw = passw

    def correct_password(self, passw):
        correct_password = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z\d0-9@$!%*?&]{10,}$')
        if correct_password.match(passw):
            return True
        return False
    

    def info_check(self):
        self.email = ctk.CTkEntry(root, placeholder_text = "Email")
        self.email.place(relx = 0.5, rely = 0.45, anchor = "center")
        self.passw = ctk.CTkEntry(root, placeholder_text = "password")
        self.passw.place(relx = 0.5, rely = 0.5, anchor = "center")

        def validate():
            email = self.email.get()
            password = self.passw.get()
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            if cursor.fetchone():
                print("This email is already taken, please choose another one.")
            elif not self.correct_password(password):
                print("Invalid password, please try another one.")

        validate_button = ctk.CTkButton(root, text="Validate", command=validate)
        validate_button.place(relx=0.5, rely=0.55, anchor="center")


    def create_account(self):
        self.name = ctk.CTkEntry(root, placeholder_text="Surname")
        self.firstname = ctk.CTkEntry(root, placeholder_text="Firstname")
        self.email = ctk.CTkEntry(root, placeholder_text="Email")
        self.passw = ctk.CTkEntry(root, placeholder_text="Password", show="*")

        self.name.place(relx=0.5, rely=0.35, anchor="center")
        self.firstname.place(relx=0.5, rely=0.4, anchor="center")
        self.email.place(relx=0.5, rely=0.45, anchor="center")
        self.passw.place(relx=0.5, rely=0.5, anchor="center")

        def submit():
            name = self.name.get()
            firstname = self.firstname.get()
            email = self.email.get()
            password = self.passw.get()
    
            error_label = ctk.CTkLabel(root, text="", text_color="red")
            error_label.place(relx=0.5, rely=0.7, anchor="center")

            if not name or not firstname or not email or not password:
                error_label.configure(text="Tous les champs doivent être remplis.")
                return

            if not self.correct_password(password):
                error_label.configure(text="Mot de passe invalide.")
                return

            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            if cursor.fetchone():
                error_label.configure(text="Cet email est déjà utilisé.")
                return

            cursor.execute("""
                INSERT INTO user (name, first_name, email, password)
                VALUES (%s, %s, %s, %s)
            """, (name, firstname, email, password))
            mydb.commit()
            error_label.configure(text="Compte créé avec succès !", text_color="green")
            main_menu()

        submit_button = ctk.CTkButton(root, text="Submit", command=submit)
        submit_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(root, text="Back", command=main_menu)
        back_button.place(relx=0.5, rely=0.65, anchor="center")
            

    def log_in(self):
        clear_screen()

        self.enter_email = ctk.CTkEntry(root, placeholder_text="Email")
        self.enter_password = ctk.CTkEntry(root, placeholder_text="Password", show="*")

        self.enter_email.place(relx=0.5, rely=0.4, anchor="center")
        self.enter_password.place(relx=0.5, rely=0.5, anchor="center")

        # def validate():
        #     email = self.enter_email.get()
        #     password = self.enter_password.get()

        #     cursor.execute("SELECT id, password FROM user WHERE email = %s", (email,))
        #     result = cursor.fetchone()

        #     error_label = ctk.CTkLabel(root, text="", text_color="red")
        #     error_label.place(relx=0.5, rely=0.7, anchor="center")

        #     if result:
        #         user_id, user_password = result
        #         if password == user_password:
        #             error_label.configure(text="Connexion réussie !", text_color="green")
        #             if email in admin_email:
        #                 admin_menu()
        #             else:
        #                 user_menu()
        #         else:
        #             error_label.configure(text="Mot de passe incorrect.", text_color="red")
        #     else:
        #         error_label.configure(text="Email non trouvé.", text_color="red")

        validate_button = ctk.CTkButton(root, text="Confirm", command=dashboard.display_dashboard)
        validate_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(root, text="Back", command=main_menu)
        back_button.place(relx=0.5, rely=0.7, anchor="center")

user = User()

if __name__ == "__main__" :
    main_menu()
    root.mainloop()

        
#bcrypt
