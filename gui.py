import tkinter as tk
from tkinter import messagebox, simpledialog

import os
import sys

from vault import Vault
from auth import AuthManager
from clipboard import ClipboardManager
from generator import PasswordGenerator
from strength import PasswordStrengthMeter
from config import load_settings, save_settings
from backup import create_backup
from import_export import export_vault, import_vault
from tkinter import filedialog

def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)


class LouketoGUI:

    DARK_THEME = {
        "bg": "#1e1e1e",
        "fg": "white",
        "entry_bg": "#2b2b2b",
        "button_bg": "#3c3f41"
    }

    LIGHT_THEME = {
        "bg": "#f0f0f0",
        "fg": "black",
        "entry_bg": "white",
        "button_bg": "#e0e0e0"
    }

    def __init__(self, root):

        self.root = root
        
        settings = load_settings()
        self.theme = settings.get("theme", "dark")

        self.root.title("Louketo")
        self.root.iconbitmap(resource_path("icon.ico"))
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e1e")

        # -------------------------
        # AUTH
        # -------------------------

        self.auth = AuthManager()

        if not self.auth.master_password_exists():
            messagebox.showinfo(
                "Setup",
                "First time setup in CLI required."
            )
            root.destroy()
            return

        pwd = simpledialog.askstring(
            "Louketo Login",
            "Enter master password:",
            show="*"
        )

        if not pwd or not self.auth.check_password(pwd):
            messagebox.showerror(
                "Access denied",
                "Invalid master password."
            )
            root.destroy()
            return

        self.vault = Vault(pwd)
        self.clip = ClipboardManager()

        # -------------------------
        # UI ELEMENTS
        # -------------------------
        self.buttons = []

        self.search_frame = tk.Frame(root)
        self.search_frame.pack(pady=5)

        self.search_entry = tk.Entry(
            self.search_frame, 
            width=30
        )
        self.search_entry.grid(row=0, column=0, padx=5)

        btn_search = tk.Button(
            self.search_frame,
            text="Search",
            command=self.search_entries
        )
        btn_search.grid(row=0, column=1, padx=5)
        self.buttons.append(btn_search)

        btn_reset = tk.Button(
            self.search_frame,
            text="Reset",
            command=self.refresh_list
        )
        btn_reset.grid(row=0, column=2, padx=5)
        self.buttons.append(btn_reset)


        # =========================
        # TOGGLE THEME BUTTON
        # =========================

        btn_toggle = tk.Button(
            root,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        btn_toggle.pack(pady=5)

        self.buttons.append(btn_toggle)


        self.listbox = tk.Listbox(root, width=60)
        self.listbox.pack(pady=20)

        btn_frame = tk.Frame(root)
        btn_frame.pack()


        btn_refresh = tk.Button(
            btn_frame,
            text="Refresh",
            command=self.refresh_list
        )
        btn_refresh.grid(row=0, column=0, padx=5)

        self.buttons.append(btn_refresh)

        btn_copy_pwd = tk.Button(
            btn_frame,
            text="Copy Password",
            command=self.copy_password
        )
        btn_copy_pwd.grid(row=0, column=1, padx=5)
        self.buttons.append(btn_copy_pwd)

        btn_copy_login = tk.Button(
            btn_frame,
            text="Copy Login",
            command=self.copy_login
        )
        btn_copy_login.grid(row=0, column=2, padx=5)
        self.buttons.append(btn_copy_login)

        btn_delete = tk.Button(
            btn_frame,
            text="Delete Entry",
            command=self.delete_entry
        )
        btn_delete.grid(row=0, column=3, padx=5)
        self.buttons.append(btn_delete)

        btn_add = tk.Button(
            btn_frame,
            text="Add Entry",
            command=self.add_entry_window
        )
        
        btn_edit = tk.Button(
            btn_frame,
            text="Edit Entry",
            command=self.edit_entry_window
        )
        btn_edit.grid(row=0, column=5, padx=5)
        self.buttons.append(btn_edit)

        btn_backup = tk.Button(
            btn_frame,
            text="Backup Vault",
            command=self.backup_vault
        )
        btn_backup.grid(row=0, column=6, padx=5)
        self.buttons.append(btn_backup)

        btn_export = tk.Button(
            btn_frame,
            text="Export Vault",
            command=self.export_vault_gui
        )
        btn_export.grid(row=0, column=7, padx=5)
        self.buttons.append(btn_export)

        btn_import = tk.Button(
            btn_frame,
            text="Import Vault",
            command=self.import_vault_gui
        )
        btn_import.grid(row=0, column=8, padx=5)
        self.buttons.append(btn_import)

        btn_add.grid(row=0, column=4, padx=5)
        self.buttons.append(btn_add)

        self.apply_theme()
        self.refresh_list()

    # =========================

    def refresh_list(self):

        self.listbox.delete(0, tk.END)

        entries = self.vault.list_entries()

        for e in entries:
            self.listbox.insert(
                tk.END,
                f"{e.service} | {e.login}"
            )

    def apply_theme(self):

        theme = (
            self.DARK_THEME
            if self.theme == "dark"
            else self.LIGHT_THEME
        )

        self.root.configure(bg=theme["bg"])

        # Search frame
        self.search_frame.configure(bg=theme["bg"])

        # Entry
        self.search_entry.configure(
            bg=theme["entry_bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"]
        )

        # Listbox
        self.listbox.configure(
            bg=theme["entry_bg"],
            fg=theme["fg"]
        )

        # Buttons
        for btn in self.buttons:
            btn.configure(
                bg=theme["button_bg"],
                fg=theme["fg"]
            )


    # =========================
    # TOGGLE THEME
    # =========================

    def toggle_theme(self):

        self.theme = (
            "light"
            if self.theme == "dark"
            else "dark"
        )

        # ===== SAVE TO SETTINGS =====
        settings = load_settings()
        settings["theme"] = self.theme
        save_settings(settings)

        self.apply_theme()

    # =========================

    def search_entries(self):

        query = self.search_entry.get()

        if not query:
            self.refresh_list()
            return

        results = self.vault.search_entries(query)

        self.listbox.delete(0, tk.END)

        for e in results:
            self.listbox.insert(
                tk.END,
                f"{e.service} | {e.login}"
            )

    # =========================

    def get_selected_entry(self):

        try:
            index = self.listbox.curselection()[0]
            return self.vault.list_entries()[index]
        except:
            messagebox.showerror(
                "Error",
                "No entry selected."
            )
            return None

    # =========================

    def copy_password(self):

        entry = self.get_selected_entry()

        if entry:
            self.clip.copy(entry.password)
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard."
            )

    # =========================

    def copy_login(self):

        entry = self.get_selected_entry()

        if entry:
            self.clip.copy(entry.login)
            messagebox.showinfo(
                "Copied",
                "Login copied to clipboard."
            )

    # =========================

    def delete_entry(self):

        entry = self.get_selected_entry()

        if entry:
            self.vault.delete_entry(entry.service)
            self.refresh_list()

    # =========================

    def backup_vault(self):

        create_backup(self.vault.filename)

        messagebox.showinfo(
            "Backup",
            "Vault backup created."
        )

    # =========================

    def add_entry_window(self):

        window = tk.Toplevel(self.root)
        window.configure(bg="#1e1e1e")
        window.title("Add Entry")
        window.geometry("300x200")

        # =========================
        # STRENGTH METER INIT
        # =========================

        meter = PasswordStrengthMeter()

        tk.Label(window, text="Service").pack()
        service_entry = tk.Entry(
            window,
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )
        service_entry.pack()

        tk.Label(window, text="Login").pack()
        login_entry = tk.Entry(
            window,
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )
        login_entry.pack()

        tk.Label(window, text="Password").pack()
        
        password_entry = tk.Entry(
            window,
            show="*",
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )
        password_entry.pack()

        # =========================
        # SHOW / HIDE BUTTON
        # =========================

        def toggle_password():

            if password_entry.cget("show") == "":
                password_entry.config(show="*")
                toggle_btn.config(text="Show")
            else:
                password_entry.config(show="")
                toggle_btn.config(text="Hide")

        toggle_btn = tk.Button(
            window,
            text="Show",
            command=toggle_password
        )
        toggle_btn.pack()


        # =========================
        # STRENGTH LABEL
        # =========================

        strength_label = tk.Label(
            window,
            text="Strength: -"
        )
        strength_label.pack()

        # =========================
        # STRENGTH UPDATE FUNCTION
        # =========================

        def update_strength(*args):

            password = password_entry.get()

            if not password:
                strength_label.config(text="Strength: -")
                return

            score = meter.evaluate(password)
            label = meter.get_label(score)

            strength_label.config(
                text=f"Strength: {label}"
            )

        # LIVE UPDATE WHEN TYPING
        password_entry.bind(
            "<KeyRelease>",
            update_strength
        )

        # -------------------------
        # GENERATOR BUTTON
        # -------------------------

        def generate_password():

            gen = PasswordGenerator()
            clip = ClipboardManager()

            password = gen.generate(
                length=16,
                use_uppercase=True,
                use_numbers=True,
                use_symbols=True
            )

            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)

            clip.copy(password)

            update_strength()

        tk.Button(
            window,
            text="Generate Password",
            command=generate_password
        ).pack(pady=5)


        # -------------------------

        def save_entry():

            service = service_entry.get()
            login = login_entry.get()
            password = password_entry.get()

            if not service or not login or not password:
                messagebox.showerror(
                    "Error",
                    "All fields required."
                )
                return

            from models import Entry

            entry = Entry(service, login, password)
            self.vault.add_entry(entry)

            self.refresh_list()
            window.destroy()

        # -------------------------

        tk.Button(
            window,
            text="Save",
            command=save_entry
        ).pack(pady=10)

    # =========================
    # EDIT ENTRY WINDOW
    # =========================

    def edit_entry_window(self):

        entry = self.get_selected_entry()

        if not entry:
            return

        window = tk.Toplevel(self.root)
        window.configure(bg="#1e1e1e")
        window.title("Edit Entry")
        window.geometry("300x200")

        tk.Label(window, text="Service").pack()
        service_entry = tk.Entry(window)
        service_entry.insert(0, entry.service)
        service_entry.pack()

        tk.Label(window, text="Login").pack()
        login_entry = tk.Entry(window)
        login_entry.insert(0, entry.login)
        login_entry.pack()

        tk.Label(window, text="Password").pack()
        password_entry = tk.Entry(window, show="*")
        password_entry.insert(0, entry.password)
        password_entry.pack()

        # =========================
        # SAVE CHANGES
        # =========================
        def save_changes():

            new_service = service_entry.get()
            new_login = login_entry.get()
            new_password = password_entry.get()

            if not new_service or not new_login or not new_password:
                messagebox.showerror(
                    "Error",
                    "All fields required."
                )
                return

            # DELETE OLD
            self.vault.delete_entry(entry.service)

            # ADD UPDATED
            from models import Entry
            updated_entry = Entry(
                new_service,
                new_login,
                new_password
            )

            self.vault.add_entry(updated_entry)

            self.refresh_list()
            window.destroy()

        # =========================
        # BUTTON
        # =========================

        tk.Button(
            window,
            text="Save Changes",
            command=save_changes
        ).pack(pady=10)

    # =========================
    # EXPORT VAULT
    # =========================

    def export_vault_gui(self):

        messagebox.showwarning(
            "Security Warning",
            "Export creates a plaintext JSON file.\n"
            "Keep it secure."
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if not file_path:
            return

        export_vault(self.vault, file_path)

        messagebox.showinfo(
            "Export",
            "Vault exported successfully."
        )
    # =========================
    # IMPORT VAULT
    # =========================

    def import_vault_gui(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )

        if not file_path:
            return

        import_vault(self.vault, file_path)

        self.refresh_list()

        messagebox.showinfo(
            "Import",
            "Vault import completed."
        )


# =============================
# RUN GUI
# =============================

if __name__ == "__main__":

    root = tk.Tk()
    app = LouketoGUI(root)
    root.mainloop()
