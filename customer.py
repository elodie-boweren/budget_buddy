import customtkinter as ctk
import mysql.connector
import random
import string
import re
import bcrypt
from PIL import Image, ImageTk
import os
from common import AppManager
from dashboard import Dashboard

# List of adminstrator emails
admin_emails = [
    "Budgetbuddy@laplateforme.io",
    "Budgetbuddy1@laplateforme.io",
    "Budgetbuddy2@laplateforme.io",
    "Budgetbuddy3@laplateforme.io",
    "Budgetbuddy4@laplateforme.io",
    "Budgetbuddy5@laplateforme.io"
]

class Customer:
    def __init__(self, app_manager=None, email=None, password=None, firstname=None, name=None):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.name = name
        self.dashboard = None
        self.app_manager = app_manager
        
    def generate_iban(self):
        """Create a random IBAN in French format"""
        country_code = "FR"
        check_digits = ''.join(random.choices(string.digits, k=2))
        bank_code = ''.join(random.choices(string.digits, k=5))
        account_number = ''.join(random.choices(string.digits + string.ascii_uppercase, k=11))
        branch_code = ''.join(random.choices(string.digits, k=5))
        
        return f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"

    def correct_password(self, password):
        """Checks if the password complies with security conditions"""
        # Must contain at least: 1 upper case, 1 lower case, 1 number, 1 special caracter, 10 caracters
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$'
        return bool(re.match(pattern, password))

    def password_visibility(self):
        """Show or hides the password"""
        if hasattr(self, 'show_password') and self.show_password.get():
            self.enter_password.configure(show="")
        else:
            self.enter_password.configure(show="*")

    def log_menu(self):
        """Displays the log-in menu"""
        from database import cursor, mydb
        
        self.app_manager.clear_screen()
        
        # Header with logo
        header = self.app_manager.create_header("Budget Buddy")
        
        # Main content
        main_frame = ctk.CTkFrame(self.app_manager.get_root())
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Description
        welcome_label = ctk.CTkLabel(main_frame, 
                                    text="your financial ally for clever speinding and balanced budget",
                                    font=ctk.CTkFont(size=14))
        welcome_label.pack(pady=(20, 40))
        
        # Boutons de connexion/inscription
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        button_signin = ctk.CTkButton(btn_frame, text="Sign in", width=200, height=50,
                                     font=ctk.CTkFont(size=16), command=self.log_in)
        button_signin.pack(pady=10)
        
        button_signup = ctk.CTkButton(btn_frame, text="Create an account", width=200, height=50,
                                     font=ctk.CTkFont(size=16), command=self.create_account)
        button_signup.pack(pady=10)
        
        self.app_manager.create_footer()

    def create_account(self):
        """Displays the entry boxes to create an account"""
        from database import cursor, mydb
        
        self.app_manager.clear_screen()
        
        header = self.app_manager.create_header("Account creation")
        
        # Main content
        main_frame = ctk.CTkFrame(self.app_manager.get_root())
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Entry area
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Entry fields
        self.name = ctk.CTkEntry(form_frame, width=300, placeholder_text="Name")
        self.name.pack(pady=10)
        
        self.firstname = ctk.CTkEntry(form_frame, width=300, placeholder_text="First name")
        self.firstname.pack(pady=10)
        
        self.email = ctk.CTkEntry(form_frame, width=300, placeholder_text="Email")
        self.email.pack(pady=10)
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x")
        
        self.enter_password = ctk.CTkEntry(password_frame, width=300, placeholder_text="Password", show="*")
        self.enter_password.pack(pady = 10)
        
        self.show_password = ctk.BooleanVar(value=False)
        show_password_checkbox = ctk.CTkCheckBox(password_frame, text="Display", 
                                                variable=self.show_password, 
                                                command=self.password_visibility)
        show_password_checkbox.place(x=580, y = 17)
        
        # Password information message
        password_info = ctk.CTkLabel(form_frame, 
                                    text="The password must contain at least:\n 1 upper case, 1 lower case, 1 number, 1 special caracter, 10 caracters.",
                                    font=ctk.CTkFont(size=12),
                                    text_color="#aaaaaa")
        password_info.pack(pady=(0, 20))
        
        # Displays errors
        self.error_label = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.error_label.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        back_button = ctk.CTkButton(button_frame, text="Back", width=140, command=self.log_menu,fg_color="#555555", hover_color="#333333")
        back_button.pack(side="left", padx=20)
        
        submit_button = ctk.CTkButton(button_frame, text="Create my account", width=200, command=self.submit_account)
        submit_button.pack(side="right", padx=20)
        
        self.app_manager.create_footer()
    
    def submit_account(self):
        """Processes the submission for account creation"""
        from database import cursor, mydb
        
        name = self.name.get()
        firstname = self.firstname.get()
        email = self.email.get()
        password = self.enter_password.get()
        
        # Check fields completed
        if not name or not firstname or not email or not password:
            self.error_label.configure(text="All fields are mandatory.")
            return
        
        # Check email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.error_label.configure(text="Invalid email format.")
            return
            
        # Validating password
        if not self.correct_password(password):
            self.error_label.configure(text="The password does not comply with security criterias.")
            return
        
        # Checks if email already used
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        if cursor.fetchone():
            self.error_label.configure(text="this email is already in use.")
            return
        
        # Encrypting password
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Creation of user
        cursor.execute("""
            INSERT INTO user (name, first_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (name, firstname, email, hash_password))
        mydb.commit()
        
        # Get user ID
        cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
        user_id = cursor.fetchone()[0]
        
        # Creation of standard bank account
        iban = self.generate_iban()
        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, user_id, "current"))
        mydb.commit()
        
        # Confirmation message
        # self.app_manager.show_success("Account created", "Your account was successfully created !")
        
        # Back to the log-in page
        self.log_in()

    def log_in(self):
        """Displays log-in fields"""
        from database import cursor, mydb
        
        self.app_manager.clear_screen()
        
        header = self.app_manager.create_header("Connexion")
        
        # Log-in area
        main_frame = ctk.CTkFrame(self.app_manager.get_root())
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Log-in fields
        self.enter_email = ctk.CTkEntry(form_frame, width=300, placeholder_text="Email")
        self.enter_email.pack(pady=10)
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x")
        
        self.enter_password = ctk.CTkEntry(password_frame, width=300, placeholder_text="Password", show="*")
        self.enter_password.pack(side="left", padx=(0, 10))
        
        self.show_password = ctk.BooleanVar(value=False)
        show_password_checkbox = ctk.CTkCheckBox(password_frame, text="Display", 
                                                variable=self.show_password, 
                                                command=self.password_visibility)
        show_password_checkbox.pack(side="left")
        
        # Error message
        self.login_error = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.login_error.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        back_button = ctk.CTkButton(button_frame, text="Back", width=140, command=self.log_menu,fg_color="#555555", hover_color="#333333")
        back_button.pack(side="left", padx=20)
        
        connect_button = ctk.CTkButton(button_frame, text="Sign in", width=200, command=self.validate_login)
        connect_button.pack(side="right", padx=20)
        
        self.app_manager.create_footer()
    
    def validate_login(self):
        """Validates connexion info"""
        from database import cursor, mydb
        
        email = self.enter_email.get()
        entered_password = self.enter_password.get()
        
        if not email or not entered_password:
            self.login_error.configure(text="All fields are mandatory.")
            return
        
        # Check the email
        cursor.execute("SELECT id, password, is_admin FROM user WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        if result:
            user_id, stored_password, is_admin = result
            
            # Check password
            if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8')):
                # Initialize dashboard with user's information
                self.dashboard = Dashboard(self.app_manager, user_id)
                
                # Go to the correct dashboard
                if is_admin or email in admin_emails:
                    self.app_manager.admin_menu()
                else:
                    self.dashboard.display_dashboard()
            else:
                self.login_error.configure(text="Invalid password.")
        else:
            self.login_error.configure(text="Unknown email.")