"""
This module contains examples of dead code that should be flagged by SonarQube.
These include unused imports, unused variables, unreachable code, and commented-out code.
"""

# Unused imports
import json
import csv
import random
import datetime
import re
import os
import sys
import math
import time
import collections
import functools


def process_user_data(user_id, name, email, phone, address, age, occupation):
    """Process user data and return a summary."""
    # Only using user_id, name, and email
    print(f"Processing data for user {user_id}: {name} ({email})")

    # phone, address, age, and occupation are never used

    return {
        "id": user_id,
        "processed": True,
        "timestamp": time.time()
    }


def calculate_statistics(data):
    """Calculate various statistics for the given data."""
    count = len(data)
    total = sum(data)
    average = total / count

    # Unused variables
    minimum = min(data)
    maximum = max(data)
    median = sorted(data)[count // 2]

    return {
        "count": count,
        "average": average
    }


def validate_password(password):
    """Validate a password and return if it's valid."""
    if len(password) < 8:
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    return True

    # Unreachable code
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    has_special = any(c in special_chars for c in password)

    if not has_special:
        return False

    print("Password validation complete")
    return True


def process_status_code(status_code):
    """Process an HTTP status code."""
    if 200 <= status_code < 300:
        return "Success"
    elif 300 <= status_code < 400:
        return "Redirect"
    elif 400 <= status_code < 500:
        return "Client Error"
    elif status_code >= 500:
        return "Server Error"
    elif status_code < 0:  # Unreachable condition
        return "Invalid Code"

    return "Unknown"


def generate_report():
    """Generate a detailed report of system status."""
    print("Generating report...")

    report = {
        "system": "online",
        "users": 1234,
        "load": "45%",
        "memory": "67%",
        "storage": "23%"
    }

    print("Report generated successfully")
    return report


def process_data(data):
    """Process the given data."""
    result = []

    for item in data:
        processed = item * 2
        result.append(processed)

    # Old implementation - commented out instead of being removed
    # for i in range(len(data)):
    #     item = data[i]
    #     if item > 0:
    #         processed = item * 2
    #     else:
    #         processed = 0
    #     result.append(processed)

    return result


class Logger:
    """A logging utility class that is never used."""

    def __init__(self, log_file):
        self.log_file = log_file
        self.entries = []

    def log(self, message, level="INFO"):
        """Log a message with the specified level."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.entries.append(entry)

        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    def get_logs(self):
        """Return all log entries."""
        return self.entries


def cleanup_resources():
    """Clean up system resources."""
    print("Cleaning up resources...")
    print("Resources cleaned up successfully")


def main():
    """Main function."""
    # Defined but unused
    config = {
        "debug": True,
        "log_level": "INFO",
        "max_retries": 3,
        "timeout": 30
    }

    data = [1, 2, 3, 4, 5]
    result = process_data(data)
    print(f"Processed data: {result}")

    # Defined but unused
    error_codes = {
        "E001": "Invalid input",
        "E002": "Connection failed",
        "E003": "Timeout",
        "E004": "Authentication failed"
    }


if __name__ == "__main__":
    main()

    # Executed but result is unused
    status = validate_password("Password123")
