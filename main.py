from vault import Vault
from models import Entry
from auth import AuthManager
from generator import PasswordGenerator
from clipboard import ClipboardManager
from strength import PasswordStrengthMeter

# ===== AUTO-LOCK IMPORT =====
from vault_lock import (
    start_auto_lock_timer,
    is_vault_locked,
    reset_lock_flag,
    register_activity
)


def show_menu():
    print("\n==== LOUKETO PASSWORD MANAGER ====")
    print("1. Add entry")
    print("2. Show all entries")
    print("3. Search entry")
    print("4. Delete entry")
    print("5. Generate password")
    print("6. Password strength audit")
    print("7. Exit")


def add_entry(vault):
    service = input("Service: ")
    login = input("Login: ")
    password = input("Password: ")

    entry = Entry(service, login, password)
    vault.add_entry(entry)

    print("Entry added.")


def show_entries(vault):
    entries = vault.list_entries()

    if not entries:
        print("No entries.")
        return

    for e in entries:
        print(f"{e.service} | {e.login} | {e.password}")


def search_entries(vault):

    query = input("Search service: ")
    results = vault.search_entries(query)

    if not results:
        print("No matches.")
        return

    print("\nResults:")

    for i, e in enumerate(results, start=1):
        print(f"{i}. {e.service} | {e.login}")

    # -------------------------
    # Clipboard options
    # -------------------------

    choice = input(
        "\nSelect entry number to copy data (Enter to skip): "
    )

    if not choice:
        return

    try:
        index = int(choice) - 1
        entry = results[index]

        clip = ClipboardManager()

        print("\n1. Copy password")
        print("2. Copy login")

        action = input("> ")

        if action == "1":
            clip.copy(entry.password)

        elif action == "2":
            clip.copy(entry.login)

        else:
            print("Invalid option.")

    except:
        print("Invalid selection.")



def delete_entry(vault):
    service = input("Service to delete: ")
    vault.delete_entry(service)
    print("Deleted (if existed).")


# =========================
# PASSWORD GENERATOR CLI
# =========================

def generate_password():

    gen = PasswordGenerator()
    clip = ClipboardManager()

    try:
        length = int(input("Length (default 12): ") or 12)

        use_upper = input("Uppercase? (y/n): ").lower() == "y"
        use_numbers = input("Numbers? (y/n): ").lower() == "y"
        use_symbols = input("Symbols? (y/n): ").lower() == "y"

        password = gen.generate(
            length,
            use_upper,
            use_numbers,
            use_symbols
        )

        print(f"\nGenerated password:\n{password}\n")

        copy_choice = input("Copy to clipboard? (y/n): ").lower()

        if copy_choice == "y":
            clip.copy(password)

    except Exception as e:
        print(f"Error: {e}")

def audit_passwords(vault):

    meter = PasswordStrengthMeter()

    entries = vault.list_entries()

    if not entries:
        print("No entries to audit.")
        return

    print("\n=== PASSWORD STRENGTH AUDIT ===\n")

    for e in entries:

        score = meter.evaluate(e.password)
        label = meter.get_label(score)

        print(
            f"{e.service} | {e.login} "
            f"→ {label} (score: {score})"
        )


def main():

    auth = AuthManager()

    # First time setup
    if not auth.master_password_exists():
        auth.set_master_password()

    # Login
    master_password = auth.verify_master_password()

    if not master_password:
        return

    vault = Vault(master_password)

    start_auto_lock_timer()

    while True:
        # Auto-lock check
        if is_vault_locked():

            print("Vault locked.")
            master_password = auth.verify_master_password()

            if not master_password:
                print("Auth failed.")
                break

            vault = Vault(master_password)

            reset_lock_flag()
            start_auto_lock_timer()

        show_menu()
        choice = input("> ")

        register_activity()

        if choice == "1":
            add_entry(vault)

        elif choice == "2":
            show_entries(vault)

        elif choice == "3":
            search_entries(vault)

        elif choice == "4":
            delete_entry(vault)

        elif choice == "5":
            generate_password()

        elif choice == "6":
            audit_passwords(vault)

        elif choice == "7":
            print("Bye.")
            break



if __name__ == "__main__":
    main()
