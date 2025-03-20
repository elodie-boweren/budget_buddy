import customtkinter as ctk

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

root = ctk.CTk()
root.geometry("800x600")


def admin_menu():
    clear_screen()
    label = ctk.CTkLabel(root, text="Menu Administrateur")
    label.pack(pady=10)