"""
This module contains examples of naming issues that should be flagged by SonarQube.
These include inconsistent naming conventions, too short names, and names that don't
follow Python's PEP 8 style guide.
"""

import datetime
import math


# ISSUE: Inconsistent naming conventions (mixing camelCase and snake_case)
class userAccount:  # Class name should be UserAccount (PascalCase)
    def __init__(self, userId, userName, email_address):
        # Inconsistent parameter naming (mixing camelCase and snake_case)
        self.userId = userId  # Should be user_id (snake_case)
        self.userName = userName  # Should be user_name (snake_case)
        self.email_address = email_address  # This one is correct snake_case
        self.CreationDate = datetime.datetime.now()  # Should be creation_date (snake_case)

    # Function with SpongeBob case function name
    def vErYInTEReSTINGFuNCtION(self, nothing):
        something = nothing[0]
        return something

    # Method using camelCase instead of snake_case
    def getUserDetails(self):
        return {
            "id": self.userId,
            "name": self.userName,
            "email": self.email_address,
            "created": self.CreationDate
        }
    
    # Inconsistent method naming (this one uses snake_case)
    def update_user_info(self, new_user_name, newEmail):  # Inconsistent parameter naming
        self.userName = new_user_name
        self.email_address = newEmail


# ISSUE: Too short, non-descriptive variable names
def calc_stats(l):  # 'l' is too short and can be confused with '1'
    n = len(l)  # 'n' is not descriptive
    if n == 0:
        return None
    
    s = sum(l)  # 's' is not descriptive
    a = s / n  # 'a' is not descriptive (should be 'average')
    
    # Calculate standard deviation
    ss = 0  # 'ss' is not descriptive (should be 'sum_of_squares')
    for x in l:  # 'x' is somewhat acceptable for a loop variable
        ss += (x - a) ** 2
    
    v = ss / n  # 'v' is not descriptive (should be 'variance')
    sd = math.sqrt(v)  # 'sd' is somewhat acceptable but 'std_dev' would be better
    
    return {
        "min": min(l),
        "max": max(l),
        "avg": a,
        "sd": sd
    }


# ISSUE: Mixing naming conventions in functions and variables
def FetchUserData(UserID):  # Should be fetch_user_data (snake_case)
    """Fetch user data from the database."""
    # Mixing snake_case and camelCase
    user_record = {"id": UserID}  # Inconsistent: UserID vs user_record
    
    lastLoginTime = "2023-01-01"  # Should be last_login_time (snake_case)
    user_record["last_login"] = lastLoginTime
    
    AccountBalance = 100.0  # Should be account_balance (snake_case)
    user_record["balance"] = AccountBalance
    
    return user_record


# ISSUE: Confusing and similar names in the same scope
def process_data(data_list, datalist, data):
    """
    Process different types of data.
    The parameter names are too similar and confusing.
    """
    # These variable names are too similar and confusing
    result_list = []
    resultList = []
    
    for item in data_list:
        result_list.append(item * 2)
    
    for item in datalist:
        resultList.append(item + 10)
    
    # More confusion with similar names
    data_processed = data * 3
    dataProcessed = data + 5
    
    return {
        "result_list": result_list,
        "resultList": resultList,
        "data_processed": data_processed,
        "dataProcessed": dataProcessed
    }


# ISSUE: Non-descriptive function name
def x(a, b):  # Function name 'x' is not descriptive
    """Calculate something."""
    return a * b + a / b if b != 0 else float('inf')


# ISSUE: Constants not in UPPER_CASE
max_retry_count = 5  # Should be MAX_RETRY_COUNT
default_timeout = 30  # Should be DEFAULT_TIMEOUT
api_base_url = "https://api.example.com"  # Should be API_BASE_URL


# ISSUE: Using single character names for functions
def f(x):  # Non-descriptive function name
    return x * x


# ISSUE: Using names that shadow built-in functions
def list(items):  # Shadows the built-in 'list' function
    """Custom list processing function."""
    return [item.upper() for item in items]


def str(obj):  # Shadows the built-in 'str' function
    """Custom string conversion."""
    return f"Object: {obj}"


def min(a, b, c):  # Shadows the built-in 'min' function
    """Find minimum of three numbers."""
    return a if a <= b and a <= c else b if b <= c else c


# BETTER ALTERNATIVE: Consistent naming following PEP 8
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


# BETTER ALTERNATIVE: Descriptive variable names
def calculate_statistics(values):
    count = len(values)
    if count == 0:
        return None
    
    total = sum(values)
    average = total / count
    
    # Calculate standard deviation
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


# BETTER ALTERNATIVE: Constants in UPPER_CASE
MAX_RETRY_COUNT = 5
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"