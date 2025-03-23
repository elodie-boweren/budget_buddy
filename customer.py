import customtkinter as ctk
import mysql.connector
import random
import string
import re
import bcrypt
from PIL import Image, ImageTk
import os
from common import *
from dashboard import Dashboard

# Liste des emails administrateurs
admin_emails = [
    "budgetbuddy@laplateforme.io",
    "Budgetbuddy1@laplateforme.io",
    "Budgetbuddy2@laplateforme.io",
    "Budgetbuddy3@laplateforme.io",
    "Budgetbuddy4@laplateforme.io",
    "Budgetbuddy5@laplateforme.io"
]

class Customer:
    def __init__(self, email=None, password=None, firstname=None, name=None):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.name = name
        self.dashboard = None
        
    def generate_iban(self):
        """Génère un IBAN aléatoire au format français"""
        country_code = "FR"
        check_digits = ''.join(random.choices(string.digits, k=2))
        bank_code = ''.join(random.choices(string.digits, k=5))
        account_number = ''.join(random.choices(string.digits + string.ascii_uppercase, k=11))
        branch_code = ''.join(random.choices(string.digits, k=5))
        
        return f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"

    def correct_password(self, password):
        """Vérifie si le mot de passe respecte les critères de sécurité"""
        # Doit contenir au moins: 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial, 10 caractères
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$'
        return bool(re.match(pattern, password))
    
    def toggle_password_visibility(self):
        """Affiche ou masque le mot de passe"""
        if hasattr(self, 'show_password') and self.show_password.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def password_visibility(self):
        """Affiche ou masque le mot de passe de connexion"""
        if hasattr(self, 'show_password') and self.show_password.get():
            self.enter_password.configure(show="")
        else:
            self.enter_password.configure(show="*")

    def log_menu(self):
        """Affiche le menu de connexion/inscription"""
        from database import cursor, mydb
        
        clear_screen()
        
        # En-tête avec logo
        header = create_header("Budget Buddy")
        
        # Contenu principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Description
        welcome_label = ctk.CTkLabel(main_frame, 
                                    text="Votre allié financier pour des dépenses malines et un budget équilibré",
                                    font=ctk.CTkFont(size=14))
        welcome_label.pack(pady=(20, 40))
        
        # Boutons de connexion/inscription
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        button_signin = ctk.CTkButton(btn_frame, text="Se connecter", width=200, height=50,
                                     font=ctk.CTkFont(size=16), command=self.log_in)
        button_signin.pack(pady=10)
        
        button_signup = ctk.CTkButton(btn_frame, text="Créer un compte", width=200, height=50,
                                     font=ctk.CTkFont(size=16), command=self.create_account)
        button_signup.pack(pady=10)
        
        create_footer()

    def create_account(self):
        """Affiche le formulaire de création de compte"""
        from database import cursor, mydb
        
        clear_screen()
        
        header = create_header("Création de compte")
        
        # Contenu principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Champs du formulaire
        self.name = ctk.CTkEntry(form_frame, width=300, placeholder_text="Nom")
        self.name.pack(pady=10)
        
        self.firstname = ctk.CTkEntry(form_frame, width=300, placeholder_text="Prénom")
        self.firstname.pack(pady=10)
        
        self.email = ctk.CTkEntry(form_frame, width=300, placeholder_text="Email")
        self.email.pack(pady=10)
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x")
        
        self.password = ctk.CTkEntry(password_frame, width=300, placeholder_text="Mot de passe", show="*")
        self.password.pack(side="left", padx=(0, 10))
        
        self.show_password = ctk.BooleanVar(value=False)
        show_password_checkbox = ctk.CTkCheckBox(password_frame, text="Afficher", 
                                                variable=self.show_password, 
                                                command=self.toggle_password_visibility)
        show_password_checkbox.pack(side="left")
        
        # Message d'information sur le mot de passe
        password_info = ctk.CTkLabel(form_frame, 
                                    text="Le mot de passe doit contenir au moins 10 caractères,\nune majuscule, une minuscule, un chiffre et un caractère spécial.",
                                    font=ctk.CTkFont(size=12),
                                    text_color="#aaaaaa")
        password_info.pack(pady=(0, 20))
        
        # Affichage des erreurs
        self.error_label = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.error_label.pack(pady=10)
        
        # Boutons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        back_button = ctk.CTkButton(button_frame, text="Retour", 
                                   width=140, command=self.log_menu,
                                   fg_color="#555555", hover_color="#333333")
        back_button.pack(side="left", padx=20)
        
        submit_button = ctk.CTkButton(button_frame, text="Créer mon compte", 
                                     width=200, command=self.submit_account)
        submit_button.pack(side="right", padx=20)
        
        create_footer()
    
    def submit_account(self):
        """Traite la soumission du formulaire de création de compte"""
        from database import cursor, mydb
        
        name = self.name.get()
        firstname = self.firstname.get()
        email = self.email.get()
        password = self.password.get()
        
        # Validation des champs
        if not name or not firstname or not email or not password:
            self.error_label.configure(text="Tous les champs sont obligatoires.")
            return
        
        # Validation de l'email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.error_label.configure(text="Format d'email invalide.")
            return
            
        # Validation du mot de passe
        if not self.correct_password(password):
            self.error_label.configure(text="Le mot de passe ne respecte pas les critères de sécurité.")
            return
        
        # Vérification si l'email existe déjà
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        if cursor.fetchone():
            self.error_label.configure(text="Cet email est déjà utilisé.")
            return
        
        # Hashage du mot de passe
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Insertion de l'utilisateur
        cursor.execute("""
            INSERT INTO user (name, first_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (name, firstname, email, hash_password))
        mydb.commit()
        
        # Récupération de l'ID utilisateur
        cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
        user_id = cursor.fetchone()[0]
        
        # Création d'un compte courant par défaut
        iban = self.generate_iban()
        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, user_id, "courant"))
        mydb.commit()
        
        # Afficher un message de succès
        show_success("Compte créé", "Votre compte a été créé avec succès !")
        
        # Redirection vers la page de connexion
        self.log_in()

    def log_in(self):
        """Affiche le formulaire de connexion"""
        from database import cursor, mydb
        
        clear_screen()
        
        header = create_header("Connexion")
        
        # Formulaire de connexion
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Champs de connexion
        self.enter_email = ctk.CTkEntry(form_frame, width=300, placeholder_text="Email")
        self.enter_email.pack(pady=10)
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x")
        
        self.enter_password = ctk.CTkEntry(password_frame, width=300, placeholder_text="Mot de passe", show="*")
        self.enter_password.pack(side="left", padx=(0, 10))
        
        self.show_password = ctk.BooleanVar(value=False)
        show_password_checkbox = ctk.CTkCheckBox(password_frame, text="Afficher", 
                                                variable=self.show_password, 
                                                command=self.password_visibility)
        show_password_checkbox.pack(side="left")
        
        # Message d'erreur
        self.login_error = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.login_error.pack(pady=10)
        
        # Boutons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        back_button = ctk.CTkButton(button_frame, text="Retour", 
                                   width=140, command=self.log_menu,
                                   fg_color="#555555", hover_color="#333333")
        back_button.pack(side="left", padx=20)
        
        connect_button = ctk.CTkButton(button_frame, text="Se connecter", 
                                      width=200, command=self.validate_login)
        connect_button.pack(side="right", padx=20)
        
        create_footer()
    
    def validate_login(self):
        """Valide les informations de connexion"""
        from database import cursor, mydb
        
        email = self.enter_email.get()
        entered_password = self.enter_password.get()
        
        if not email or not entered_password:
            self.login_error.configure(text="Veuillez remplir tous les champs.")
            return
        
        # Vérification des identifiants
        cursor.execute("SELECT id, password, is_admin FROM user WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        if result:
            user_id, stored_password, is_admin = result
            
            # Vérification du mot de passe
            if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8')):
                # Initialiser le dashboard avec l'ID utilisateur
                self.dashboard = Dashboard(user_id)
                
                # Rediriger vers le menu approprié
                if is_admin or email in admin_emails:
                    admin_menu()
                else:
                    self.dashboard.display_dashboard()
            else:
                self.login_error.configure(text="Mot de passe incorrect.")
        else:
            self.login_error.configure(text="Email non reconnu.")