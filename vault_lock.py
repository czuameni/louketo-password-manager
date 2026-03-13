import threading
import time

from config import load_settings


settings = load_settings()

AUTO_LOCK_ENABLED = settings.get(
    "vault_auto_lock_enabled",
    True
)

AUTO_LOCK_TIME = settings.get(
    "vault_auto_lock_time",
    300
)


_last_activity = time.time()
_lock_triggered = False
_timer_thread = None
_lock = threading.Lock()


def _monitor_inactivity():

    global _lock_triggered

    while True:

        time.sleep(1)

        if not AUTO_LOCK_ENABLED:
            continue

        elapsed = time.time() - _last_activity

        if elapsed >= AUTO_LOCK_TIME:
            _lock_triggered = True
            print(
                "\n[Vault] Auto-locked "
                "due to inactivity\n"
            )
            break


def start_auto_lock_timer():

    global _timer_thread

    if not AUTO_LOCK_ENABLED:
        return

    _timer_thread = threading.Thread(
        target=_monitor_inactivity,
        daemon=True
    )
    _timer_thread.start()

    print(
        f"[Vault] Inactivity auto-lock "
        f"in {AUTO_LOCK_TIME}s"
    )


def register_activity():

    global _last_activity

    with _lock:
        _last_activity = time.time()


def is_vault_locked():

    return _lock_triggered


def reset_lock_flag():

    global _lock_triggered
    _lock_triggered = False