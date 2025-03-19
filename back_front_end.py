import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import random
import string
import os
import re
import bcrypt

load_dotenv("./.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

admin_email = ["Budgetbuddy1@laplateforme.io","Budgetbuddy2@laplateforme.io","Budgetbuddy3@laplateforme.io","Budgetbuddy4@laplateforme.io","Budgetbuddy5@laplateforme.io"]

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("800x600")


iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

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

class User():
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def correct_password(self, password):
        correct_password = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z\d0-9@$!%*?&]{10,}$')
        if correct_password.match(password):
            return True
        return False
    

    def info_check(self):
        self.email = ctk.CTkEntry(root, placeholder_text = "Email")
        self.email.place(relx = 0.5, rely = 0.45, anchor = "center")
        self.password = ctk.CTkEntry(root, placeholder_text = "password")
        self.password.place(relx = 0.5, rely = 0.5, anchor = "center")

        def validate():
            email = self.email.get()
            password = self.password.get()
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            if cursor.fetchone():
                print("This email is already taken, please choose another one.")
            elif not self.correct_password(password):
                print("Invalid password, please try another one.")

        validate_button = ctk.CTkButton(root, text="Submit", command=validate)
        validate_button.place(relx=0.5, rely=0.55, anchor="center")

    def create_account(self):
        self.name = ctk.CTkEntry(root, width = 220, placeholder_text="Surname")
        self.firstname = ctk.CTkEntry(root, width = 220, placeholder_text="Firstname")
        self.email = ctk.CTkEntry(root, width = 220, placeholder_text="Email")
        self.password = ctk.CTkEntry(root, width = 220, placeholder_text="Password", show="*")

        self.name.place(relx=0.5, rely=0.35, anchor="center")
        self.firstname.place(relx=0.5, rely=0.4, anchor="center")
        self.email.place(relx=0.5, rely=0.45, anchor="center")
        self.password.place(relx=0.5, rely=0.5, anchor="center")

        self.show_password = ctk.BooleanVar(value=False)
        self.show_password_checkbox = ctk.CTkCheckBox(root, text="Show", variable=self.show_password, command=self.toggle_password_visibility)
        self.show_password_checkbox.place(relx=0.7, rely=0.5, anchor="center")

        def submit():
            name = self.name.get()
            firstname = self.firstname.get()
            email = self.email.get()
            password = self.password.get()
    
            error_label = ctk.CTkLabel(root, text="", text_color="red")
            error_label.place(relx=0.5, rely=0.7, anchor="center")

            if not name or not firstname or not email or not password:
                error_label.configure(text="All fields must be complete.")
                return

            if not self.correct_password(password):
                error_label.configure(text="Invalid password.")
                return

            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            if cursor.fetchone():
                error_label.configure(text="This email is already in use.")
                return

            #protect password:
            salt = bcrypt.gensalt()
            bytes = password.encode('utf-8')
            hash_password = bcrypt.hashpw(bytes, salt)
            
            cursor.execute("""
                INSERT INTO user (name, first_name, email, password)
                VALUES (%s, %s, %s, %s)
            """, (name, firstname, email, hash_password))
            mydb.commit()

            cursor.execute("SELECT id FROM user WHERE email = %s",(email,))
            id_user_create = cursor.fetchone()

            cursor.execute("""
            INSERT INTO account (balance, iban, user_id)
            VALUES (%s, %s, %s)
            """, (0, iban, id_user_create[0]))
            mydb.commit()

            error_label.configure(text="Your account was created successfully", text_color="green")
            main_menu()

        submit_button = ctk.CTkButton(root, text="Submit", command=submit)
        submit_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(root, text="Back", command=main_menu)
        back_button.place(relx=0.5, rely=0.65, anchor="center")
            
    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def log_in(self):
        clear_screen()

        self.enter_email = ctk.CTkEntry(root, placeholder_text="Email")
        self.enter_password = ctk.CTkEntry(root, placeholder_text="Password", show="*")

        self.enter_email.place(relx=0.5, rely=0.4, anchor="center")
        self.enter_password.place(relx=0.5, rely=0.5, anchor="center")

        error_label = ctk.CTkLabel(root, text="", text_color="red")
        error_label.place(relx=0.5, rely=0.7, anchor="center")

        self.show_password = ctk.BooleanVar(value=False)
        self.show_password_checkbox = ctk.CTkCheckBox(root, text="Show", variable=self.show_password, command=self.toggle_password_visibility)
        self.show_password_checkbox.place(relx=0.65, rely=0.5, anchor="center")

        def validate():
            email = self.enter_email.get()
            entered_password = self.enter_password.get()

            cursor.execute("SELECT id, password FROM user WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            if result: 
                user_id, hash_password = result
                userBytes = entered_password.encode('utf-8')
                if bcrypt.checkpw(userBytes, hash_password.encode('utf-8')):
                    error_label.configure(text="Connected!", text_color="green")
                    root.update()
                    if email in admin_email:
                        admin_menu()
                    else:
                        user_menu()
                else:
                    error_label.configure(text="Wrong password.", text_color="red")
            else:
                error_label.configure(text="Email not found.", text_color="red")

        validate_button = ctk.CTkButton(root, text="Submit", command=validate)
        validate_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(root, text="Back", command=main_menu)
        back_button.place(relx=0.5, rely=0.7, anchor="center")

user = User()

def user_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Utilisateur")
    label.pack(pady=10)

def admin_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Administrateur")
    label.pack(pady=10)

class Transaction():
    def __init__(self):
        cursor.execute("SELECT id FROM user WHERE email = %s", (user.email))
        self.user_id = cursor.fetchall()
        cursor.execute("SELECT balance FROM amount WHERE user_id = %s", (self.user_id) )
        self.user_balance = cursor.fetchall()
    def deposit(self, amount):
        self.amount = amount
        new_balance = self.user_balance + self.amount
        cursor.execute("UPDATE accout SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
        mydb.commit()
        self.user_balance = new_balance

    def withdrawal(self, amount):
        self.amount = amount
        new_balance = self.user_balance - self.amount
        cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (new_balance, self.user_id))
        mydb.commit()
        self.user_balance = new_balance

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


if __name__ == "__main__" :
    main_menu()
    root.mainloop()

        
#bcrypt
