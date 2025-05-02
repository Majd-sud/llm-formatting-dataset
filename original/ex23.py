"""
This module contains examples of overly complex nested conditionals that should be flagged by SonarQube.
Deeply nested conditionals make code hard to understand, test, and maintain.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple, Union


# ISSUE: Deeply nested conditionals for user permissions

def check_user_permission_nested(user: Dict[str, Any], resource: Dict[str, Any], action: str) -> bool:
    """
    Check if a user has permission to perform an action on a resource.
    Contains deeply nested conditionals that make the logic hard to follow.
    """
    if user is not None:
        if "role" in user:
            if user["role"] == "admin":
                # Admins can do anything
                return True
            elif user["role"] == "manager":
                if resource is not None:
                    if "type" in resource:
                        if resource["type"] == "document":
                            if action in ["read", "write", "update"]:
                                if "department" in user and "department" in resource:
                                    if user["department"] == resource["department"]:
                                        # Managers can read, write, and update documents in their department
                                        return True
                                    else:
                                        if action == "read":
                                            if "visibility" in resource:
                                                if resource["visibility"] == "public":
                                                    # Managers can read public documents from other departments
                                                    return True
                                                else:
                                                    return False
                                            else:
                                                return False
                                        else:
                                            return False
                                else:
                                    return False
                            elif action == "delete":
                                if "created_by" in resource:
                                    if resource["created_by"] == user["id"]:
                                        # Managers can delete documents they created
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        elif resource["type"] == "report":
                            if action in ["read", "generate"]:
                                # Managers can read and generate reports
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            elif user["role"] == "employee":
                if resource is not None:
                    if "type" in resource:
                        if resource["type"] == "document":
                            if action == "read":
                                if "visibility" in resource:
                                    if resource["visibility"] == "public":
                                        # Employees can read public documents
                                        return True
                                    elif resource["visibility"] == "internal":
                                        if "department" in user and "department" in resource:
                                            if user["department"] == resource["department"]:
                                                # Employees can read internal documents in their department
                                                return True
                                            else:
                                                return False
                                        else:
                                            return False
                                    else:
                                        return False
                                else:
                                    return False
                            elif action in ["write", "update"]:
                                if "created_by" in resource:
                                    if resource["created_by"] == user["id"]:
                                        # Employees can write and update documents they created
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        elif resource["type"] == "report":
                            if action == "read":
                                if "department" in user and "department" in resource:
                                    if user["department"] == resource["department"]:
                                        # Employees can read reports in their department
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# ISSUE: Nested conditionals for order processing

def process_order_nested(order: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process an order with various conditions and rules.
    Contains deeply nested conditionals that make the logic hard to follow.
    """
    result = {
        "order_id": order.get("id"),
        "status": "pending",
        "messages": []
    }
    
    if "items" in order and order["items"]:
        total = 0
        for item in order["items"]:
            if "price" in item and "quantity" in item:
                item_total = item["price"] * item["quantity"]
                total += item_total
            else:
                result["messages"].append("Invalid item data")
                result["status"] = "error"
                return result
        
        result["total"] = total
        
        if "customer" in order:
            customer = order["customer"]
            if "type" in customer:
                if customer["type"] == "premium":
                    if total > 100:
                        # Premium customers get 10% discount on orders over $100
                        discount = total * 0.1
                        result["discount"] = discount
                        result["total_after_discount"] = total - discount
                    else:
                        result["total_after_discount"] = total
                elif customer["type"] == "regular":
                    if "loyalty_years" in customer:
                        if customer["loyalty_years"] > 2:
                            if total > 200:
                                # Loyal regular customers get 5% discount on orders over $200
                                discount = total * 0.05
                                result["discount"] = discount
                                result["total_after_discount"] = total - discount
                            else:
                                result["total_after_discount"] = total
                        else:
                            result["total_after_discount"] = total
                    else:
                        result["total_after_discount"] = total
                else:
                    result["total_after_discount"] = total
            else:
                result["total_after_discount"] = total
        else:
            result["messages"].append("Customer information missing")
            result["status"] = "error"
            return result
        
        if "shipping" in order:
            shipping = order["shipping"]
            if "method" in shipping:
                if shipping["method"] == "express":
                    if "address" in shipping:
                        address = shipping["address"]
                        if "country" in address:
                            if address["country"] == "US":
                                shipping_cost = 15
                            elif address["country"] in ["CA", "MX"]:
                                shipping_cost = 25
                            else:
                                shipping_cost = 50
                        else:
                            result["messages"].append("Shipping country missing")
                            result["status"] = "error"
                            return result
                    else:
                        result["messages"].append("Shipping address missing")
                        result["status"] = "error"
                        return result
                elif shipping["method"] == "standard":
                    if "address" in shipping:
                        address = shipping["address"]
                        if "country" in address:
                            if address["country"] == "US":
                                shipping_cost = 5
                            elif address["country"] in ["CA", "MX"]:
                                shipping_cost = 10
                            else:
                                shipping_cost = 20
                        else:
                            result["messages"].append("Shipping country missing")
                            result["status"] = "error"
                            return result
                    else:
                        result["messages"].append("Shipping address missing")
                        result["status"] = "error"
                        return result
                else:
                    result["messages"].append("Invalid shipping method")
                    result["status"] = "error"
                    return result
            else:
                result["messages"].append("Shipping method missing")
                result["status"] = "error"
                return result
            
            result["shipping_cost"] = shipping_cost
            result["final_total"] = result["total_after_discount"] + shipping_cost
            
            if "payment" in order:
                payment = order["payment"]
                if "method" in payment:
                    if payment["method"] == "credit_card":
                        if "card_info" in payment:
                            card_info = payment["card_info"]
                            if "number" in card_info and "expiry" in card_info and "cvv" in card_info:
                                # Process credit card payment
                                result["payment_status"] = "processed"
                                result["status"] = "completed"
                            else:
                                result["messages"].append("Incomplete credit card information")
                                result["status"] = "payment_required"
                        else:
                            result["messages"].append("Credit card information missing")
                            result["status"] = "payment_required"
                    elif payment["method"] == "paypal":
                        if "email" in payment:
                            # Process PayPal payment
                            result["payment_status"] = "processed"
                            result["status"] = "completed"
                        else:
                            result["messages"].append("PayPal email missing")
                            result["status"] = "payment_required"
                    else:
                        result["messages"].append("Unsupported payment method")
                        result["status"] = "payment_required"
                else:
                    result["messages"].append("Payment method missing")
                    result["status"] = "payment_required"
            else:
                result["messages"].append("Payment information missing")
                result["status"] = "payment_required"
        else:
            result["messages"].append("Shipping information missing")
            result["status"] = "error"
    else:
        result["messages"].append("No items in order")
        result["status"] = "error"
    
    return result


# ISSUE: Nested conditionals for data validation

def validate_user_data_nested(data: Dict[str, Any]) -> List[str]:
    """
    Validate user data with various rules.
    Contains deeply nested conditionals that make the logic hard to follow.
    """
    errors = []
    
    if "personal_info" in data:
        personal_info = data["personal_info"]
        if "name" in personal_info:
            name = personal_info["name"]
            if "first" in name:
                if not name["first"]:
                    errors.append("First name is required")
                elif len(name["first"]) < 2:
                    errors.append("First name must be at least 2 characters")
                elif len(name["first"]) > 50:
                    errors.append("First name cannot exceed 50 characters")
            else:
                errors.append("First name is required")
            
            if "last" in name:
                if not name["last"]:
                    errors.append("Last name is required")
                elif len(name["last"]) < 2:
                    errors.append("Last name must be at least 2 characters")
                elif len(name["last"]) > 50:
                    errors.append("Last name cannot exceed 50 characters")
            else:
                errors.append("Last name is required")
        else:
            errors.append("Name information is required")
        
        if "contact" in personal_info:
            contact = personal_info["contact"]
            if "email" in contact:
                email = contact["email"]
                if not email:
                    errors.append("Email is required")
                elif "@" not in email:
                    errors.append("Email must contain @")
                elif "." not in email:
                    errors.append("Email must contain a domain")
                elif len(email.split("@")[0]) < 1:
                    errors.append("Email username part cannot be empty")
                elif len(email.split("@")[1]) < 3:
                    errors.append("Email domain part is too short")
            else:
                errors.append("Email is required")
            
            if "phone" in contact:
                phone = contact["phone"]
                if phone:
                    if not all(c.isdigit() or c in "+-() " for c in phone):
                        errors.append("Phone number can only contain digits and +-() characters")
                    elif len(''.join(c for c in phone if c.isdigit())) < 10:
                        errors.append("Phone number must have at least 10 digits")
            # Phone is optional, so no error if missing
        else:
            errors.append("Contact information is required")
        
        if "address" in personal_info:
            address = personal_info["address"]
            if "street" in address:
                if not address["street"]:
                    errors.append("Street address is required")
            else:
                errors.append("Street address is required")
            
            if "city" in address:
                if not address["city"]:
                    errors.append("City is required")
            else:
                errors.append("City is required")
            
            if "state" in address:
                if not address["state"]:
                    errors.append("State is required")
                elif len(address["state"]) != 2:
                    errors.append("State must be a 2-letter code")
            else:
                errors.append("State is required")
            
            if "zip" in address:
                zip_code = address["zip"]
                if not zip_code:
                    errors.append("ZIP code is required")
                elif not zip_code.isdigit():
                    errors.append("ZIP code must contain only digits")
                elif len(zip_code) != 5:
                    errors.append("ZIP code must be 5 digits")
            else:
                errors.append("ZIP code is required")
            
            if "country" in address:
                if not address["country"]:
                    errors.append("Country is required")
            else:
                errors.append("Country is required")
        else:
            errors.append("Address information is required")
    else:
        errors.append("Personal information is required")
    
    if "account_info" in data:
        account_info = data["account_info"]
        if "username" in account_info:
            username = account_info["username"]
            if not username:
                errors.append("Username is required")
            elif len(username) < 3:
                errors.append("Username must be at least 3 characters")
            elif len(username) > 20:
                errors.append("Username cannot exceed 20 characters")
            elif not username.isalnum():
                errors.append("Username can only contain letters and numbers")
        else:
            errors.append("Username is required")
        
        if "password" in account_info:
            password = account_info["password"]
            if not password:
                errors.append("Password is required")
            elif len(password) < 8:
                errors.append("Password must be at least 8 characters")
            else:
                has_upper = False
                has_lower = False
                has_digit = False
                has_special = False
                
                for char in password:
                    if char.isupper():
                        has_upper = True
                    elif char.islower():
                        has_lower = True
                    elif char.isdigit():
                        has_digit = True
                    elif char in "!@#$%^&*()_+-=[]{}|;:,.<>?/":
                        has_special = True
                
                if not has_upper:
                    errors.append("Password must contain at least one uppercase letter")
                if not has_lower:
                    errors.append("Password must contain at least one lowercase letter")
                if not has_digit:
                    errors.append("Password must contain at least one digit")
                if not has_special:
                    errors.append("Password must contain at least one special character")
        else:
            errors.append("Password is required")
        
        if "confirm_password" in account_info:
            if account_info["confirm_password"] != account_info.get("password", ""):
                errors.append("Passwords do not match")
        else:
            errors.append("Password confirmation is required")
    else:
        errors.append("Account information is required")
    
    return errors


# BETTER ALTERNATIVE: Refactored code with early returns and guard clauses

class Role(Enum):
    """User roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class ResourceType(Enum):
    """Resource types."""
    DOCUMENT = "document"
    REPORT = "report"


class Action(Enum):
    """Possible actions on resources."""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    GENERATE = "generate"


class Visibility(Enum):
    """Document visibility levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"


def check_user_permission_better(user: Dict[str, Any], resource: Dict[str, Any], action: str) -> bool:
    """
    Check if a user has permission to perform an action on a resource.
    Refactored with early returns and guard clauses for better readability.
    """
    # Guard clauses for required fields
    if not user or "role" not in user:
        return False
    
    if not resource or "type" not in resource:
        return False
    
    role = user["role"]
    resource_type = resource["type"]
    
    # Admin can do anything
    if role == Role.ADMIN.value:
        return True
    
    # Manager permissions
    if role == Role.MANAGER.value:
        return _check_manager_permissions(user, resource, action, resource_type)
    
    # Employee permissions
    if role == Role.EMPLOYEE.value:
        return _check_employee_permissions(user, resource, action, resource_type)
    
    # Unknown role
    return False


def _check_manager_permissions(user: Dict[str, Any], resource: Dict[str, Any], action: str, resource_type: str) -> bool:
    """Check permissions for a manager."""
    # Document permissions
    if resource_type == ResourceType.DOCUMENT.value:
        # Read, write, update permissions
        if action in [Action.READ.value, Action.WRITE.value, Action.UPDATE.value]:
            # Same department
            if _is_same_department(user, resource):
                return True
            
            # Different department but public document
            if action == Action.READ.value and resource.get("visibility") == Visibility.PUBLIC.value:
                return True
            
            return False
        
        # Delete permission
        if action == Action.DELETE.value:
            return resource.get("created_by") == user.get("id")
        
        return False
    
    # Report permissions
    if resource_type == ResourceType.REPORT.value:
        return action in [Action.READ.value, Action.GENERATE.value]
    
    return False


def _check_employee_permissions(user: Dict[str, Any], resource: Dict[str, Any], action: str, resource_type: str) -> bool:
    """Check permissions for an employee."""
    # Document permissions
    if resource_type == ResourceType.DOCUMENT.value:
        # Read permission
        if action == Action.READ.value:
            visibility = resource.get("visibility")
            
            # Public document
            if visibility == Visibility.PUBLIC.value:
                return True
            
            # Internal document in same department
            if visibility == Visibility.INTERNAL.value and _is_same_department(user, resource):
                return True
            
            return False
        
        # Write and update permissions
        if action in [Action.WRITE.value, Action.UPDATE.value]:
            return resource.get("created_by") == user.get("id")
        
        return False
    
    # Report permissions
    if resource_type == ResourceType.REPORT.value:
        return action == Action.READ.value and _is_same_department(user, resource)
    
    return False


def _is_same_department(user: Dict[str, Any], resource: Dict[str, Any]) -> bool:
    """Check if user and resource are in the same department."""
    return "department" in user and "department" in resource and user["department"] == resource["department"]


# BETTER ALTERNATIVE: Refactored order processing with smaller functions

def process_order_better(order: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process an order with various conditions and rules.
    Refactored into smaller functions for better readability.
    """
    result = {
        "order_id": order.get("id"),
        "status": "pending",
        "messages": []
    }
    
    # Validate order has items
    if not order.get("items"):
        result["messages"].append("No items in order")
        result["status"] = "error"
        return result
    
    # Calculate order total
    try:
        total = _calculate_order_total(order["items"])
        result["total"] = total
    except ValueError as e:
        result["messages"].append(str(e))
        result["status"] = "error"
        return result
    
    # Process customer information
    if "customer" not in order:
        result["messages"].append("Customer information missing")
        result["status"] = "error"
        return result
    
    # Apply discounts
    discount_info = _apply_customer_discounts(order["customer"], total)
    result.update(discount_info)
    
    # Process shipping
    if "shipping" not in order:
        result["messages"].append("Shipping information missing")
        result["status"] = "error"
        return result
    
    try:
        shipping_info = _calculate_shipping_cost(order["shipping"])
        result.update(shipping_info)
    except ValueError as e:
        result["messages"].append(str(e))
        result["status"] = "error"
        return result
    
    # Calculate final total
    result["final_total"] = result["total_after_discount"] + result["shipping_cost"]
    
    # Process payment
    if "payment" not in order:
        result["messages"].append("Payment information missing")
        result["status"] = "payment_required"
        return result
    
    try:
        payment_info = _process_payment(order["payment"])
        result.update(payment_info)
        result["status"] = "completed"
    except ValueError as e:
        result["messages"].append(str(e))
        result["status"] = "payment_required"
    
    return result


def _calculate_order_total(items: List[Dict[str, Any]]) -> float:
    """Calculate the total cost of items in an order."""
    total = 0
    for item in items:
        if "price" not in item or "quantity" not in item:
            raise ValueError("Invalid item data")
        item_total = item["price"] * item["quantity"]
        total += item_total
    return total


def _apply_customer_discounts(customer: Dict[str, Any], total: float) -> Dict[str, float]:
    """Apply discounts based on customer type and order total."""
    result = {"total_after_discount": total}
    
    customer_type = customer.get("type")
    
    # Premium customer discount
    if customer_type == "premium" and total > 100:
        discount = total * 0.1
        result["discount"] = discount
        result["total_after_discount"] = total - discount
    
    # Loyal regular customer discount
    elif customer_type == "regular" and customer.get("loyalty_years", 0) > 2 and total > 200:
        discount = total * 0.05
        result["discount"] = discount
        result["total_after_discount"] = total - discount
    
    return result


def _calculate_shipping_cost(shipping: Dict[str, Any]) -> Dict[str, float]:
    """Calculate shipping cost based on method and destination."""
    if "method" not in shipping:
        raise ValueError("Shipping method missing")
    
    if "address" not in shipping:
        raise ValueError("Shipping address missing")
    
    address = shipping["address"]
    if "country" not in address:
        raise ValueError("Shipping country missing")
    
    method = shipping["method"]
    country = address["country"]
    
    # Express shipping rates
    if method == "express":
        if country == "US":
            shipping_cost = 15
        elif country in ["CA", "MX"]:
            shipping_cost = 25
        else:
            shipping_cost = 50
    
    # Standard shipping rates
    elif method == "standard":
        if country == "US":
            shipping_cost = 5
        elif country in ["CA", "MX"]:
            shipping_cost = 10
        else:
            shipping_cost = 20
    
    else:
        raise ValueError("Invalid shipping method")
    
    return {"shipping_cost": shipping_cost}


def _process_payment(payment: Dict[str, Any]) -> Dict[str, str]:
    """Process payment based on payment method."""
    if "method" not in payment:
        raise ValueError("Payment method missing")
    
    method = payment["method"]
    
    # Credit card payment
    if method == "credit_card":
        if "card_info" not in payment:
            raise ValueError("Credit card information missing")
        
        card_info = payment["card_info"]
        required_fields = ["number", "expiry", "cvv"]
        
        for field in required_fields:
            if field not in card_info:
                raise ValueError(f"Missing {field} in credit card information")
        
        # Process credit card payment logic would go here
    
    # PayPal payment
    elif method == "paypal":
        if "email" not in payment:
            raise ValueError("PayPal email missing")
        
        # Process PayPal payment logic would go here
    
    else:
        raise ValueError("Unsupported payment method")
    
    return {"payment_status": "processed"}


# BETTER ALTERNATIVE: Refactored data validation with smaller functions

def validate_user_data_better(data: Dict[str, Any]) -> List[str]:
    """
    Validate user data with various rules.
    Refactored into smaller functions for better readability.
    """
    errors = []
    
    # Validate personal information
    if "personal_info" not in data:
        errors.append("Personal information is required")
        return errors
    
    personal_info = data["personal_info"]
    errors.extend(_validate_name(personal_info))
    errors.extend(_validate_contact(personal_info))
    errors.extend(_validate_address(personal_info))
    
    # Validate account information
    if "account_info" not in data:
        errors.append("Account information is required")
        return errors
    
    account_info = data["account_info"]
    errors.extend(_validate_username(account_info))
    errors.extend(_validate_password(account_info))
    
    return errors


def _validate_name(personal_info: Dict[str, Any]) -> List[str]:
    """Validate name information."""
    errors = []
    
    if "name" not in personal_info:
        errors.append("Name information is required")
        return errors
    
    name = personal_info["name"]
    
    # Validate first name
    if "first" not in name:
        errors.append("First name is required")
    elif not name["first"]:
        errors.append("First name is required")
    elif len(name["first"]) < 2:
        errors.append("First name must be at least 2 characters")
    elif len(name["first"]) > 50:
        errors.append("First name cannot exceed 50 characters")
    
    # Validate last name
    if "last" not in name:
        errors.append("Last name is required")
    elif not name["last"]:
        errors.append("Last name is required")
    elif len(name["last"]) < 2:
        errors.append("Last name must be at least 2 characters")
    elif len(name["last"]) > 50:
        errors.append("Last name cannot exceed 50 characters")
    
    return errors


def _validate_contact(personal_info: Dict[str, Any]) -> List[str]:
    """Validate contact information."""
    errors = []
    
    if "contact" not in personal_info:
        errors.append("Contact information is required")
        return errors
    
    contact = personal_info["contact"]
    
    # Validate email
    if "email" not in contact:
        errors.append("Email is required")
    else:
        email = contact["email"]
        if not email:
            errors.append("Email is required")
        elif "@" not in email:
            errors.append("Email must contain @")
        elif "." not in email:
            errors.append("Email must contain a domain")
        elif len(email.split("@")[0]) < 1:
            errors.append("Email username part cannot be empty")
        elif len(email.split("@")[1]) < 3:
            errors.append("Email domain part is too short")
    
    # Validate phone (optional)
    if "phone" in contact and contact["phone"]:
        phone = contact["phone"]
        if not all(c.isdigit() or c in "+-() " for c in phone):
            errors.append("Phone number can only contain digits and +-() characters")
        elif len(''.join(c for c in phone if c.isdigit())) < 10:
            errors.append("Phone number must have at least 10 digits")
    
    return errors


def _validate_address(personal_info: Dict[str, Any]) -> List[str]:
    """Validate address information."""
    errors = []
    
    if "address" not in personal_info:
        errors.append("Address information is required")
        return errors
    
    address = personal_info["address"]
    
    # Validate street
    if "street" not in address:
        errors.append("Street address is required")
    elif not address["street"]:
        errors.append("Street address is required")
    
    # Validate city
    if "city" not in address:
        errors.append("City is required")
    elif not address["city"]:
        errors.append("City is required")
    
    # Validate state
    if "state" not in address:
        errors.append("State is required")
    elif not address["state"]:
        errors.append("State is required")
    elif len(address["state"]) != 2:
        errors.append("State must be a 2-letter code")
    
    # Validate ZIP code
    if "zip" not in address:
        errors.append("ZIP code is required")
    else:
        zip_code = address["zip"]
        if not zip_code:
            errors.append("ZIP code is required")
        elif not zip_code.isdigit():
            errors.append("ZIP code must contain only digits")
        elif len(zip_code) != 5:
            errors.append("ZIP code must be 5 digits")
    
    # Validate country
    if "country" not in address:
        errors.append("Country is required")
    elif not address["country"]:
        errors.append("Country is required")
    
    return errors


def _validate_username(account_info: Dict[str, Any]) -> List[str]:
    """Validate username."""
    errors = []
    
    if "username" not in account_info:
        errors.append("Username is required")
        return errors
    
    username = account_info["username"]
    if not username:
        errors.append("Username is required")
    elif len(username) < 3:
        errors.append("Username must be at least 3 characters")
    elif len(username) > 20:
        errors.append("Username cannot exceed 20 characters")
    elif not username.isalnum():
        errors.append("Username can only contain letters and numbers")
    
    return errors


def _validate_password(account_info: Dict[str, Any]) -> List[str]:
    """Validate password and confirmation."""
    errors = []
    
    # Check if password exists
    if "password" not in account_info:
        errors.append("Password is required")
        return errors
    
    password = account_info["password"]
    if not password:
        errors.append("Password is required")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters")
    else:
        # Check password complexity
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password)
        
        if not has_upper:
            errors.append("Password must contain at least one uppercase letter")
        if not has_lower:
            errors.append("Password must contain at least one lowercase letter")
        if not has_digit:
            errors.append("Password must contain at least one digit")
        if not has_special:
            errors.append("Password must contain at least one special character")
    
    # Check password confirmation
    if "confirm_password" not in account_info:
        errors.append("Password confirmation is required")
    elif account_info["confirm_password"] != account_info.get("password", ""):
        errors.append("Passwords do not match")
    
    return errors