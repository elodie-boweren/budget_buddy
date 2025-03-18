import mysql.connector
from dotenv import load_dotenv
import os
import re
from budget_buddy.connection import App

load_dotenv("./.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

admin_email = ["Budgetbuddy1@laplateforme.io","Budgetbuddy2@laplateforme.io","Budgetbuddy3@laplateforme.io","Budgetbuddy4@laplateforme.io","Budgetbuddy5@laplateforme.io"]

class User():
    def __init__(self, surname, firstname, email, passw):
        self.surname = surname
        self.firstname = firstname
        self.email = email
        self.passw = passw

    def correct_password(self, passw):
        correct_password = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z\d0-9@$!%*?&]{10,}$')
        if correct_password.match(passw):
            return True
        return False
    

    def info_check(self):
        while True:
            self.email = input("Enter your email :")
            cursor.execute("SELECT * FROM user WHERE email = %s", (self.email,))
            if cursor.fetchone():
                print("This email is already taken, please choose another one.")
            else :
                self.passw =input("Enter your password :")
                if self.correct_password(self.passw):
                    break
                else :
                    print("Invalide password, please try an other one")


    def create_user(self):
        surname = self.entry_surname.get()
        firstname = self.entry_firstname.get()
        email = self.entry_email.get()
        passw = self.entry_passw.get()

        self.info_check()

        cursor.execute("""
            INSERT INTO user (name, first_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (surname, firstname, email, passw))
        mydb.commit()
            

    def log_in(self):
        self.enter_email = input("Enter your email :")
        self.enter_password = input("Enter your password :")
        cursor.execute("SELECT id FROM user WHERE email = %s", (self.enter_email,))
        self.user_id = cursor.fetchall()
        cursor.execute("SELECT password FROM user WHERE email = %s", (self.enter_email,))
        self.user_password = cursor.fetchone()
        cursor.execute("SELECT email FROM user")
        self.list_email = [email[0] for email in cursor.fetchall()]
        if self.enter_password == self.user_password[0] and self.enter_email in self.list_email:
            if self.email in admin_email :
                cursor.execute("SELECT * FROM account")
                cursor.fetchall()
                mydb.commit()
            else :
                cursor.execute("SELECT * FROM account WHERE user_email = %s", (self.enter_email,))
                cursor.fetchall()
                mydb.commit()
        else : 
            print("Wrong password, try again")
            self.log_in()

user = User()

class Transaction():
    def __init__(self):
        cursor.execute("SELECT id FROM user WHERE email = %s" (user.email))
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

    def outcoming_transfert(self):
        amount = int(input ("Insert amount to transfert :"))
        iban = input ("Enter IBAN : ")
        cursor.execute("SELECT iban from account")
        iban_list = [cursor.fetchall]
        if iban in iban_list :
            cursor.execute("SELECT id FROM user WHERE iban = %s" (iban,))
            self.outcoming_name = cursor.fetchone()[0]
            cursor.execute("SELECT balance FROM account WHERE user_id = %s" (self.outcoming_name))
            self.outcoming_balance = cursor.fetchone()[0]
            cursor.execute("SELECT balance FROM account WHERE user_id = %s" (self.user_id))
            self.balance = cursor.fetchall()
            if self.balance > amount :
                self.balance -= amount
                self.outcoming_balance += amount
                cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.balance, self.user_id))
                cursor.execute("UPDATE account SET balance = %s WHERE user_id = %s", (self.outcoming_balance, self.outcoming_name))
                mydb.commit()


        