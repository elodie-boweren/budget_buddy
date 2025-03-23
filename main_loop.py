import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from dashboard import Dashboard
from customer import Customer
from database import *
from transaction import Transaction
from common import *

# Chargement des variables d'environnement
load_dotenv("../.env")

# Initialisation de la connexion à la base de données
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD"),
        database="budget_buddy"
    )
    cursor = mydb.cursor(buffered=True)
    print("Connexion à la base de données réussie!")
except mysql.connector.Error as err:
    print(f"Erreur de connexion à la base de données: {err}")
    exit(1)

# Configuration de l'interface
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

# Initialisation de la fenêtre principale
root = init_root("900x700")
root.title("Budget Buddy - Votre allié financier")

def main():
    """Fonction principale pour démarrer l'application"""
    # Instance du client
    customer = Customer()
   
    # Affichage de la page de connexion/inscription
    customer.log_menu()

if __name__ == "__main__":
    main()
    root.mainloop()