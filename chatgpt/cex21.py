"""
This module contains examples of naming issues that should be flagged by SonarQube.
These include inconsistent naming conventions, too short names, and names that don't
follow Python's PEP 8 style guide.
"""

import datetime
import math


# ISSUE: Inconsistent naming conventions (class and method)
class userAccount:
    def __init__(self, userId, userName, email_address):
        self.userId = userId
        self.userName = userName
        self.email_address = email_address
        self.CreationDate = datetime.datetime.now()

    def vErYInTEReSTINGFuNCtION(self, nothing):
        something = nothing[0]
        return something

    def getUserDetails(self):
        return {
            "id": self.userId,
            "name": self.userName,
            "email": self.email_address,
            "created": self.CreationDate
        }

    def update_user_info(self, new_user_name, newEmail):
        self.userName = new_user_name
        self.email_address = newEmail


# ISSUE: Too short, non-descriptive variable names
def calc_stats(l):
    n = len(l)
    if n == 0:
        return None

    s = sum(l)
    a = s / n

    ss = 0
    for x in l:
        ss += (x - a) ** 2

    v = ss / n
    sd = math.sqrt(v)

    return {
        "min": min(l),
        "max": max(l),
        "avg": a,
        "sd": sd
    }


# ISSUE: Mixing naming conventions
def FetchUserData(UserID):
    """Fetch user data from the database."""
    user_record = {"id": UserID}

    lastLoginTime = "2023-01-01"
    user_record["last_login"] = lastLoginTime

    AccountBalance = 100.0
    user_record["balance"] = AccountBalance

    return user_record


# ISSUE: Similar/confusing parameter names
def process_data(data_list, datalist, data):
    """Process different types of data."""
    result_list = []
    resultList = []

    for item in data_list:
        result_list.append(item * 2)

    for item in datalist:
        resultList.append(item + 10)

    data_processed = data * 3
    dataProcessed = data + 5

    return {
        "result_list": result_list,
        "resultList": resultList,
        "data_processed": data_processed,
        "dataProcessed": dataProcessed
    }


# ISSUE: Non-descriptive function name
def x(a, b):
    """Calculate something."""
    return a * b + a / b if b != 0 else float('inf')


# ISSUE: Constants not in UPPER_CASE
max_retry_count = 5
default_timeout = 30
api_base_url = "https://api.example.com"


# ISSUE: Single-letter function name
def f(x):
    return x * x


# ISSUE: Shadows built-ins
def list(items):
    """Custom list processing function."""
    return [item.upper() for item in items]


def str(obj):
    """Custom string conversion."""
    return f"Object: {obj}"


def min(a, b, c):
    """Find minimum of three numbers."""
    return a if a <= b and a <= c else b if b <= c else c


# BETTER ALTERNATIVE: Consistent naming
class UserAccount:
    def __init__(self, user_id, user_name, email_address):
        self.user_id = user_id
        self.user_name = user_name
        self.email_address = email_address
        self.creation_date = datetime.datetime.now()

    def get_user_details(self):
        return {
            "id": self.user_id,
            "name": self.user_name,
            "email": self.email_address,
            "created": self.creation_date
        }

    def update_user_info(self, new_user_name, new_email):
        self.user_name = new_user_name
        self.email_address = new_email


# BETTER ALTERNATIVE: Descriptive names
def calculate_statistics(values):
    count = len(values)
    if count == 0:
        return None

    total = sum(values)
    average = total / count

    sum_of_squares = 0
    for value in values:
        sum_of_squares += (value - average) ** 2

    variance = sum_of_squares / count
    std_dev = math.sqrt(variance)

    return {
        "min": min(values),
        "max": max(values),
        "avg": average,
        "std_dev": std_dev
    }


# BETTER ALTERNATIVE: UPPER_CASE constants
MAX_RETRY_COUNT = 5
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
