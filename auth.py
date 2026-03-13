import hashlib
import os
import getpass


class AuthManager:

    def __init__(self, filename="master.hash"):
        self.filename = filename

    # -------------------------

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # =========================
    # CHECK PASSWORD (GUI LOGIN)
    # =========================

    def check_password(self, password):

        if not self.master_password_exists():
            return False

        with open(self.filename, "r") as f:
            stored_hash = f.read()

        hashed = self.hash_password(password)

        return hashed == stored_hash


    # -------------------------

    def master_password_exists(self):
        return os.path.exists(self.filename)

    # -------------------------

    def set_master_password(self):

        print("=== FIRST TIME SETUP ===")

        while True:
            pwd1 = getpass.getpass("Set master password: ")
            pwd2 = getpass.getpass("Confirm password: ")

            if pwd1 != pwd2:
                print("Passwords do not match.\n")
                continue

            hashed = self.hash_password(pwd1)

            with open(self.filename, "w") as f:
                f.write(hashed)

            print("Master password set.\n")
            break

    # -------------------------

    def verify_master_password(self):

        with open(self.filename, "r") as f:
            stored_hash = f.read()

        attempts = 3

        while attempts > 0:

            pwd = getpass.getpass("Enter master password: ")
            hashed = self.hash_password(pwd)

            if hashed == stored_hash:
                print("Access granted.\n")
                return pwd

            attempts -= 1
            print(f"Wrong password. Attempts left: {attempts}")

        print("Access denied.")
        return None
