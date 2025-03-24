import customtkinter as ctk
from database import *
from transaction import Transaction
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class Dashboard:
    def __init__(self, app_manager=None, user_id=None):
        self.app_manager = app_manager
        self.user_id = user_id
        self.accounts = []
        self.selected_account_id = None
        self.transaction = None

    def get_user_info(self):
        """Gets user information and related accounts"""
        cursor.execute("""
            SELECT id, first_name, name
            FROM user
            WHERE id = %s
        """, (self.user_id,))
        user_info = cursor.fetchone()

        if user_info:
            self.user_id, self.first_name, self.name = user_info

            # Initialize class Transaction
            self.transaction = Transaction(self.user_id, self.app_manager)

            # gets all accounts of user
            cursor.execute("""
                SELECT id, type, balance, iban FROM account WHERE user_id = %s
            """, (self.user_id,))
            self.accounts = cursor.fetchall()

            # Sets the first account as default
            if self.accounts:
                self.selected_account_id = self.accounts[0][0]
        else:
            self.user_id, self.first_name, self.name, self.accounts = None, None, None, []

    def update_account_info(self, choice=None):
        """Updates information with account selected"""
        account_type = self.account_options.get()

        for acc_id, acc_type, balance, iban in self.accounts:
            if acc_type.capitalize() == account_type:
                self.selected_account_id = acc_id
                self.balance_var.set(f"Balance : {balance}€")
                self.iban_var.set(f"IBAN : {iban}")
                self.load_transactions()
                self.create_monthly_stats()
                break

    def add_savings_account(self):
        """Add a savings account for user"""
        import random
        import string

        iban = "FR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

        cursor.execute("""
            INSERT INTO account (balance, iban, user_id, type)
            VALUES (%s, %s, %s, %s)
        """, (0, iban, self.user_id, "savings"))

        mydb.commit()

        # Updates the accounts list
        self.get_user_info()

        # Displays confirmation message
        # CTkMessagebox(title="Success", message="Savings account successfully created!", icon="check")

        # Updates the display
        self.display_dashboard()

    def create_monthly_stats(self):
        """Creates a chart with monthly incomes and expenditure"""
        # Clean display frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Gets the data for current month
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

            # Creates chart
            figure = plt.Figure(figsize=(5, 2), dpi=100)
            ax = figure.add_subplot(111)

            labels = ['Income', 'Expenditure']
            values = [income, expense]
            colors = ['#4CAF50', '#E53935']

            ax.bar(labels, values, color=colors)
            ax.set_title('Monthly summary')

            # Add chart to the frame
            canvas = FigureCanvasTkAgg(figure, self.stats_frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)

            # Display text statistics
            stats_label = ctk.CTkLabel(
                self.stats_frame,
                text=f"Income: {income}€ | Expenditure: {expense}€ | Summary: {income-expense}€",
                font=("Arial", 14)
            )
            stats_label.pack(pady=10)

            # Display an alert if balance is low
            if self.accounts and self.selected_account_id:
                for acc_id, acc_type, balance, iban in self.accounts:
                    if acc_id == self.selected_account_id and balance < 100:
                        alert_label = ctk.CTkLabel(
                            self.stats_frame,
                            text="⚠️ ALERT: Your account balance is low!",
                            font=("Arial", 14, "bold"),
                            text_color="red"
                        )
                        alert_label.pack(pady=5)

    def load_transactions(self):
        """Loads recent transactions for the account selected"""
        # Reset the frame
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
            #  Add header
            header_frame = ctk.CTkFrame(self.transactions_frame)
            header_frame.pack(fill="x", pady=(0, 5))

            ctk.CTkLabel(header_frame, text="Date", width=100).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Description", width=200).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Amount", width=100).pack(side="left", padx=5)

            # Add transactions
            for date, desc, amount, trans_type in transactions:
                trans_frame = ctk.CTkFrame(self.transactions_frame, fg_color="transparent")
                trans_frame.pack(fill="x", pady=2)

                date_str = date.strftime("%d/%m/%Y")

                # Format the amount based on the type (income, spending)
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
            no_trans = ctk.CTkLabel(self.transactions_frame, text="No recent transaction.")
            no_trans.pack(pady=20)

    def display_dashboard(self):
        """Displays main dashboard"""
        self.get_user_info()
        self.app_manager.clear_screen()

        # Header
        header = self.app_manager.create_header(f"Dashboard - {self.first_name} {self.name}")

        # Main frame
        main_frame = ctk.CTkFrame(self.app_manager.get_root())
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Left panel - Account selection and info
        left_panel = ctk.CTkFrame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Account selection
        account_frame = ctk.CTkFrame(left_panel)
        account_frame.pack(pady=10, fill="x")

        account_label = ctk.CTkLabel(account_frame, text="Account:", font=("Arial", 14))
        account_label.pack(side="left", padx=10)

        if self.accounts:
            # Dropdown menu
            self.account_options = ctk.CTkComboBox(
                account_frame,
                values=[acc_type.capitalize() for _, acc_type, _, _ in self.accounts],
                command=self.update_account_info
            )
            self.account_options.pack(side="left", padx=10, fill="x", expand=True)
            self.account_options.set(self.accounts[0][1].capitalize())

            # Account information
            self.balance_var = ctk.StringVar(value=f"Balance : {self.accounts[0][2]}€")
            self.iban_var = ctk.StringVar(value=f"IBAN : {self.accounts[0][3]}")

            info_frame = ctk.CTkFrame(left_panel)
            info_frame.pack(pady=10, fill="x")

            balance_label = ctk.CTkLabel(info_frame, textvariable=self.balance_var, font=("Arial", 16, "bold"))
            balance_label.pack(pady=5)

            iban_label = ctk.CTkLabel(info_frame, textvariable=self.iban_var, font=("Arial", 12))
            iban_label.pack(pady=5)

            # Button to add a savings account
            add_savings_button = ctk.CTkButton(
                left_panel,
                text="Add a savings account",
                command=self.add_savings_account
            )
            add_savings_button.pack(pady=10, fill="x")

            # Buttons for transactions
            transaction_button = ctk.CTkButton(
                left_panel,
                text="Manage my transactions",
                command=self.transaction.display_transaction
            )
            transaction_button.pack(pady=10, fill="x")

            # Recent transactions
            trans_label = ctk.CTkLabel(left_panel, text="Recent transactions", font=("Arial", 16, "bold"))
            trans_label.pack(pady=(20, 10))

            self.transactions_frame = ctk.CTkFrame(left_panel)
            self.transactions_frame.pack(fill="both", expand=True, pady=5)

            # Right panel - Statistics and chart
            right_panel = ctk.CTkFrame(main_frame)
            right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

            stats_label = ctk.CTkLabel(right_panel, text="Résumé financier", font=("Arial", 16, "bold"))
            stats_label.pack(pady=(10, 20))

            self.stats_frame = ctk.CTkFrame(right_panel)
            self.stats_frame.pack(fill="both", expand=True, pady=5)

            # Load initial data
            self.load_transactions()
            self.create_monthly_stats()
        else:
            no_account_label = ctk.CTkLabel(
                left_panel,
                text="You have no accoutn yet.",
                font=("Arial", 14)
            )
            no_account_label.pack(pady=20)

        # Log out button
        from customer import Customer
        logout_button = ctk.CTkButton(
            main_frame,
            text="Sign out",
            command=lambda: Customer(self.app_manager).log_menu(),
            fg_color="#E53935",
            hover_color="#C62828"
        )
        logout_button.pack(side="bottom", pady=20)

        self.app_manager.create_footer()