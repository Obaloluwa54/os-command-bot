import os

# ------------------------
# TELEGRAM BOT SETTINGS
# ------------------------
TELEGRAM_TOKEN = os.getenv("8454819156:AAEX1Qjbk3fwVbHirKSHnsMNkyCbECdaxMM")  # Set in Render environment variables

# ------------------------
# FILE PATHS
# ------------------------
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
REPOS_DIR = os.path.join(DATA_DIR, "repos")

# ------------------------
# SANDBOX SETTINGS
# ------------------------
SANDBOX_PATH = os.path.join(DATA_DIR, "sandbox")
ALLOWED_TOOLS = ["python", "bash", "node"]  # Add any runtime you allow

# ------------------------
# OTHER SETTINGS
# ------------------------
MAX_LOGS = 100
