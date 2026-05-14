import logging
from pathlib import Path

# Create logs folder
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger("Irtiqa")
logger.setLevel(logging.INFO)

# Format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# File handler
file_handler = logging.FileHandler("logs/irtiqa.log")
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)