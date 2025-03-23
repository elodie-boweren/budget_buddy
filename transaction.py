import customtkinter as ctk
from database import *
from common import *
from CTkMessagebox import CTkMessagebox
import datetime
from decimal import Decimal

class Transaction:
    def __init__(self, user_id):
        self.user_id = user_id
        self.update_balance()
   
    def update_balance(self):
        cursor.execute("SELECT id, balance FROM account WHERE user_id = %s", (self.user_id,))
        result = cursor.fetchone()
        if result:
            self.account_id, self.user_balance = result[0], Decimal(str(result[1]))
        else:
            self.account_id, self.user_balance = None, 0
   
    def deposit(self):
        clear_screen()
       
        # Titre
        title_label = ctk.CTkLabel(root, text="Faire un dépôt", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")
       
        # Champ pour le montant
        self.entry_amount = ctk.CTkEntry(root, width=220, placeholder_text="Montant à déposer")
        self.entry_amount.place(relx=0.5, rely=0.3, anchor="center")
       
        # Champ pour la description
        self.description = ctk.CTkEntry(root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.4, anchor="center")
       
        # Menu déroulant pour la catégorie
        cursor.execute("SELECT id, name FROM category")
        categories = cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        self.category_ids = [cat[0] for cat in categories]
       
        self.category_menu = ctk.CTkComboBox(root, values=category_names)
        self.category_menu.place(relx=0.5, rely=0.5, anchor="center")
        self.category_menu.set("Choisir une catégorie")
       
        # Message d'erreur
        self.error_label = ctk.CTkLabel(root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")
       
        # Bouton pour valider
        validate_button = ctk.CTkButton(root, text="Déposer", command=self.validate_deposit)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")
       
        # Bouton retour
        back_button = ctk.CTkButton(root, text="Retour", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
   
    def validate_deposit(self):
        try:
            amount = Decimal(self.entry_amount.get())
            description = self.description.get()
            category_name = self.category_menu.get()
           
            # Vérifications des champs
            if amount <= 0:
                self.error_label.configure(text="Le montant doit être positif")
                return
           
            if not description:
                self.error_label.configure(text="Veuillez ajouter une description")
                return
               
            if category_name == "Choisir une catégorie":
                self.error_label.configure(text="Veuillez choisir une catégorie")
                return
               
            # Récupération de l'ID de catégorie
            category_index = self.category_menu.get().index(category_name)
            category_id = self.category_ids[category_index]
           
            # Mise à jour du solde
            new_balance = self.user_balance + Decimal(str(amount))
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))
           
            # Génération d'une référence unique
            reference = f"DEP-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
           
            # Ajout de la transaction
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'deposit')
            """, (description, amount, reference, self.account_id, category_id))
           
            mydb.commit()
           
            # Mise à jour du solde affiché
            self.update_balance()
           
            # Message de succès
            CTkMessagebox(title="Succès", message=f"Dépôt de {amount}€ effectué avec succès!", icon="check")
           
            # Retour à l'écran des transactions
            self.display_transaction()
           
        except ValueError:
            self.error_label.configure(text="Veuillez entrer un montant valide")
   
    def withdrawal(self):
        clear_screen()
       
        # Titre
        title_label = ctk.CTkLabel(root, text="Faire un retrait", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")
       
        # Champ pour le montant
        self.entry_withdrawal = ctk.CTkEntry(root, width=220, placeholder_text="Montant à retirer")
        self.entry_withdrawal.place(relx=0.5, rely=0.3, anchor="center")
       
        # Champ pour la description
        self.description = ctk.CTkEntry(root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.4, anchor="center")
       
        # Menu déroulant pour la catégorie
        cursor.execute("SELECT id, name FROM category")
        categories = cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        self.category_ids = [cat[0] for cat in categories]
       
        self.category_menu = ctk.CTkComboBox(root, values=category_names)
        self.category_menu.place(relx=0.5, rely=0.5, anchor="center")
        self.category_menu.set("Choisir une catégorie")
       
        # Message d'erreur
        self.error_label = ctk.CTkLabel(root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")
       
        # Bouton pour valider
        validate_button = ctk.CTkButton(root, text="Retirer", command=self.validate_withdrawal)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")
       
        # Bouton retour
        back_button = ctk.CTkButton(root, text="Retour", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
   
    def validate_withdrawal(self):
        try:
            amount = Decimal(self.entry_withdrawal.get())
            description = self.description.get()
            category_name = self.category_menu.get()
           
            # Vérifications des champs
            if amount <= 0:
                self.error_label.configure(text="Le montant doit être positif")
                return
           
            if not description:
                self.error_label.configure(text="Veuillez ajouter une description")
                return
               
            if category_name == "Choisir une catégorie":
                self.error_label.configure(text="Veuillez choisir une catégorie")
                return
           
            if amount > self.user_balance:
                self.error_label.configure(text="Solde insuffisant")
                return
               
            # Récupération de l'ID de catégorie
            category_index = self.category_menu.get().index(category_name)
            category_id = self.category_ids[category_index]
           
            # Mise à jour du solde
            new_balance = self.user_balance - amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))
           
            # Génération d'une référence unique
            reference = f"WIT-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
           
            # Ajout de la transaction
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'withdrawal')
            """, (description, amount, reference, self.account_id, category_id))
           
            mydb.commit()
           
            # Mise à jour du solde affiché
            self.update_balance()
           
            # Message de succès
            CTkMessagebox(title="Succès", message=f"Retrait de {amount}€ effectué avec succès!", icon="check")
           
            # Retour à l'écran des transactions
            self.display_transaction()
           
        except ValueError:
            self.error_label.configure(text="Veuillez entrer un montant valide")
   
    def transfer(self):
        clear_screen()
       
        # Titre
        title_label = ctk.CTkLabel(root, text="Faire un transfert", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")
       
        # Champ pour l'IBAN
        self.iban_entry = ctk.CTkEntry(root, width=220, placeholder_text="IBAN du destinataire")
        self.iban_entry.place(relx=0.5, rely=0.3, anchor="center")
       
        # Champ pour le montant
        self.transfer_amount = ctk.CTkEntry(root, width=220, placeholder_text="Montant à transférer")
        self.transfer_amount.place(relx=0.5, rely=0.4, anchor="center")
       
        # Champ pour la description
        self.description = ctk.CTkEntry(root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.5, anchor="center")
       
        # Message d'erreur
        self.error_label = ctk.CTkLabel(root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")
       
        # Bouton pour valider
        validate_button = ctk.CTkButton(root, text="Transférer", command=self.validate_transfer)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")
       
        # Bouton retour
        back_button = ctk.CTkButton(root, text="Retour", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
   
    def validate_transfer(self):
        try:
            iban = self.iban_entry.get()
            amount = Decimal(self.transfer_amount.get())
            description = self.description.get()
           
            # Vérifications des champs
            if not iban:
                self.error_label.configure(text="Veuillez entrer un IBAN")
                return
               
            if amount <= 0:
                self.error_label.configure(text="Le montant doit être positif")
                return
           
            if amount > self.user_balance:
                self.error_label.configure(text="Solde insuffisant")
                return
               
            if not description:
                self.error_label.configure(text="Veuillez ajouter une description")
                return
           
            # Recherche du compte destinataire
            cursor.execute("SELECT id, user_id FROM account WHERE iban = %s", (iban,))
            dest_account = cursor.fetchone()
           
            if not dest_account:
                self.error_label.configure(text="IBAN invalide")
                return
               
            dest_account_id, dest_user_id = dest_account
           
            # Vérifier qu'on ne transfère pas à soi-même
            if dest_user_id == self.user_id:
                self.error_label.configure(text="Vous ne pouvez pas transférer à vous-même")
                return
           
            # Mise à jour du solde source (débiteur)
            new_balance = self.user_balance - amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))
           
            # Mise à jour du solde destination (créditeur)
            cursor.execute("SELECT balance FROM account WHERE id = %s", (dest_account_id,))
            dest_balance = cursor.fetchone()[0]
            new_dest_balance = dest_balance + amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_dest_balance, dest_account_id))
           
            # Génération de références uniques
            out_reference = f"OUT-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            in_reference = f"IN-{dest_user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
           
            # Récupération de l'ID de catégorie "Transfert"
            cursor.execute("SELECT id FROM category WHERE name = 'Autres'")
            category_id = cursor.fetchone()[0]
           
            # Ajout de la transaction sortante
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'outgoing_transfer')
            """, (description, amount, out_reference, self.account_id, category_id))
           
            # Ajout de la transaction entrante
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'incoming_transfer')
            """, (f"Transfert reçu: {description}", amount, in_reference, dest_account_id, category_id))
           
            mydb.commit()
           
            # Mise à jour du solde affiché
            self.update_balance()
           
            # Message de succès
            CTkMessagebox(title="Succès", message=f"Transfert de {amount}€ effectué avec succès!", icon="check")
           
            # Retour à l'écran des transactions
            self.display_transaction()
           
        except ValueError:
            self.error_label.configure(text="Veuillez entrer un montant valide")
   
    def show_history(self):
        clear_screen()
       
        # Titre
        title_label = ctk.CTkLabel(root, text="Historique des transactions", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")
       
        # Options de filtrage
        filter_frame = ctk.CTkFrame(root)
        filter_frame.place(relx=0.5, rely=0.2, anchor="center")
       
        # Menu déroulant pour le type de transaction
        type_label = ctk.CTkLabel(filter_frame, text="Type:")
        type_label.grid(row=0, column=0, padx=5, pady=5)
       
        types = ["Tous", "Dépôt", "Retrait", "Transfert entrant", "Transfert sortant"]
        self.type_menu = ctk.CTkComboBox(filter_frame, values=types)
        self.type_menu.grid(row=0, column=1, padx=5, pady=5)
        self.type_menu.set("Tous")
       
        # Bouton de filtrage
        filter_button = ctk.CTkButton(filter_frame, text="Filtrer", command=self.apply_filters)
        filter_button.grid(row=0, column=2, padx=5, pady=5)
       
        # Zone d'affichage des transactions
        self.history_frame = ctk.CTkScrollableFrame(root, width=600, height=300)
        self.history_frame.place(relx=0.5, rely=0.5, anchor="center")
       
        # Chargement des transactions
        self.load_transactions()
       
        # Bouton retour
        back_button = ctk.CTkButton(root, text="Retour", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.85, anchor="center")
   
    def load_transactions(self, type_filter=None):
        # Nettoyer le cadre d'historique
        for widget in self.history_frame.winfo_children():
            widget.destroy()
       
        # Titre des colonnes
        header_frame = ctk.CTkFrame(self.history_frame)
        header_frame.pack(fill="x", pady=5)
       
        ctk.CTkLabel(header_frame, text="Date", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Description", width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Montant", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Type", width=150).pack(side="left", padx=5)
       
        # Construire la requête SQL en fonction du filtre
        query = """
            SELECT t.date, t.description, t.amount, t.transaction_type, c.name
            FROM transaction t
            JOIN category c ON t.category_id = c.id
            WHERE t.account_id = %s
        """
        params = [self.account_id]
       
        if type_filter and type_filter != "Tous":
            type_map = {
                "Dépôt": "deposit",
                "Retrait": "withdrawal",
                "Transfert entrant": "incoming_transfer",
                "Transfert sortant": "outgoing_transfer"
            }
            query += " AND t.transaction_type = %s"
            params.append(type_map[type_filter])
       
        query += " ORDER BY t.date DESC"
       
        cursor.execute(query, params)
        transactions = cursor.fetchall()
       
        if not transactions:
            no_trans = ctk.CTkLabel(self.history_frame, text="Aucune transaction trouvée")
            no_trans.pack(pady=20)
            return
       
        # Afficher chaque transaction
        for date, desc, amount, trans_type, category in transactions:
            trans_frame = ctk.CTkFrame(self.history_frame)
            trans_frame.pack(fill="x", pady=2)
           
            # Formater la date
            date_str = date.strftime("%d/%m/%Y")
           
            # Formater le type
            type_map = {
                "deposit": "Dépôt",
                "withdrawal": "Retrait",
                "incoming_transfer": "Transfert entrant",
                "outgoing_transfer": "Transfert sortant"
            }
            type_str = type_map.get(trans_type, trans_type)
           
            # Formater le montant avec couleur
            if trans_type in ["deposit", "incoming_transfer"]:
                amount_str = f"+{amount}€"
                amount_color = "green"
            else:
                amount_str = f"-{amount}€"
                amount_color = "red"
           
            ctk.CTkLabel(trans_frame, text=date_str, width=100).pack(side="left", padx=5)
            ctk.CTkLabel(trans_frame, text=desc, width=150).pack(side="left", padx=5)
            ctk.CTkLabel(trans_frame, text=amount_str, width=100, text_color=amount_color).pack(side="left", padx=5)
            ctk.CTkLabel(trans_frame, text=f"{type_str} ({category})", width=150).pack(side="left", padx=5)
   
    def apply_filters(self):
        type_filter = self.type_menu.get()
        self.load_transactions(type_filter)
   
    def display_transaction(self):
        clear_screen()
       
        # Titre
        title_label = ctk.CTkLabel(root, text="Transactions", font=("Arial", 20, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")
       
        # Affichage du solde
        balance_label = ctk.CTkLabel(root,
                                     text=f"Solde actuel: {self.user_balance}€",
                                     font=("Arial", 16))
        balance_label.place(relx=0.5, rely=0.2, anchor="center")
       
        # Boutons pour les différentes opérations
        deposit_button = ctk.CTkButton(root, text="Faire un dépôt",
                                      command=self.deposit,
                                      width=200, height=40)
        deposit_button.place(relx=0.5, rely=0.35, anchor="center")
       
        withdrawal_button = ctk.CTkButton(root, text="Faire un retrait",
                                         command=self.withdrawal,
                                         width=200, height=40)
        withdrawal_button.place(relx=0.5, rely=0.45, anchor="center")
       
        transfer_button = ctk.CTkButton(root, text="Faire un transfert",
                                       command=self.transfer,
                                       width=200, height=40)
        transfer_button.place(relx=0.5, rely=0.55, anchor="center")
       
        history_button = ctk.CTkButton(root, text="Voir l'historique",
                                      command=self.show_history,
                                      width=200, height=40)
        history_button.place(relx=0.5, rely=0.65, anchor="center")
       
        # Bouton de retour
        back_button = ctk.CTkButton(root, text="Retour au tableau de bord",
                                   command=self.back_to_dashboard,
                                   width=200, height=40)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
   
    def back_to_dashboard(self):
        from dashboard import Dashboard
        dashboard = Dashboard()
        dashboard.user_id = self.user_id
        dashboard.display_dashboard()