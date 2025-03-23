import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

# General config of the app
APP_NAME = "Budget Buddy"
PRIMARY_COLOR = "#2d8659"  # Dark green
SECONDARY_COLOR = "#3b3b3b"  # Dark grey
TEXT_COLOR = "#ffffff"  # White
ACCENT_COLOR = "#4CAF50"  # Light green

# Global config of CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# global variables
root = None

def init_root(size="800x600"):
    """Initialize main window"""
    global root
    root = ctk.CTk()
    root.title(APP_NAME)
    root.geometry(size)
    root.minsize(800, 600)
    return root

def clear_screen():
    """CLears all widgets from main screen"""
    if root:
        for widget in root.winfo_children():
            widget.destroy()

def show_info(title, message):
    """Display info message"""
    CTkMessagebox(title=title, message=message, icon="info")

def show_error(title, message):
    """Displays error message"""
    CTkMessagebox(title=title, message=message, icon="cancel")

def show_success(title, message):
    """Displays confirmation message"""
    CTkMessagebox(title=title, message=message, icon="check")

def show_confirmation(title, message):
    """Displays confirmation window"""
    msg = CTkMessagebox(title=title, message=message, icon="question", 
                        option_1="Yes", option_2="No")
    return msg.get() == "Yes"

def create_header(title):
    """Standard header for all pages"""
    header_frame = ctk.CTkFrame(root, height=80, fg_color=PRIMARY_COLOR)
    header_frame.pack(fill="x", pady=(0, 20))
    
    title_label = ctk.CTkLabel(header_frame, text=title, 
                              font=ctk.CTkFont(size=24, weight="bold"),
                              text_color=TEXT_COLOR)
    title_label.place(relx=0.5, rely=0.5, anchor="center")
    
    return header_frame

def create_footer():
    """Standard footer"""
    footer_frame = ctk.CTkFrame(root, height=50, fg_color=SECONDARY_COLOR)
    footer_frame.pack(fill="x", side="bottom")
    
    footer_label = ctk.CTkLabel(footer_frame, text=f"{APP_NAME} - Your financial ally",
                               font=ctk.CTkFont(size=12),
                               text_color=TEXT_COLOR)
    footer_label.place(relx=0.5, rely=0.5, anchor="center")
    
    return footer_frame

def admin_menu():
    """Displays admin dashboard"""
    clear_screen()
    header = create_header("Administrator dashboard")
    
    # Main content
    content_frame = ctk.CTkFrame(root)
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
    
    # Log-out button
    from customer import user
    btn_logout = ctk.CTkButton(content_frame, text="Sign out", 
                              height=40, font=ctk.CTkFont(size=14),
                              fg_color="#E53935", hover_color="#C62828",
                              command=user.log_menu)
    btn_logout.pack(pady=30, padx=20, fill="x")
    
    create_footer()