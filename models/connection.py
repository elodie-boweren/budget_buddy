import mysql.connector
from dotenv import load_dotenv
import os
import customtkinter as ctk
from customtkinter import *
from user import User
# import matplotlib.pyplot as plt
# import numpy as np

load_dotenv("./.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="budget_buddy"
)
cursor = mydb.cursor()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Budget Buddy")
        self.geometry("800x600")
        set_default_color_theme("blue") 
        set_appearance_mode("light")
  
    def clear_screen(self):     
        for widget in self.winfo_children():         
            widget.destroy()  

    def main_menu(self):     
        self.clear_screen()      
        label = ctk.CTkLabel(self, text = "Budget Buddy")     
        label.pack(pady=10)      
        button1 = ctk.CTkButton(self, text="Sign in")     
        button2 = ctk.CTkButton(self, text = "Sign up", command = self.sign_up)      
        button1.place(relx = 0.5, rely = 0.4, anchor = "center")     
        button2.place(relx = 0.5, rely = 0.6, anchor = "center")  

    def sign_up_screen(self):     
        self.clear_screen()      
        self.entry_surname = ctk.CTkEntry(self, placeholder_text = "Surname")    
        self.entry_firstname = ctk.CTkEntry(self, placeholder_text = "Firstname")    
        self.entry_email = ctk.CTkEntry(self, placeholder_text = "Email")   
        self.entry_passw = ctk.CTkEntry(self, placeholder_text = "Password")   
        self.entry_surname.place(relx = 0.5, rely = 0.35, anchor = "center")     
        self.entry_firstname.place(relx = 0.5, rely = 0.4, anchor = "center")     
        self.entry_email.place(relx = 0.5, rely = 0.45, anchor = "center")     
        self.entry_passw.place(relx = 0.5, rely = 0.5, anchor = "center")      
            
        back_button = ctk.CTkButton(self, text="Back", command = self.main_menu)    
        back_button.place(relx = 0.5, rely = 0.65, anchor = "center")

        submit_button = ctk.CTkButton(self, text="Submit", command = User.create_user)
        submit_button.place(relx = 0.5, rely = 0.6, anchor = "center")

    def sign_in_screen(self):     
        self.clear_screen()      
        self.entry_email = ctk.CTkEntry(self, placeholder_text = "Email")   
        self.entry_passw = ctk.CTkEntry(self, placeholder_text = "Password")   
        self.entry_email.place(relx = 0.5, rely = 0.45, anchor = "center")     
        self.entry_passw.place(relx = 0.5, rely = 0.5, anchor = "center")      
            
        back_button = ctk.CTkButton(self, text="Back", command = self.main_menu)    
        back_button.place(relx = 0.5, rely = 0.65, anchor = "center")

        submit_button = ctk.CTkButton(self, text="Submit", command = self.dashboard)
        submit_button.place(relx = 0.5, rely = 0.6, anchor = "center")       

    def dashboard(self):
        self.clear_screen()
        label = ctk.CTkLabel(self, text = "Budget Buddy")  
        label.pack(pady=10) 


Sign_in_menu = App()   
Sign_in_menu.main_menu()  
Sign_in_menu.mainloop()
