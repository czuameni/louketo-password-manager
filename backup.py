import os
import shutil
from datetime import datetime

BACKUP_DIR = "backups"


def ensure_backup_dir():

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def create_backup(vault_path):

    ensure_backup_dir()

    if not os.path.exists(vault_path):
        print("[Backup] No vault file found.")
        return

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    backup_name = (
        f"vault_backup_{timestamp}.dat"
    )

    backup_path = os.path.join(
        BACKUP_DIR,
        backup_name
    )

    shutil.copy2(vault_path, backup_path)

    print(f"[Backup] Created: {backup_name}")