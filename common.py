import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

# Configuration globale de l'application
APP_NAME = "Budget Buddy"
PRIMARY_COLOR = "#2d8659"  # Vert foncé
SECONDARY_COLOR = "#3b3b3b"  # Gris foncé
TEXT_COLOR = "#ffffff"  # Blanc
ACCENT_COLOR = "#4CAF50"  # Vert clair

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Variables globales
root = None

def init_root(size="800x600"):
    """Initialise la fenêtre principale"""
    global root
    root = ctk.CTk()
    root.title(APP_NAME)
    root.geometry(size)
    root.minsize(800, 600)
    return root

def clear_screen():
    """Efface tous les widgets de la fenêtre principale"""
    if root:
        for widget in root.winfo_children():
            widget.destroy()

def show_info(title, message):
    """Affiche un message d'information"""
    CTkMessagebox(title=title, message=message, icon="info")

def show_error(title, message):
    """Affiche un message d'erreur"""
    CTkMessagebox(title=title, message=message, icon="cancel")

def show_success(title, message):
    """Affiche un message de succès"""
    CTkMessagebox(title=title, message=message, icon="check")

def show_confirmation(title, message):
    """Affiche une boîte de dialogue de confirmation"""
    msg = CTkMessagebox(title=title, message=message, icon="question", 
                        option_1="Oui", option_2="Non")
    return msg.get() == "Oui"

def create_header(title):
    """Crée un en-tête standardisé pour les pages"""
    header_frame = ctk.CTkFrame(root, height=80, fg_color=PRIMARY_COLOR)
    header_frame.pack(fill="x", pady=(0, 20))
    
    title_label = ctk.CTkLabel(header_frame, text=title, 
                              font=ctk.CTkFont(size=24, weight="bold"),
                              text_color=TEXT_COLOR)
    title_label.place(relx=0.5, rely=0.5, anchor="center")
    
    return header_frame

def create_footer():
    """Crée un pied de page standardisé"""
    footer_frame = ctk.CTkFrame(root, height=50, fg_color=SECONDARY_COLOR)
    footer_frame.pack(fill="x", side="bottom")
    
    footer_label = ctk.CTkLabel(footer_frame, text=f"{APP_NAME} - Votre allié financier",
                               font=ctk.CTkFont(size=12),
                               text_color=TEXT_COLOR)
    footer_label.place(relx=0.5, rely=0.5, anchor="center")
    
    return footer_frame

def admin_menu():
    """Affiche le menu administrateur"""
    clear_screen()
    header = create_header("Menu Administrateur")
    
    # Contenu principal
    content_frame = ctk.CTkFrame(root)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Options administrateur
    btn_users = ctk.CTkButton(content_frame, text="Gestion des utilisateurs", 
                             height=40, font=ctk.CTkFont(size=14))
    btn_users.pack(pady=10, padx=20, fill="x")
    
    btn_accounts = ctk.CTkButton(content_frame, text="Gestion des comptes", 
                                height=40, font=ctk.CTkFont(size=14))
    btn_accounts.pack(pady=10, padx=20, fill="x")
    
    btn_stats = ctk.CTkButton(content_frame, text="Statistiques globales", 
                             height=40, font=ctk.CTkFont(size=14))
    btn_stats.pack(pady=10, padx=20, fill="x")
    
    # Bouton de déconnexion
    from customer import user
    btn_logout = ctk.CTkButton(content_frame, text="Déconnexion", 
                              height=40, font=ctk.CTkFont(size=14),
                              fg_color="#E53935", hover_color="#C62828",
                              command=user.log_menu)
    btn_logout.pack(pady=30, padx=20, fill="x")
    
    create_footer()