"""
This module contains examples of hardcoded values that should be flagged by SonarQube.
These include magic numbers, hardcoded IPs/URLs, and other constants that should be defined.
"""

import time
import requests


def calculate_price(base_price, quantity):
    """Calculate the final price with discounts based on quantity."""
    if quantity > 100:
        return base_price * quantity * 0.85  # 15% discount
    elif quantity > 50:
        return base_price * quantity * 0.90  # 10% discount
    elif quantity > 10:
        return base_price * quantity * 0.95  # 5% discount
    else:
        return base_price * quantity


def fetch_data_from_api(endpoint):
    """Fetch data from the specified API endpoint."""
    try:
        response = requests.get(endpoint, timeout=30)  # Hardcoded 30s timeout

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Status code {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None


def retry_operation(operation, max_attempts=3):
    """Retry an operation with exponential backoff."""
    attempt = 1

    while attempt <= max_attempts:
        try:
            result = operation()
            return result
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")

            if attempt < max_attempts:
                wait_time = 2 ** attempt * 100 / 1000  # 2^attempt * 100ms
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)

            attempt += 1

    print(f"Operation failed after {max_attempts} attempts")
    return None


def connect_to_services():
    """Connect to various services using hardcoded addresses."""
    database_ip = "192.168.1.100"
    cache_server_ip = "192.168.1.101"
    message_queue_ip = "192.168.1.102"

    api_url = "https://api.example.com/v1"
    auth_url = "https://auth.example.com/oauth/token"
    webhook_url = "https://hooks.example.com/incoming"

    database_port = 5432
    cache_port = 6379
    queue_port = 5672

    services = {
        "database": f"{database_ip}:{database_port}",
        "cache": f"{cache_server_ip}:{cache_port}",
        "queue": f"{message_queue_ip}:{queue_port}",
        "api": api_url,
        "auth": auth_url,
        "webhook": webhook_url
    }

    return services


def read_configuration():
    """Read configuration from hardcoded file paths."""
    config_path = "/etc/myapp/config.json"
    secrets_path = "/etc/myapp/secrets.json"
    logs_path = "/var/log/myapp/app.log"

    print(f"Reading configuration from {config_path}")
    print(f"Reading secrets from {secrets_path}")
    print(f"Logging to {logs_path}")

    config = {
        "debug": True,
        "log_level": "INFO",
        "max_connections": 100
    }

    return config


def authenticate_user(username):
    """Authenticate a user against hardcoded credentials."""
    admin_username = "admin"
    admin_password = "admin123"  # Insecure hardcoded password
    api_key = "1a2b3c4d5e6f7g8h9i0j"  # Insecure hardcoded API key

    if username == admin_username:
        print("Admin user detected, using special authentication")
        return {
            "authenticated": True,
            "role": "admin",
            "api_key": api_key
        }
    else:
        return {
            "authenticated": True,
            "role": "user"
        }


def calculate_shipping_cost(weight, destination):
    """Calculate shipping cost based on weight and destination."""
    if weight <= 1:
        base_cost = 5.99
    elif weight <= 5:
        base_cost = 10.99
    elif weight <= 10:
        base_cost = 15.99
    else:
        base_cost = 20.99

    if destination == "domestic":
        return base_cost
    elif destination == "canada":
        return base_cost * 1.5
    elif destination == "europe":
        return base_cost * 2.5
    elif destination == "asia":
        return base_cost * 3.0
    else:
        return base_cost * 3.5


def process_user_data(user_data):
    """Process user data from a specific format array."""
    user_id = user_data[0]
    name = user_data[1]
    email = user_data[2]
    role = user_data[3]
    department = user_data[4]

    print(f"Processing user: {name} ({email})")
    print(f"User ID: {user_id}, Role: {role}, Department: {department}")

    return {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "department": department
    }


# Constants for better maintainability
LARGE_ORDER_THRESHOLD = 100
LARGE_ORDER_DISCOUNT = 0.15
MEDIUM_ORDER_THRESHOLD = 50
MEDIUM_ORDER_DISCOUNT = 0.10
SMALL_ORDER_THRESHOLD = 10
SMALL_ORDER_DISCOUNT = 0.05


def calculate_price_better(base_price, quantity):
    """Calculate the final price with discounts using constants."""
    if quantity > LARGE_ORDER_THRESHOLD:
        return base_price * quantity * (1 - LARGE_ORDER_DISCOUNT)
    elif quantity > MEDIUM_ORDER_THRESHOLD:
        return base_price * quantity * (1 - MEDIUM_ORDER_DISCOUNT)
    elif quantity > SMALL_ORDER_THRESHOLD:
        return base_price * quantity * (1 - SMALL_ORDER_DISCOUNT)
    else:
        return base_price * quantity


class ServiceConfig:
    """Configuration for service connections."""
    DATABASE_HOST = "192.168.1.100"
    DATABASE_PORT = 5432
    CACHE_HOST = "192.168.1.101"
    CACHE_PORT = 6379
    QUEUE_HOST = "192.168.1.102"
    QUEUE_PORT = 5672
    API_URL = "https://api.example.com/v1"
    AUTH_URL = "https://auth.example.com/oauth/token"
    WEBHOOK_URL = "https://hooks.example.com/incoming"
    REQUEST_TIMEOUT = 30


def connect_to_services_better():
    """Connect to various services using configuration constants."""
    services = {
        "database": f"{ServiceConfig.DATABASE_HOST}:{ServiceConfig.DATABASE_PORT}",
        "cache": f"{ServiceConfig.CACHE_HOST}:{ServiceConfig.CACHE_PORT}",
        "queue": f"{ServiceConfig.QUEUE_HOST}:{ServiceConfig.QUEUE_PORT}",
        "api": ServiceConfig.API_URL,
        "auth": ServiceConfig.AUTH_URL,
        "webhook": ServiceConfig.WEBHOOK_URL
    }

    return services
