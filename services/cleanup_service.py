import time
import threading
from pathlib import Path
from core.config import TEMP_FOLDER, CLEANUP_INTERVAL, FILE_EXPIRY_TIME

def cleanup_old_files():
    """Background task to remove files older than FILE_EXPIRY_TIME."""
    while True:
        time.sleep(CLEANUP_INTERVAL)
        try:
            for item in Path(TEMP_FOLDER).glob("*"):
                if item.is_file():
                    if time.time() - item.stat().st_mtime > FILE_EXPIRY_TIME:
                        item.unlink()
                        print(f"[Cleanup] Deleted: {item.name}")
        except Exception as e:
            print(f"[Cleanup Error] {e}")

def start_cleanup_service():
    """Starts the cleanup service in a daemon thread."""
    thread = threading.Thread(target=cleanup_old_files, daemon=True)
    thread.start()
    return thread
