import json
import os


SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "clipboard_clear_time": 5,
    "clipboard_auto_clear_enabled": True,
    "vault_auto_lock_enabled": True,
    "vault_auto_lock_time": 300,
    "theme": "dark"
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)

        for key, value in DEFAULT_SETTINGS.items():
            if key not in data:
                data[key] = value

        return data

    except:
        return DEFAULT_SETTINGS


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
