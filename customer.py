import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import random
import string
import os
import re
import bcrypt
from dashboard import Dashboard
from database import *
from common import *


iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
admin_email = ["Budgetbuddy1@laplateforme.io","Budgetbuddy2@laplateforme.io","Budgetbuddy3@laplateforme.io","Budgetbuddy4@laplateforme.io","Budgetbuddy5@laplateforme.io"]


class Customer():
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
        self.show_password_checkbox = ctk.CTkCheckBox(root, text="Show", variable=self.show_password, command=self.password_visibility)
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
            self.log_menu()

        submit_button = ctk.CTkButton(root, text="Submit", command=submit)
        submit_button.place(relx=0.5, rely=0.6, anchor="center")

<<<<<<< HEAD:back_front_end.py
        back_button = ctk.CTkButton(root, text="Back", command=main_menu)
        back_button.place(relx=0.5, rely=0.65, anchor="center")      
=======
        back_button = ctk.CTkButton(root, text="Back", command=self.log_menu)
        back_button.place(relx=0.5, rely=0.65, anchor="center")
            
>>>>>>> 6608a785699df72385ca84c8e23a4481593d9116:customer.py

    def log_in(self):
        clear_screen()

        self.email = ctk.CTkEntry(root, width = 220, placeholder_text="Email")
        self.password = ctk.CTkEntry(root, width = 220, placeholder_text="Password", show="*")

        self.email.place(relx=0.5, rely=0.4, anchor="center")
        self.password.place(relx=0.5, rely=0.5, anchor="center")

        error_label = ctk.CTkLabel(root, text="", text_color="red")
        error_label.place(relx=0.5, rely=0.7, anchor="center")

        self.show_password = ctk.BooleanVar(value=False)
        self.show_password_checkbox = ctk.CTkCheckBox(root, text="Show", variable=self.show_password, command=self.password_visibility)
        self.show_password_checkbox.place(relx=0.7, rely=0.5, anchor="center")

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
                        dashboard.display_dashboard()
                else:
                    error_label.configure(text="Wrong password.", text_color="red")
            else:
                error_label.configure(text="Email not found.", text_color="red")

        validate_button = ctk.CTkButton(root, text="Submit", command=dashboard.display_dashboard)
        validate_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(root, text="Back", command=self.log_menu)
        back_button.place(relx=0.5, rely=0.65, anchor="center")

<<<<<<< HEAD:back_front_end.py
=======
    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

>>>>>>> 6608a785699df72385ca84c8e23a4481593d9116:customer.py
    def password_visibility(self):
        if self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def log_menu(self):
        clear_screen()

        label = ctk.CTkLabel(root, text = "Budget Buddy")
        label.pack(pady=10)

        button1 = ctk.CTkButton(root, text="Sign in", command = self.log_in)
        button2 = ctk.CTkButton(root, text = "Sign up", command = self.create_account)

        button1.place(relx = 0.5, rely = 0.4, anchor = "center")
        button2.place(relx = 0.5, rely = 0.6, anchor = "center")


<<<<<<< HEAD:back_front_end.py
if __name__ == "__main__" :
    main_menu()
    root.mainloop()

        

=======
user = Customer()
dashboard=Dashboard()
>>>>>>> 6608a785699df72385ca84c8e23a4481593d9116:customer.py
