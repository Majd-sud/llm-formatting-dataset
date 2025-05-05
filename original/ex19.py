"""
This module contains examples of dead code that should be flagged by SonarQube.
These include unused imports, unused variables, unreachable code, and commented-out code.
"""

# ISSUE: Unused imports
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


# ISSUE: Function with unused parameters
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


# ISSUE: Unused variables
def calculate_statistics(data):
    """Calculate various statistics for the given data."""
    count = len(data)  # Used
    total = sum(data)  # Used
    average = total / count  # Used
    
    # Unused variables
    minimum = min(data)
    maximum = max(data)
    median = sorted(data)[count // 2]
    
    # Only returning average
    return {
        "count": count,
        "average": average
    }


# ISSUE: Unreachable code after return statement
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
    
    # Unreachable code after return
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    has_special = any(c in special_chars for c in password)
    
    if not has_special:
        return False
    
    print("Password validation complete")
    return True


# ISSUE: Dead code in conditional branches that can never be executed
def process_status_code(status_code):
    """Process an HTTP status code."""
    if status_code >= 200 and status_code < 300:
        return "Success"
    elif status_code >= 300 and status_code < 400:
        return "Redirect"
    elif status_code >= 400 and status_code < 500:
        return "Client Error"
    elif status_code >= 500:
        return "Server Error"
    elif status_code < 0:  # This condition can never be true after the above checks
        return "Invalid Code"
    
    return "Unknown"


# ISSUE: Unused function
def generate_report():
    """Generate a detailed report of system status."""
    print("Generating report...")
    
    # Complex report generation logic
    report = {
        "system": "online",
        "users": 1234,
        "load": "45%",
        "memory": "67%",
        "storage": "23%"
    }
    
    print("Report generated successfully")
    return report


# ISSUE: Commented-out code
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


# ISSUE: Unused class
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


# ISSUE: Function that is defined but never called
def cleanup_resources():
    """Clean up system resources."""
    print("Cleaning up resources...")
    
    # Resource cleanup logic
    print("Resources cleaned up successfully")


# ISSUE: Variable defined but never used
def main():
    """Main function."""
    # This variable is defined but never used
    config = {
        "debug": True,
        "log_level": "INFO",
        "max_retries": 3,
        "timeout": 30
    }
    
    data = [1, 2, 3, 4, 5]
    result = process_data(data)
    print(f"Processed data: {result}")
    
    # This variable is defined but never used
    error_codes = {
        "E001": "Invalid input",
        "E002": "Connection failed",
        "E003": "Timeout",
        "E004": "Authentication failed"
    }


if __name__ == "__main__":
    main()
    
    # This code is executed but the result is never used
    status = validate_password("Password123")