import customtkinter as ctk
from customtkinter import *
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Laura21!",
    database="BudgetBuddy"
)

cursor = mydb.cursor()

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("800x600")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def sign_up():
    clear_screen()

    entry_surname = ctk.CTkEntry(root, placeholder_text = "Surname")
    entry_firstname = ctk.CTkEntry(root, placeholder_text = "Firstname")
    entry_email = ctk.CTkEntry(root, placeholder_text = "Email")
    entry_password = ctk.CTkEntry(root, placeholder_text = "password")

    entry_surname.place(relx = 0.5, rely = 0.35, anchor = "center")
    entry_firstname.place(relx = 0.5, rely = 0.4, anchor = "center")
    entry_email.place(relx = 0.5, rely = 0.45, anchor = "center")
    entry_password.place(relx = 0.5, rely = 0.5, anchor = "center")

    submit_button = ctk.CTkButton(root, text="Submit")
    submit_button.place(relx = 0.5, rely = 0.6, anchor = "center")

    back_button = ctk.CTkButton(root, text="Back", command=main_menu)
    back_button.place(relx = 0.5, rely = 0.65, anchor = "center")

def main_menu():
    clear_screen()

    label = ctk.CTkLabel(root, text = "Budget Buddy")
    label.pack(pady=10)

    button1 = ctk.CTkButton(root, text="Sign in")
    button2 = ctk.CTkButton(root, text = "Sign up", command = sign_up)

    button1.place(relx = 0.5, rely = 0.4, anchor = "center")
    button2.place(relx = 0.5, rely = 0.6, anchor = "center")

main_menu()

root.mainloop()
