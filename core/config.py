import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Temporary folder for processing
HOME = os.path.expanduser("~")
TEMP_FOLDER = os.path.join(HOME, "musica", "nightcore_temp")

# Ensure temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Cleanup Settings (in seconds)
CLEANUP_INTERVAL = 60    # Check every minute
FILE_EXPIRY_TIME = 120   # Delete after 2 minutes

# App Settings
APP_TITLE = "Musica - Sarcastic Nightcore Generator"
VERSION = "0.1.0-alpha"

# Sarcastic Messages
SARCASM_SUCCESS = [
    "Fine, here's your nightcore. Don't play it too loud, my ears are bleeding.",
    "Done. It's high pitched. Are you happy now?",
    "Your audio has been processed. Try not to break anything else.",
]

SARCASM_ERROR = [
    "Your URL is as broken as my dreams.",
    "Something went wrong. It's definitely your fault, not mine.",
    "FFmpeg threw a tantrum. Maybe give it a better input next time?",
]

SARCASM_BETA_WARNING = "⚠️ VOCAL FREE is in beta. It might mess up your audio, or it might just give up. Use at your own risk."
