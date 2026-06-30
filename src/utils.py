"""
utils.py
-----------------------------
Utility functions for the
LLM Evaluation Pipeline
"""

import json
import csv
import os
import logging
import time
from functools import wraps
from datetime import datetime


# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_logger(name="LLM Evaluation"):
    return logging.getLogger(name)


logger = get_logger()


# -----------------------------
# Timer Decorator
# -----------------------------

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        logger.info(
            f"{func.__name__} executed in {round(end-start,3)} seconds"
        )

        return result

    return wrapper


# -----------------------------
# Load JSON Dataset
# -----------------------------

def load_json(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Save JSON
# -----------------------------

def save_json(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Export CSV
# -----------------------------

def export_csv(data, filename):

    if len(data) == 0:
        return

    os.makedirs("reports", exist_ok=True)

    filepath = os.path.join("reports", filename)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=data[0].keys()
        )

        writer.writeheader()

        writer.writerows(data)

    logger.info(f"CSV exported to {filepath}")


# -----------------------------
# Create Folder
# -----------------------------

def ensure_dir(path):

    os.makedirs(path, exist_ok=True)


# -----------------------------
# Timestamp
# -----------------------------

def timestamp():

    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# -----------------------------
# Average
# -----------------------------

def average(values):

    if len(values) == 0:
        return 0

    return round(sum(values) / len(values), 3)


# -----------------------------
# Percentage
# -----------------------------

def percentage(part, total):

    if total == 0:
        return 0

    return round((part / total) * 100, 2)


# -----------------------------
# Normalize Text
# -----------------------------

def normalize(text):

    return text.lower().strip()


# -----------------------------
# Safe Divide
# -----------------------------

def safe_divide(a, b):

    if b == 0:
        return 0

    return a / b