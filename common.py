import customtkinter as ctk

# General config of the app
APP_NAME = "Budget Buddy"
PRIMARY_COLOR = "#2d8659"  # Dark green
SECONDARY_COLOR = "#3b3b3b"  # Dark grey
TEXT_COLOR = "#ffffff"  # White
ACCENT_COLOR = "#4CAF50"  # Light green

# Global config of CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class AppManager:
    def __init__(self, size="800x600"):
        """Initialize main window"""
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry(size)
        self.root.minsize(800, 600)
    
    def get_root(self):
        """Returns the root window"""
        return self.root
    
    def clear_screen(self):
        """Clears all widgets from main screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, title):
        """Standard header for all pages"""
        header_frame = ctk.CTkFrame(self.root, height=80, fg_color=PRIMARY_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(header_frame, text=title, 
                                    font=ctk.CTkFont(size=24, weight="bold"),
                                    text_color=TEXT_COLOR)
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        return header_frame
    
    def create_footer(self):
        """Standard footer"""
        footer_frame = ctk.CTkFrame(self.root, height=50, fg_color=SECONDARY_COLOR)
        footer_frame.pack(fill="x", side="bottom")
        
        footer_label = ctk.CTkLabel(footer_frame, text=f"{APP_NAME} - Your financial ally",
                                    font=ctk.CTkFont(size=12),
                                    text_color=TEXT_COLOR)
        footer_label.place(relx=0.5, rely=0.5, anchor="center")
        
        return footer_frame
    
    def admin_menu(self):
        """Displays admin dashboard"""
        self.clear_screen()
        self.create_header("Administrator dashboard")
        
        # Main content
        content_frame = ctk.CTkFrame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Administrator options
        btn_users = ctk.CTkButton(content_frame, text="Manage users", 
                                height=40, font=ctk.CTkFont(size=14))
        btn_users.pack(pady=10, padx=20, fill="x")
        
        btn_accounts = ctk.CTkButton(content_frame, text="Manage accounts", 
                                    height=40, font=ctk.CTkFont(size=14))
        btn_accounts.pack(pady=10, padx=20, fill="x")
        
        btn_stats = ctk.CTkButton(content_frame, text="Global statistics", 
                                height=40, font=ctk.CTkFont(size=14))
        btn_stats.pack(pady=10, padx=20, fill="x")
        
        # Import moved inside method to avoid circular import issues
        from customer import user
        
        # Log-out button with a reference to user.log_menu
        # This will need to be updated as well to use the AppManager instance
        btn_logout = ctk.CTkButton(content_frame, text="Sign out", 
                                height=40, font=ctk.CTkFont(size=14),
                                fg_color="#E53935", hover_color="#C62828",
                                command=lambda: user.log_menu(self))  # Pass self as AppManager instance
        btn_logout.pack(pady=30, padx=20, fill="x")
        
        self.create_footer()