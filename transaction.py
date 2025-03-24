import customtkinter as ctk
from database import *
from common import *
import datetime
from decimal import Decimal

class Transaction:
    def __init__(self, user_id, app_manager):
        self.user_id = user_id
        self.app_manager = app_manager
        self.root = app_manager.get_root()
        self.update_balance()

    def update_balance(self):
        cursor.execute("SELECT id, balance FROM account WHERE user_id = %s", (self.user_id,))
        result = cursor.fetchone()
        if result:
            self.account_id, self.user_balance = result[0], Decimal(str(result[1]))
        else:
            self.account_id, self.user_balance = None, 0

    def deposit(self):
        self.app_manager.clear_screen()

        # Title
        title_label = ctk.CTkLabel(self.root, text="Deposit", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Enter amount 
        self.entry_amount = ctk.CTkEntry(self.root, width=220, placeholder_text="Amount to deposit")
        self.entry_amount.place(relx=0.5, rely=0.3, anchor="center")

        # Enter description
        self.description = ctk.CTkEntry(self.root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.4, anchor="center")

        # Scroll down menu to select category
        cursor.execute("SELECT id, name FROM category")
        categories = cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        self.category_ids = [cat[0] for cat in categories]

        self.category_menu = ctk.CTkComboBox(self.root, values=category_names)
        self.category_menu.place(relx=0.5, rely=0.5, anchor="center")
        self.category_menu.set("Select a category")

        # Error message
        self.error_label = ctk.CTkLabel(self.root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")

        # Submit button
        validate_button = ctk.CTkButton(self.root, text="Deposit", command=self.validate_deposit)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")

        # Back button
        back_button = ctk.CTkButton(self.root, text="Back", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def validate_deposit(self):
        try:
            amount = Decimal(self.entry_amount.get())
            description = self.description.get()
            category_name = self.category_menu.get()

            # Check fields
            if amount <= 0:
                self.error_label.configure(text="The amount must be positive")
                return

            if not description:
                self.error_label.configure(text="Please enter a description")
                return

            if category_name == "Select a category":
                self.error_label.configure(text="Please choose a category")
                return

            # Get the category ID
            category_index = self.category_menu.cget("values").index(category_name)
            category_id = self.category_ids[category_index]

            # Update account balance
            new_balance = self.user_balance + Decimal(str(amount))
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))

            # Creation of a unique reference
            reference = f"DEP-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Add transaction 
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'deposit')
            """, (description, amount, reference, self.account_id, category_id))

            mydb.commit()

            # Display updated balance
            self.update_balance()

            # Confirmation message
            # self.app_manager.show_success("Success", f"Deposit of {amount}€ completed successfully!")

            # Return to transaction screen
            self.display_transaction()

        except ValueError:
            self.error_label.configure(text="Please enter a valid amount")

    def withdrawal(self):
        self.app_manager.clear_screen()

        # Title
        title_label = ctk.CTkLabel(self.root, text="Withdraw", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Enter amount
        self.entry_withdrawal = ctk.CTkEntry(self.root, width=220, placeholder_text="Amount to withdraw")
        self.entry_withdrawal.place(relx=0.5, rely=0.3, anchor="center")

        # Enter description
        self.description = ctk.CTkEntry(self.root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.4, anchor="center")

        # Scroll down menu to select category 
        cursor.execute("SELECT id, name FROM category")
        categories = cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        self.category_ids = [cat[0] for cat in categories]

        self.category_menu = ctk.CTkComboBox(self.root, values=category_names)
        self.category_menu.place(relx=0.5, rely=0.5, anchor="center")
        self.category_menu.set("Select a category")

        # Error message
        self.error_label = ctk.CTkLabel(self.root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")

        # Confirmation button
        validate_button = ctk.CTkButton(self.root, text="Withdraw", command=self.validate_withdrawal)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")

        # Back button
        back_button = ctk.CTkButton(self.root, text="Back", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def validate_withdrawal(self):
        try:
            amount = Decimal(self.entry_withdrawal.get())
            description = self.description.get()
            category_name = self.category_menu.get()

            # Check fields
            if amount <= 0:
                self.error_label.configure(text="The amount must be positive")
                return

            if not description:
                self.error_label.configure(text="Please enter a description")
                return

            if category_name == "Select a category":
                self.error_label.configure(text="Please choose a category")
                return

            if amount > self.user_balance:
                self.error_label.configure(text="Insufficient balance")
                return

            # Get the category ID
            category_index = self.category_menu.cget("values").index(category_name)
            category_id = self.category_ids[category_index]

            # Update the balance
            new_balance = self.user_balance - amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))

            # Creation of a unique reference
            reference = f"WIT-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Add transaction
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'withdrawal')
            """, (description, amount, reference, self.account_id, category_id))

            mydb.commit()

            # Display updated balance
            self.update_balance()

            # Confirmation message
            # self.app_manager.show_success("Success", f"Withdrawal of {amount}€ completed successfully!")

            # Return to transaction screen
            self.display_transaction()

        except ValueError:
            self.error_label.configure(text="Please enter a valid amount")

    def transfer(self):
        self.app_manager.clear_screen()

        # Title
        title_label = ctk.CTkLabel(self.root, text="Make a transfer", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Iban field
        self.iban_entry = ctk.CTkEntry(self.root, width=220, placeholder_text="Recipient IBAN")
        self.iban_entry.place(relx=0.5, rely=0.2, anchor="center")

        # Enter amount
        self.transfer_amount = ctk.CTkEntry(self.root, width=220, placeholder_text="Amount to transfer")
        self.transfer_amount.place(relx=0.5, rely=0.3, anchor="center")

        # Enter description
        self.description = ctk.CTkEntry(self.root, width=220, placeholder_text="Description")
        self.description.place(relx=0.5, rely=0.4, anchor="center")

        # Error message
        self.error_label = ctk.CTkLabel(self.root, text="", text_color="red")
        self.error_label.place(relx=0.5, rely=0.6, anchor="center")

        # Confirmation button
        validate_button = ctk.CTkButton(self.root, text="Transfer", command=self.validate_transfer)
        validate_button.place(relx=0.5, rely=0.7, anchor="center")

        # Back button
        back_button = ctk.CTkButton(self.root, text="Back", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def validate_transfer(self):
        try:
            iban = self.iban_entry.get()
            amount = Decimal(self.transfer_amount.get())
            description = self.description.get()
        
            # Verify input
            if not iban:
                self.error_label.configure(text="Enter IBAN")
                return
            
            if amount <= 0:
                self.error_label.configure(text="Amount must be positive")
                return
            
            if amount > self.user_balance:
                self.error_label.configure(text="Insuficient balance")
                return
            
            if not description:
                self.error_label.configure(text="Enter decription")
                return
            
            # Get account infos 
            cursor.execute("SELECT id, user_id, type FROM account WHERE iban = %s", (iban,))
            dest_account = cursor.fetchone()
        
            if not dest_account:
                self.error_label.configure(text="IBAN invalide")
                return
            
            dest_account_id, dest_user_id, dest_account_type = dest_account
        
            # Verify if transafert in internal
            is_internal_transfer = dest_user_id == self.user_id
        
            # Update balance
            new_balance = self.user_balance - amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_balance, self.account_id))
        
            # Update balance receiver
            cursor.execute("SELECT balance FROM account WHERE id = %s", (dest_account_id,))
            dest_balance = cursor.fetchone()[0]
            new_dest_balance = dest_balance + amount
            cursor.execute("UPDATE account SET balance = %s WHERE id = %s", (new_dest_balance, dest_account_id))
        
            # Create references
            out_reference = f"OUT-{self.user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            in_reference = f"IN-{dest_user_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
            # Select category
            if is_internal_transfer:
                cursor.execute("SELECT id FROM category WHERE name = 'Internal Transfert'")
            else:
                cursor.execute("SELECT id FROM category WHERE name = 'Other'")
            
            category_id = cursor.fetchone()[0]
        
            # Substranct transaction 
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'outgoing_transfer')
            """, (description, amount, out_reference, self.account_id, category_id))
        
            # Add transaction to receiving account
            cursor.execute("""
                INSERT INTO transaction (date, description, amount, reference, account_id, category_id, transaction_type)
                VALUES (NOW(), %s, %s, %s, %s, %s, 'incoming_transfer')
            """, (f"transaction received: {description}", amount, in_reference, dest_account_id, category_id))
        
            mydb.commit()
        
            # Update balance
            self.update_balance()
        
            # Back button
            self.display_transaction()
        
        except ValueError:
            self.error_label.configure(text="Veuillez entrer un montant valide")


    def show_history(self):
        self.app_manager.clear_screen()

        # Title
        title_label = ctk.CTkLabel(self.root, text="History of transactions", font=("Arial", 18, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Sort options
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.place(relx=0.5, rely=0.2, anchor="center")

        # Scroll down menu for the type of transaction
        type_label = ctk.CTkLabel(filter_frame, text="Type:")
        type_label.grid(row=0, column=0, padx=5, pady=5)

        types = ["All", "Deposit", "Withdrawal", "Incoming transfer", "outgoing transfer"]
        self.type_menu = ctk.CTkComboBox(filter_frame, values=types)
        self.type_menu.grid(row=0, column=1, padx=5, pady=5)
        self.type_menu.set("All")

        # Sort button
        filter_button = ctk.CTkButton(filter_frame, text="Sort", command=self.apply_filters)
        filter_button.grid(row=0, column=2, padx=5, pady=5)

        # Transaction display area
        self.history_frame = ctk.CTkScrollableFrame(self.root, width=600, height=300)
        self.history_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load transactions
        self.load_transactions()

        # Back button
        back_button = ctk.CTkButton(self.root, text="Back", command=self.display_transaction)
        back_button.place(relx=0.5, rely=0.85, anchor="center")

    def load_transactions(self, type_filter=None):
        # Clean the history frame
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Column titles
        header_frame = ctk.CTkFrame(self.history_frame)
        header_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(header_frame, text="Date", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Description", width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Amount", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Type", width=150).pack(side="left", padx=5)

        # SQL request based on sort requested
        query = """
            SELECT t.date, t.description, t.amount, t.transaction_type, c.name
            FROM transaction t
            JOIN category c ON t.category_id = c.id
            WHERE t.account_id = %s
        """
        params = [self.account_id]

        if type_filter and type_filter != "All":
            type_map = {
                "Deposit": "deposit",
                "Withdrawal": "withdrawal",
                "Incoming transfer": "incoming_transfer",
                "Outgoing transfer": "outgoing_transfer"
            }
            query += " AND t.transaction_type = %s"
            params.append(type_map[type_filter])

        query += " ORDER BY t.date DESC"

        cursor.execute(query, params)
        transactions = cursor.fetchall()

        if not transactions:
            no_trans = ctk.CTkLabel(self.history_frame, text="No transaction found")
            no_trans.pack(pady=20)
            return

        # Display each transaction
        for date, desc, amount, trans_type, category in transactions:
            trans_frame = ctk.CTkFrame(self.history_frame)
            trans_frame.pack(fill="x", pady=2)

            # Format date
            date_str = date.strftime("%d/%m/%Y")

            # Format the type
            type_map = {
                "deposit": "Deposit",
                "withdrawal": "Withdrawal",
                "incoming_transfer": "Incoming transfer",
                "outgoing_transfer": "Outgoing transfer"
            }
            type_str = type_map.get(trans_type, trans_type)

            # Format the type with colors
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
        self.app_manager.clear_screen()

        # Title
        title_label = ctk.CTkLabel(self.root, text="Transactions", font=("Arial", 20, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Balance display
        balance_label = ctk.CTkLabel(self.root,
text=f"Current balance: {self.user_balance}€",
font=("Arial", 16))
        balance_label.place(relx=0.5, rely=0.2, anchor="center")

        # Buttons for various operations
        deposit_button = ctk.CTkButton(self.root, text="Make a deposit",command=self.deposit,width=200, height=40)
        deposit_button.place(relx=0.5, rely=0.35, anchor="center")

        withdrawal_button = ctk.CTkButton(self.root, text="Make a withdrawal",command=self.withdrawal,width=200, height=40)
        withdrawal_button.place(relx=0.5, rely=0.45, anchor="center")

        transfer_button = ctk.CTkButton(self.root, text="Make a transfer",command=self.transfer,width=200, height=40)
        transfer_button.place(relx=0.5, rely=0.55, anchor="center")

        history_button = ctk.CTkButton(self.root, text="Show history of transactions",command=self.show_history,width=200, height=40)
        history_button.place(relx=0.5, rely=0.65, anchor="center")

        # Back button
        back_button = ctk.CTkButton(self.root, text="Back to dashboard",command=self.back_to_dashboard,width=200, height=40)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

    def back_to_dashboard(self):
        from dashboard import Dashboard
        dashboard = Dashboard(self.app_manager)
        dashboard.user_id = self.user_id
        dashboard.display_dashboard()