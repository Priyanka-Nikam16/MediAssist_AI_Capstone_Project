import logging
import os

# Folder containing logger.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# backend/logs
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "mediassist.log")

print("LOG FILE =", LOG_FILE)

logger = logging.getLogger("mediassist")

if logger.hasHandlers():
    logger.handlers.clear()

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.propagate = False