import json
from datetime import datetime
from models import Entry

def export_vault(vault, file_path=None):

    entries = vault.list_entries()

    data = []

    for e in entries:
        data.append({
            "service": e.service,
            "login": e.login,
            "password": e.password
        })

    if not file_path:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = (
            f"vault_export_{timestamp}.json"
        )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[Export] Created: {file_path}")


def import_vault(vault, file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:

        entry = Entry(
            item["service"],
            item["login"],
            item["password"]
        )

        vault.add_entry(entry)

    print("[Import] Completed.")
