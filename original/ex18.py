"""
This module contains examples of complex functions with high cyclomatic complexity.
SonarQube should flag these as code smells due to their complexity and maintainability issues.
"""

import random
import time


# ISSUE: Function with high cyclomatic complexity due to nested conditionals
def determine_user_access_level(user_id, role, department, years_of_service, 
                               security_clearance, is_contractor, special_permissions):
    """
    Determines a user's access level based on multiple factors.
    This function has high cyclomatic complexity and should be refactored.
    """
    access_level = 0
    
    if user_id < 1000:
        # Legacy users get base access
        access_level = 1
        
        if role == "manager":
            access_level += 2
            if years_of_service > 5:
                access_level += 1
                if security_clearance > 3:
                    access_level += 2
            elif special_permissions:
                access_level += 1
        elif role == "developer":
            access_level += 1
            if department == "security":
                access_level += 2
                if not is_contractor:
                    access_level += 1
            elif department == "infrastructure":
                access_level += 1
                if years_of_service > 3:
                    access_level += 1
    else:
        # New users
        if security_clearance > 2:
            access_level = 2
            if role == "manager":
                access_level += 1
                if department in ["security", "compliance"]:
                    access_level += 2
            elif role == "developer" and not is_contractor:
                if years_of_service > 2:
                    access_level += 1
                    if special_permissions:
                        access_level += 1
        else:
            access_level = 1
            if special_permissions and not is_contractor:
                access_level += 1
    
    return access_level


# ISSUE: Function with too many branches and conditions
def calculate_insurance_premium(age, gender, smoker, bmi, family_history, 
                               exercise_level, occupation_risk, coverage_level,
                               previous_claims, location, pre_existing_conditions):
    """
    Calculates insurance premium based on various risk factors.
    This function has too many branches and should be simplified.
    """
    base_premium = 500
    
    # Age factor
    if age < 25:
        age_factor = 1.5
    elif age < 40:
        age_factor = 1.0
    elif age < 60:
        age_factor = 1.2
    else:
        age_factor = 1.8
    
    # Health factors
    if smoker:
        health_factor = 2.0
    else:
        health_factor = 1.0
        
    if bmi < 18.5:
        health_factor *= 1.1
    elif bmi < 25:
        health_factor *= 0.9
    elif bmi < 30:
        health_factor *= 1.2
    else:
        health_factor *= 1.5
    
    if family_history:
        health_factor *= 1.3
    
    if pre_existing_conditions:
        if len(pre_existing_conditions) > 3:
            health_factor *= 2.0
        elif len(pre_existing_conditions) > 1:
            health_factor *= 1.5
        else:
            health_factor *= 1.2
    
    # Lifestyle factors
    if exercise_level == "high":
        lifestyle_factor = 0.8
    elif exercise_level == "medium":
        lifestyle_factor = 1.0
    else:
        lifestyle_factor = 1.2
    
    # Occupation risk
    if occupation_risk == "high":
        risk_factor = 1.5
    elif occupation_risk == "medium":
        risk_factor = 1.2
    else:
        risk_factor = 1.0
    
    # Previous claims
    if previous_claims > 3:
        claims_factor = 1.8
    elif previous_claims > 0:
        claims_factor = 1.2
    else:
        claims_factor = 0.9
    
    # Location factor
    if location in ["urban", "suburban"]:
        if location == "urban":
            location_factor = 1.2
        else:
            location_factor = 1.0
    else:
        location_factor = 0.9
    
    # Coverage level
    if coverage_level == "premium":
        coverage_factor = 1.5
    elif coverage_level == "standard":
        coverage_factor = 1.0
    else:
        coverage_factor = 0.7
    
    # Calculate final premium
    premium = base_premium * age_factor * health_factor * lifestyle_factor * risk_factor * claims_factor * location_factor * coverage_factor
    
    # Apply gender-based discount (could be flagged as discriminatory)
    if gender == "female":
        premium *= 0.9
    
    return round(premium, 2)


# ISSUE: Function with long method and too many responsibilities
def process_customer_order(customer_id, items, payment_info, shipping_address, 
                          coupon_code, gift_wrap, loyalty_points, notification_preferences):
    """
    Processes a customer order with too many responsibilities.
    This function should be broken down into smaller, focused functions.
    """
    # Validate customer
    print(f"Validating customer {customer_id}")
    time.sleep(0.1)  # Simulate database lookup
    
    # Check inventory
    inventory_status = {}
    for item in items:
        # Simulate inventory check
        time.sleep(0.05)
        in_stock = random.choice([True, True, True, False])
        inventory_status[item["id"]] = in_stock
        if not in_stock:
            print(f"Item {item['id']} is out of stock")
            return {"status": "failed", "reason": "item_out_of_stock", "item_id": item["id"]}
    
    # Calculate price
    total_price = 0
    for item in items:
        item_price = item["price"] * item["quantity"]
        if item.get("discount"):
            item_price *= (1 - item["discount"])
        total_price += item_price
    
    # Apply coupon if provided
    if coupon_code:
        # Simulate coupon validation
        time.sleep(0.1)
        valid_coupon = random.choice([True, False])
        if valid_coupon:
            # Assume 10% discount
            total_price *= 0.9
        else:
            print(f"Invalid coupon code: {coupon_code}")
    
    # Apply loyalty points
    if loyalty_points > 0:
        # Convert loyalty points to discount
        points_value = loyalty_points * 0.01
        if points_value > total_price * 0.2:  # Cap at 20% of total
            points_value = total_price * 0.2
        total_price -= points_value
    
    # Add gift wrap fee
    if gift_wrap:
        gift_wrap_fee = len(items) * 2  # $2 per item
        total_price += gift_wrap_fee
    
    # Calculate shipping cost
    shipping_cost = calculate_shipping_cost(shipping_address, items)
    total_price += shipping_cost
    
    # Process payment
    payment_result = process_payment(payment_info, total_price)
    if not payment_result["success"]:
        return {"status": "failed", "reason": "payment_failed", "details": payment_result["error"]}
    
    # Create order in database
    order_id = f"ORD-{random.randint(10000, 99999)}"
    # Simulate database insertion
    time.sleep(0.2)
    
    # Update inventory
    for item in items:
        # Simulate inventory update
        time.sleep(0.05)
        print(f"Updating inventory for item {item['id']}")
    
    # Generate shipping label
    # Simulate shipping label generation
    time.sleep(0.1)
    shipping_label = f"SHIP-{random.randint(10000, 99999)}"
    
    # Send notifications
    if notification_preferences.get("email"):
        # Simulate sending email
        time.sleep(0.1)
        print(f"Sending order confirmation email to customer {customer_id}")
    
    if notification_preferences.get("sms"):
        # Simulate sending SMS
        time.sleep(0.1)
        print(f"Sending order confirmation SMS to customer {customer_id}")
    
    # Return order information
    return {
        "status": "success",
        "order_id": order_id,
        "total_price": total_price,
        "shipping_label": shipping_label,
        "estimated_delivery": "3-5 business days"
    }


def calculate_shipping_cost(address, items):
    """Helper function for calculating shipping cost."""
    # Simplified calculation
    return 10.0


def process_payment(payment_info, amount):
    """Helper function for processing payment."""
    # Simulate payment processing
    time.sleep(0.2)
    success = random.random() > 0.1  # 90% success rate
    
    if success:
        return {"success": True}
    else:
        return {"success": False, "error": "Payment gateway error"}


# ISSUE: Function with excessive parameters
def generate_report(user_id, report_type, start_date, end_date, department, 
                   include_charts, chart_type, data_granularity, file_format,
                   include_summary, include_raw_data, page_size, color_scheme,
                   logo_position, custom_header, custom_footer, language):
    """
    Generates a report with too many parameters.
    This function should use a configuration object pattern instead.
    """
    print(f"Generating {report_type} report for user {user_id}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Department: {department}")
    print(f"Including charts: {include_charts}")
    if include_charts:
        print(f"Chart type: {chart_type}")
    print(f"Data granularity: {data_granularity}")
    print(f"File format: {file_format}")
    print(f"Include summary: {include_summary}")
    print(f"Include raw data: {include_raw_data}")
    print(f"Page size: {page_size}")
    print(f"Color scheme: {color_scheme}")
    print(f"Logo position: {logo_position}")
    print(f"Custom header: {custom_header}")
    print(f"Custom footer: {custom_footer}")
    print(f"Language: {language}")
    
    # Simulate report generation
    time.sleep(0.5)
    
    return {
        "report_id": f"REP-{random.randint(10000, 99999)}",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": f"{random.randint(100, 9999)} KB"
    }


# BETTER ALTERNATIVE: Using a configuration object pattern
class ReportConfig:
    def __init__(self, report_type, start_date, end_date):
        self.report_type = report_type
        self.start_date = start_date
        self.end_date = end_date
        self.department = None
        self.include_charts = False
        self.chart_type = None
        self.data_granularity = "daily"
        self.file_format = "pdf"
        self.include_summary = True
        self.include_raw_data = False
        self.page_size = "A4"
        self.color_scheme = "default"
        self.logo_position = "top-right"
        self.custom_header = None
        self.custom_footer = None
        self.language = "en"


def generate_report_better(user_id, config):
    """
    A better version of the report generation function using a configuration object.
    """
    print(f"Generating {config.report_type} report for user {user_id}")
    print(f"Period: {config.start_date} to {config.end_date}")
    
    # Simulate report generation
    time.sleep(0.5)
    
    return {
        "report_id": f"REP-{random.randint(10000, 99999)}",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": f"{random.randint(100, 9999)} KB"
    }