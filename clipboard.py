import pyperclip
import threading
import time
import secrets
import string

from config import load_settings


settings = load_settings()

CLIPBOARD_CLEAR_TIME = settings.get(
    "clipboard_clear_time",
    5
)

AUTO_CLEAR_ENABLED = settings.get(
    "clipboard_auto_clear_enabled",
    True
)

_clear_timer = None
_timer_lock = threading.Lock()


def _random_string(length=32):

    alphabet = (
        string.ascii_letters +
        string.digits
    )

    return ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def clear_clipboard():

    try:
        print("[Clipboard] Secure wipe started")

        # Pass 1 — random data
        pyperclip.copy(_random_string())

        # Pass 2 — zeros
        pyperclip.copy("0" * 32)

        # Pass 3 — random data
        pyperclip.copy(_random_string())

        # Final pass — empty
        pyperclip.copy("")

        print("[Clipboard] Securely cleared")

    except Exception as e:
        print(f"[Clipboard Error] {e}")


def schedule_clear(delay=CLIPBOARD_CLEAR_TIME):
    global _clear_timer

    def worker():
        time.sleep(delay)
        clear_clipboard()

    with _timer_lock:

        # Cancel previous timer
        if _clear_timer and _clear_timer.is_alive():
            print("[Clipboard] Previous timer cancelled")

        # Start new timer
        _clear_timer = threading.Thread(
            target=worker,
            daemon=True
        )
        _clear_timer.start()

        print(
            f"[Clipboard] Auto-clear in {delay}s "
            f"(reset)"
        )


class ClipboardManager:

    def copy(self, text):

        try:
            pyperclip.copy(text)

            print("[Clipboard] Copied")

            if AUTO_CLEAR_ENABLED:
                schedule_clear()
            else:
                print(
                    "[Clipboard] Auto-clear disabled"
                )

        except Exception as e:
            print(f"[Clipboard Error] {e}")