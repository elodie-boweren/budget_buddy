import customtkinter as ctk
from database import *
from common import *
from transaction import Transaction
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class Dashboard:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.accounts = []
        self.selected_account_id = None
        self.transaction = None

    def get_user_info(self):
        """Récupère les informations de l'utilisateur et ses comptes"""
        cursor.execute("""
            SELECT id, first_name, name
            FROM user
            WHERE id = %s
        """, (self.user_id,))
        user_info = cursor.fetchone()

        if user_info:
            self.user_id, self.first_name, self.name = user_info
           
            # Initialiser la classe Transaction
            self.transaction = Transaction(self.user_id)

            # Récupération des comptes de l'utilisateur
            cursor.execute("""
                SELECT id, type, balance, iban FROM account WHERE user_id = %s
            """, (self.user_id,))
            self.accounts = cursor.fetchall()

            # Définit le premier compte comme sélectionné par défaut
            if self.accounts:
                self.selected_account_id = self.accounts[0][0]
        else:
            self.user_id, self.first_name, self.name, self.accounts = None, None, None, []

    def update_account_info(self, choice=None):
        """Met à jour les informations du compte sélectionné"""
        account_type = self.account_options.get()
       
        for acc_id, acc_type, balance, iban in self.accounts:
            if acc_type.capitalize() == account_type:
                self.selected_account_id = acc_id
                self.balance_var.set(f"Solde : {balance}€")
                self.iban_var.set(f"IBAN : {iban}")
                self.load_transactions()
                self.create_monthly_stats()
                break

    def add_savings_account(self):
        """Ajoute un compte épargne à l'utilisateur"""
        import random
        import string
       
        iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
       
        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, self.user_id, "epargne"))
       
        mydb.commit()
       
        # Rafraîchir la liste des comptes
        self.get_user_info()
       
        # Afficher un message de succès
        CTkMessagebox(title="Succès", message="Compte épargne ajouté avec succès!", icon="check")
       
        # Rafraîchir l'affichage
        self.display_dashboard()

    def create_monthly_stats(self):
        """Crée un graphique des dépenses/revenus mensuels"""
        # Nettoyer le cadre du graphique
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
           
        # Récupération des données du mois en cours
        current_date = datetime.datetime.now()
        start_of_month = datetime.datetime(current_date.year, current_date.month, 1).strftime('%Y-%m-%d')
        end_of_month = current_date.strftime('%Y-%m-%d')
       
        cursor.execute("""
            SELECT
                SUM(CASE WHEN transaction_type IN ('deposit', 'incoming_transfer') THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN transaction_type IN ('withdrawal', 'outgoing_transfer') THEN amount ELSE 0 END) as expense
            FROM transaction
            WHERE account_id = %s AND date BETWEEN %s AND %s
        """, (self.selected_account_id, start_of_month, end_of_month))
       
        result = cursor.fetchone()
       
        if result:
            income, expense = result
            income = income if income else 0
            expense = expense if expense else 0
           
            # Création du graphique
            figure = plt.Figure(figsize=(5, 2), dpi=100)
            ax = figure.add_subplot(111)
           
            labels = ['Revenus', 'Dépenses']
            values = [income, expense]
            colors = ['#4CAF50', '#E53935']
           
            ax.bar(labels, values, color=colors)
            ax.set_title('Résumé du mois')
           
            # Ajouter le graphique au cadre
            canvas = FigureCanvasTkAgg(figure, self.stats_frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)
           
            # Afficher des statistiques textuelles
            stats_label = ctk.CTkLabel(
                self.stats_frame,
                text=f"Revenus: {income}€ | Dépenses: {expense}€ | Bilan: {income-expense}€",
                font=("Arial", 14)
            )
            stats_label.pack(pady=10)
           
            # Afficher une alerte si le solde est faible
            if self.accounts and self.selected_account_id:
                for acc_id, acc_type, balance, iban in self.accounts:
                    if acc_id == self.selected_account_id and balance < 100:
                        alert_label = ctk.CTkLabel(
                            self.stats_frame,
                            text="⚠️ ALERTE: Votre solde est faible!",
                            font=("Arial", 14, "bold"),
                            text_color="red"
                        )
                        alert_label.pack(pady=5)

    def load_transactions(self):
        """Charge les transactions récentes pour le compte sélectionné"""
        # Nettoyer le cadre des transactions
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
           
        cursor.execute("""
            SELECT date, description, amount, transaction_type
            FROM transaction
            WHERE account_id = %s
            ORDER BY date DESC
            LIMIT 5
        """, (self.selected_account_id,))
       
        transactions = cursor.fetchall()
       
        if transactions:
            # Ajouter un en-tête
            header_frame = ctk.CTkFrame(self.transactions_frame)
            header_frame.pack(fill="x", pady=(0, 5))
           
            ctk.CTkLabel(header_frame, text="Date", width=100).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Description", width=200).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Montant", width=100).pack(side="left", padx=5)
           
            # Ajouter les transactions
            for date, desc, amount, trans_type in transactions:
                trans_frame = ctk.CTkFrame(self.transactions_frame, fg_color="transparent")
                trans_frame.pack(fill="x", pady=2)
               
                date_str = date.strftime("%d/%m/%Y")
               
                # Formater le montant avec couleur selon le type
                if trans_type in ["deposit", "incoming_transfer"]:
                    amount_str = f"+{amount}€"
                    amount_color = "green"
                else:
                    amount_str = f"-{amount}€"
                    amount_color = "red"
               
                ctk.CTkLabel(trans_frame, text=date_str, width=100).pack(side="left", padx=5)
                ctk.CTkLabel(trans_frame, text=desc, width=200).pack(side="left", padx=5)
                ctk.CTkLabel(trans_frame, text=amount_str, width=100, text_color=amount_color).pack(side="left", padx=5)
        else:
            no_trans = ctk.CTkLabel(self.transactions_frame, text="Aucune transaction récente.")
            no_trans.pack(pady=20)

    def display_dashboard(self):
        """Affiche le tableau de bord principal"""
        self.get_user_info()
        clear_screen()
       
        # En-tête
        header = create_header(f"Tableau de Bord - {self.first_name} {self.name}")
       
        # Cadre principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
       
        # Panel gauche - Sélection de compte et info
        left_panel = ctk.CTkFrame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
       
        # Sélecteur de compte
        account_frame = ctk.CTkFrame(left_panel)
        account_frame.pack(pady=10, fill="x")
       
        account_label = ctk.CTkLabel(account_frame, text="Compte:", font=("Arial", 14))
        account_label.pack(side="left", padx=10)
       
        if self.accounts:
            # Menu déroulant des comptes
            self.account_options = ctk.CTkComboBox(
                account_frame,
                values=[acc_type.capitalize() for _, acc_type, _, _ in self.accounts],
                command=self.update_account_info
            )
            self.account_options.pack(side="left", padx=10, fill="x", expand=True)
            self.account_options.set(self.accounts[0][1].capitalize())
           
            # Informations du compte
            self.balance_var = ctk.StringVar(value=f"Solde : {self.accounts[0][2]}€")
            self.iban_var = ctk.StringVar(value=f"IBAN : {self.accounts[0][3]}")
           
            info_frame = ctk.CTkFrame(left_panel)
            info_frame.pack(pady=10, fill="x")
           
            balance_label = ctk.CTkLabel(info_frame, textvariable=self.balance_var, font=("Arial", 16, "bold"))
            balance_label.pack(pady=5)
           
            iban_label = ctk.CTkLabel(info_frame, textvariable=self.iban_var, font=("Arial", 12))
            iban_label.pack(pady=5)
           
            # Bouton pour ajouter un compte épargne
            add_savings_button = ctk.CTkButton(
                left_panel,
                text="Ajouter un compte épargne",
                command=self.add_savings_account
            )
            add_savings_button.pack(pady=10, fill="x")
           
            # Bouton pour les transactions
            transaction_button = ctk.CTkButton(
                left_panel,
                text="Gérer mes transactions",
                command=self.transaction.display_transaction
            )
            transaction_button.pack(pady=10, fill="x")
           
            # Transactions récentes
            trans_label = ctk.CTkLabel(left_panel, text="Transactions récentes", font=("Arial", 16, "bold"))
            trans_label.pack(pady=(20, 10))
           
            self.transactions_frame = ctk.CTkFrame(left_panel)
            self.transactions_frame.pack(fill="both", expand=True, pady=5)
           
            # Panel droit - Statistiques et graphiques
            right_panel = ctk.CTkFrame(main_frame)
            right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
           
            stats_label = ctk.CTkLabel(right_panel, text="Résumé financier", font=("Arial", 16, "bold"))
            stats_label.pack(pady=(10, 20))
           
            self.stats_frame = ctk.CTkFrame(right_panel)
            self.stats_frame.pack(fill="both", expand=True, pady=5)
           
            # Charger les données initiales
            self.load_transactions()
            self.create_monthly_stats()
        else:
            no_account_label = ctk.CTkLabel(
                left_panel,
                text="Vous n'avez pas encore de compte.",
                font=("Arial", 14)
            )
            no_account_label.pack(pady=20)
       
        # Bouton déconnexion
        from customer import Customer
        logout_button = ctk.CTkButton(
            main_frame,
            text="Déconnexion",
            command=lambda: Customer().log_menu(),
            fg_color="#E53935",
            hover_color="#C62828"
        )
        logout_button.pack(side="bottom", pady=20)
       
        create_footer()