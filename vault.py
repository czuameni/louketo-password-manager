import json
import os
import sys

from models import Entry
from crypto import CryptoManager
from backup import create_backup

def get_app_path(filename):

    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)

class Vault:

    def __init__(self, master_password, filename="vault.dat"):

        self.filename = get_app_path(filename)

        self.entries = []
        self.crypto = CryptoManager()
        self.key = self.crypto.generate_key(master_password)

        if os.path.exists(self.filename):
            self.load()

    def add_entry(self, entry):

        entry.password = self.crypto.encrypt_password(
            entry.password
        )

        self.entries.append(entry)
        self.save()

    def list_entries(self):

        decrypted_list = []

        for e in self.entries:
            decrypted_entry = Entry(
                e.service,
                e.login,
                self.crypto.decrypt_password(e.password)
            )
            decrypted_list.append(decrypted_entry)

        return decrypted_list

    def delete_entry(self, service):

        self.entries = [
            e for e in self.entries
            if e.service.lower() != service.lower()
        ]

        self.save()

    def search_entries(self, query):

        results = [
            e for e in self.entries
            if query.lower() in e.service.lower()
        ]

        decrypted_results = []

        for e in results:
            decrypted_entry = Entry(
                e.service,
                e.login,
                self.crypto.decrypt_password(e.password)
            )
            decrypted_results.append(decrypted_entry)

        return decrypted_results


    def save(self):

        try:
            create_backup(self.filename)
        except:
            pass

        data = json.dumps(
            [e.to_dict() for e in self.entries]
        )

        encrypted_data = self.crypto.encrypt_vault(
            data,
            self.key
        )

        with open(self.filename, "w") as f:
            f.write(encrypted_data)

    def load(self):

        with open(self.filename, "r") as f:
            encrypted_data = f.read()

        decrypted_data = self.crypto.decrypt_vault(
            encrypted_data,
            self.key
        )

        data = json.loads(decrypted_data)

        self.entries = [
            Entry.from_dict(item)
            for item in data
        ]
