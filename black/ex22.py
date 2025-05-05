"""
This module contains examples of long methods that should be flagged by SonarQube.
Long methods are hard to understand, test, and maintain because they often do too many things.
"""

import csv
import datetime
import json
import logging
import math
import os
import random
import re
import time
from typing import Dict, List, Any, Optional, Tuple, Union


# ISSUE: Long method that does too many things
def process_customer_order_long(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a customer order from start to finish.
    This method is too long and does too many things:
    - Validates order data
    - Checks inventory
    - Calculates pricing
    - Applies discounts
    - Processes payment
    - Updates inventory
    - Generates shipping label
    - Sends confirmation emails
    - Updates customer records
    - Logs the transaction
    """
    logger = logging.getLogger("order_processor")
    logger.info(f"Processing order: {order_data.get('order_id')}")

    # Initialize result
    result = {
        "order_id": order_data.get("order_id"),
        "status": "pending",
        "messages": [],
        "timestamps": {"started": datetime.datetime.now().isoformat()},
    }

    # Validate order data
    logger.debug("Validating order data")
    if not order_data.get("customer_id"):
        result["messages"].append("Customer ID is required")
        result["status"] = "error"
        return result

    if not order_data.get("items") or len(order_data["items"]) == 0:
        result["messages"].append("Order must contain at least one item")
        result["status"] = "error"
        return result

    for item in order_data["items"]:
        if not item.get("product_id"):
            result["messages"].append("Product ID is required for all items")
            result["status"] = "error"
            return result

        if not item.get("quantity") or item["quantity"] <= 0:
            result["messages"].append("Quantity must be positive for all items")
            result["status"] = "error"
            return result

    if not order_data.get("shipping_address"):
        result["messages"].append("Shipping address is required")
        result["status"] = "error"
        return result

    address = order_data["shipping_address"]
    required_address_fields = ["street", "city", "state", "zip", "country"]
    for field in required_address_fields:
        if not address.get(field):
            result["messages"].append(f"Shipping address {field} is required")
            result["status"] = "error"
            return result

    if not order_data.get("payment_info"):
        result["messages"].append("Payment information is required")
        result["status"] = "error"
        return result

    payment_info = order_data["payment_info"]
    if not payment_info.get("method"):
        result["messages"].append("Payment method is required")
        result["status"] = "error"
        return result

    # Load customer data
    logger.debug(f"Loading customer data for ID: {order_data['customer_id']}")
    customer_data = {}
    try:
        customer_file = f"data/customers/{order_data['customer_id']}.json"
        if os.path.exists(customer_file):
            with open(customer_file, "r") as f:
                customer_data = json.load(f)
        else:
            result["messages"].append(
                f"Customer not found: {order_data['customer_id']}"
            )
            result["status"] = "error"
            return result
    except Exception as e:
        logger.error(f"Error loading customer data: {e}")
        result["messages"].append("Error loading customer data")
        result["status"] = "error"
        return result

    # Check inventory and get product details
    logger.debug("Checking inventory")
    items_with_details = []
    subtotal = 0
    inventory_updates = []

    for item in order_data["items"]:
        product_id = item["product_id"]
        quantity = item["quantity"]

        # Load product data
        try:
            product_file = f"data/products/{product_id}.json"
            if not os.path.exists(product_file):
                result["messages"].append(f"Product not found: {product_id}")
                result["status"] = "error"
                return result

            with open(product_file, "r") as f:
                product_data = json.load(f)

            # Check if product is active
            if not product_data.get("active", True):
                result["messages"].append(f"Product is not available: {product_id}")
                result["status"] = "error"
                return result

            # Check inventory
            current_stock = product_data.get("stock", 0)
            if current_stock < quantity:
                result["messages"].append(
                    f"Insufficient stock for product: {product_id}"
                )
                result["status"] = "error"
                return result

            # Calculate item price
            price = product_data.get("price", 0)
            item_total = price * quantity
            subtotal += item_total

            # Prepare inventory update
            inventory_updates.append(
                {
                    "product_id": product_id,
                    "old_stock": current_stock,
                    "new_stock": current_stock - quantity,
                    "change": -quantity,
                }
            )

            # Add item with details
            items_with_details.append(
                {
                    "product_id": product_id,
                    "name": product_data.get("name", "Unknown Product"),
                    "price": price,
                    "quantity": quantity,
                    "total": item_total,
                }
            )

        except Exception as e:
            logger.error(f"Error processing product {product_id}: {e}")
            result["messages"].append(f"Error processing product: {product_id}")
            result["status"] = "error"
            return result

    # Calculate pricing
    logger.debug("Calculating pricing")
    result["subtotal"] = subtotal

    # Calculate tax
    tax_rate = 0.08  # 8% tax rate
    if address["state"] in ["DE", "MT", "NH", "OR"]:
        tax_rate = 0  # No sales tax in these states
    elif address["state"] == "CA":
        tax_rate = 0.0725  # California tax rate
    elif address["state"] == "NY":
        tax_rate = 0.045  # New York tax rate

    tax_amount = subtotal * tax_rate
    result["tax"] = round(tax_amount, 2)

    # Calculate shipping cost
    shipping_cost = 0
    if address["country"] == "US":
        if subtotal >= 100:
            shipping_cost = 0  # Free shipping for orders over $100
        else:
            shipping_cost = 10  # Standard US shipping
    else:
        shipping_cost = 25  # International shipping

    result["shipping"] = shipping_cost

    # Apply discounts
    discount_amount = 0
    customer_type = customer_data.get("type", "regular")

    # Loyalty discount
    if customer_type == "premium":
        discount_amount += subtotal * 0.1  # 10% discount for premium customers
        result["messages"].append("Applied 10% premium customer discount")
    elif customer_data.get("orders_count", 0) > 10:
        discount_amount += subtotal * 0.05  # 5% discount for loyal customers
        result["messages"].append("Applied 5% loyalty discount")

    # Coupon code discount
    if order_data.get("coupon_code"):
        coupon_code = order_data["coupon_code"]
        # In a real system, this would validate against a database of coupon codes
        if coupon_code == "SAVE20":
            additional_discount = subtotal * 0.2
            discount_amount += additional_discount
            result["messages"].append("Applied 20% coupon discount")
        elif coupon_code == "FREESHIP":
            shipping_cost = 0
            result["shipping"] = 0
            result["messages"].append("Applied free shipping coupon")

    result["discount"] = round(discount_amount, 2)

    # Calculate total
    total = subtotal + tax_amount + shipping_cost - discount_amount
    result["total"] = round(total, 2)

    # Process payment
    logger.debug("Processing payment")
    payment_method = payment_info["method"]
    payment_result = {"success": False, "transaction_id": None, "message": ""}

    try:
        if payment_method == "credit_card":
            if not payment_info.get("card_number"):
                result["messages"].append("Credit card number is required")
                result["status"] = "payment_error"
                return result

            if not payment_info.get("expiry"):
                result["messages"].append("Credit card expiry is required")
                result["status"] = "payment_error"
                return result

            if not payment_info.get("cvv"):
                result["messages"].append("Credit card CVV is required")
                result["status"] = "payment_error"
                return result

            # In a real system, this would call a payment gateway API
            # Simulate payment processing
            time.sleep(1)

            # Simulate success or failure (90% success rate)
            if random.random() < 0.9:
                payment_result["success"] = True
                payment_result["transaction_id"] = (
                    f"CC-{int(time.time())}-{random.randint(1000, 9999)}"
                )
                payment_result["message"] = "Payment processed successfully"
            else:
                payment_result["message"] = "Payment declined by issuer"

        elif payment_method == "paypal":
            if not payment_info.get("email"):
                result["messages"].append("PayPal email is required")
                result["status"] = "payment_error"
                return result

            # In a real system, this would call PayPal's API
            # Simulate payment processing
            time.sleep(1)

            # Simulate success or failure (95% success rate)
            if random.random() < 0.95:
                payment_result["success"] = True
                payment_result["transaction_id"] = (
                    f"PP-{int(time.time())}-{random.randint(1000, 9999)}"
                )
                payment_result["message"] = "Payment processed successfully"
            else:
                payment_result["message"] = "PayPal payment failed"

        else:
            payment_result["message"] = f"Unsupported payment method: {payment_method}"

    except Exception as e:
        logger.error(f"Payment processing error: {e}")
        payment_result["message"] = f"Payment processing error: {str(e)}"

    result["payment_result"] = payment_result

    if not payment_result["success"]:
        result["status"] = "payment_error"
        result["messages"].append(payment_result["message"])
        return result

    # Update inventory
    logger.debug("Updating inventory")
    for update in inventory_updates:
        product_id = update["product_id"]
        new_stock = update["new_stock"]

        try:
            product_file = f"data/products/{product_id}.json"
            with open(product_file, "r") as f:
                product_data = json.load(f)

            product_data["stock"] = new_stock

            with open(product_file, "w") as f:
                json.dump(product_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating inventory for product {product_id}: {e}")
            # Continue processing, but log the error
            result["messages"].append(
                f"Warning: Inventory update failed for product {product_id}"
            )

    # Generate shipping label
    logger.debug("Generating shipping label")
    shipping_label = {
        "order_id": order_data.get("order_id"),
        "customer_name": f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}",
        "address": {
            "street": address["street"],
            "city": address["city"],
            "state": address["state"],
            "zip": address["zip"],
            "country": address["country"],
        },
        "shipping_method": order_data.get("shipping_method", "standard"),
        "tracking_number": f"TRK-{int(time.time())}-{random.randint(10000, 99999)}",
        "generated_at": datetime.datetime.now().isoformat(),
    }

    result["shipping_label"] = shipping_label

    # Calculate estimated delivery date
    today = datetime.date.today()
    if shipping_label["shipping_method"] == "express":
        delivery_days = 2
    elif shipping_label["shipping_method"] == "priority":
        delivery_days = 3
    else:  # standard
        delivery_days = 5
        if address["country"] != "US":
            delivery_days = 10

    # Skip weekends
    delivery_date = today
    for _ in range(delivery_days):
        delivery_date += datetime.timedelta(days=1)
        while delivery_date.weekday() >= 5:  # Saturday or Sunday
            delivery_date += datetime.timedelta(days=1)

    result["estimated_delivery"] = delivery_date.isoformat()

    # Send confirmation email
    logger.debug("Sending confirmation email")
    try:
        if customer_data.get("email"):
            # In a real system, this would send an actual email
            email_subject = f"Order Confirmation #{order_data.get('order_id')}"

            # Build email body
            email_body = f"""
            Dear {customer_data.get('first_name', 'Valued Customer')},
            
            Thank you for your order! We're pleased to confirm that your order has been received and is being processed.
            
            Order Details:
            - Order Number: {order_data.get('order_id')}
            - Order Date: {datetime.date.today().isoformat()}
            - Payment Method: {payment_method}
            - Tracking Number: {shipping_label['tracking_number']}
            - Estimated Delivery: {result['estimated_delivery']}
            
            Items:
            """

            for item in items_with_details:
                email_body += (
                    f"- {item['name']} x {item['quantity']} - ${item['total']:.2f}\n"
                )

            email_body += f"""
            Subtotal: ${result['subtotal']:.2f}
            Shipping: ${result['shipping']:.2f}
            Tax: ${result['tax']:.2f}
            Discount: ${result['discount']:.2f}
            Total: ${result['total']:.2f}
            
            Shipping Address:
            {shipping_label['customer_name']}
            {address['street']}
            {address['city']}, {address['state']} {address['zip']}
            {address['country']}
            
            If you have any questions about your order, please contact our customer service team.
            
            Thank you for shopping with us!
            """

            # Simulate sending email
            print(f"Sending email to: {customer_data.get('email')}")
            print(f"Subject: {email_subject}")
            print("Email sent successfully")

            result["email_sent"] = True

    except Exception as e:
        logger.error(f"Error sending confirmation email: {e}")
        result["messages"].append("Warning: Failed to send confirmation email")
        result["email_sent"] = False

    # Update customer records
    logger.debug("Updating customer records")
    try:
        # Update order count
        customer_data["orders_count"] = customer_data.get("orders_count", 0) + 1

        # Update total spent
        customer_data["total_spent"] = (
            customer_data.get("total_spent", 0) + result["total"]
        )

        # Update last order date
        customer_data["last_order_date"] = datetime.date.today().isoformat()

        # Save updated customer data
        with open(f"data/customers/{order_data['customer_id']}.json", "w") as f:
            json.dump(customer_data, f, indent=2)

    except Exception as e:
        logger.error(f"Error updating customer records: {e}")
        result["messages"].append("Warning: Failed to update customer records")

    # Save order to database
    logger.debug("Saving order to database")
    try:
        # Create order record
        order_record = {
            "order_id": order_data.get("order_id"),
            "customer_id": order_data["customer_id"],
            "order_date": datetime.date.today().isoformat(),
            "items": items_with_details,
            "subtotal": result["subtotal"],
            "tax": result["tax"],
            "shipping": result["shipping"],
            "discount": result["discount"],
            "total": result["total"],
            "payment": {
                "method": payment_method,
                "transaction_id": payment_result["transaction_id"],
                "status": "completed",
            },
            "shipping_address": address,
            "shipping_label": shipping_label,
            "estimated_delivery": result["estimated_delivery"],
            "status": "processing",
        }

        # Ensure orders directory exists
        os.makedirs("data/orders", exist_ok=True)

        # Save order to file (simulating database save)
        with open(f"data/orders/{order_data.get('order_id')}.json", "w") as f:
            json.dump(order_record, f, indent=2)

    except Exception as e:
        logger.error(f"Error saving order: {e}")
        result["messages"].append("Warning: Failed to save order record")

    # Log the transaction
    logger.debug("Logging transaction")
    try:
        # Ensure logs directory exists
        os.makedirs("data/logs", exist_ok=True)

        # Append to transaction log
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "order_id": order_data.get("order_id"),
            "customer_id": order_data["customer_id"],
            "total": result["total"],
            "payment_method": payment_method,
            "transaction_id": payment_result["transaction_id"],
            "status": "completed",
        }

        with open("data/logs/transactions.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        logger.error(f"Error logging transaction: {e}")
        # Non-critical error, just log it

    # Set final status and timestamps
    result["status"] = "completed"
    result["timestamps"]["completed"] = datetime.datetime.now().isoformat()
    result["processing_time"] = (
        datetime.datetime.fromisoformat(result["timestamps"]["completed"])
        - datetime.datetime.fromisoformat(result["timestamps"]["started"])
    ).total_seconds()

    logger.info(f"Order processed successfully: {order_data.get('order_id')}")
    return result


# BETTER ALTERNATIVE: Refactored code with smaller, focused methods


def process_customer_order_better(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a customer order from start to finish.
    This is a refactored version that delegates to smaller, focused methods.
    """
    logger = logging.getLogger("order_processor")
    logger.info(f"Processing order: {order_data.get('order_id')}")

    # Initialize result
    result = {
        "order_id": order_data.get("order_id"),
        "status": "pending",
        "messages": [],
        "timestamps": {"started": datetime.datetime.now().isoformat()},
    }

    # Validate order data
    validation_result = _validate_order_data(order_data)
    if not validation_result["valid"]:
        result["messages"].extend(validation_result["errors"])
        result["status"] = "error"
        return result

    # Load customer data
    customer_data = _load_customer_data(order_data["customer_id"])
    if not customer_data:
        result["messages"].append(f"Customer not found: {order_data['customer_id']}")
        result["status"] = "error"
        return result

    # Check inventory and get product details
    inventory_result = _check_inventory_and_get_details(order_data["items"])
    if not inventory_result["success"]:
        result["messages"].extend(inventory_result["errors"])
        result["status"] = "error"
        return result

    result["subtotal"] = inventory_result["subtotal"]
    items_with_details = inventory_result["items_with_details"]
    inventory_updates = inventory_result["inventory_updates"]

    # Calculate pricing
    pricing_result = _calculate_pricing(
        result["subtotal"],
        order_data["shipping_address"],
        customer_data,
        order_data.get("coupon_code"),
    )

    result.update(pricing_result)

    # Process payment
    payment_result = _process_payment(order_data["payment_info"], result["total"])
    result["payment_result"] = payment_result

    if not payment_result["success"]:
        result["status"] = "payment_error"
        result["messages"].append(payment_result["message"])
        return result

    # Update inventory
    _update_inventory(inventory_updates)

    # Generate shipping label
    shipping_label = _generate_shipping_label(
        order_data.get("order_id"),
        customer_data,
        order_data["shipping_address"],
        order_data.get("shipping_method", "standard"),
    )

    result["shipping_label"] = shipping_label

    # Calculate estimated delivery date
    result["estimated_delivery"] = _calculate_delivery_date(
        shipping_label["shipping_method"], order_data["shipping_address"]["country"]
    )

    # Send confirmation email
    email_result = _send_confirmation_email(
        customer_data, order_data, items_with_details, result, shipping_label
    )

    result["email_sent"] = email_result["success"]
    if not email_result["success"]:
        result["messages"].append("Warning: Failed to send confirmation email")

    # Update customer records
    _update_customer_records(customer_data, result["total"])

    # Save order to database
    _save_order_to_database(
        order_data,
        customer_data,
        items_with_details,
        result,
        shipping_label,
        payment_result,
    )

    # Log the transaction
    _log_transaction(
        order_data.get("order_id"),
        order_data["customer_id"],
        result["total"],
        order_data["payment_info"]["method"],
        payment_result["transaction_id"],
    )

    # Set final status and timestamps
    result["status"] = "completed"
    result["timestamps"]["completed"] = datetime.datetime.now().isoformat()
    result["processing_time"] = (
        datetime.datetime.fromisoformat(result["timestamps"]["completed"])
        - datetime.datetime.fromisoformat(result["timestamps"]["started"])
    ).total_seconds()

    logger.info(f"Order processed successfully: {order_data.get('order_id')}")
    return result


def _validate_order_data(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate order data."""
    errors = []

    # Check customer ID
    if not order_data.get("customer_id"):
        errors.append("Customer ID is required")

    # Check items
    if not order_data.get("items") or len(order_data["items"]) == 0:
        errors.append("Order must contain at least one item")
    else:
        for item in order_data["items"]:
            if not item.get("product_id"):
                errors.append("Product ID is required for all items")

            if not item.get("quantity") or item["quantity"] <= 0:
                errors.append("Quantity must be positive for all items")

    # Check shipping address
    if not order_data.get("shipping_address"):
        errors.append("Shipping address is required")
    else:
        address = order_data["shipping_address"]
        required_address_fields = ["street", "city", "state", "zip", "country"]
        for field in required_address_fields:
            if not address.get(field):
                errors.append(f"Shipping address {field} is required")

    # Check payment info
    if not order_data.get("payment_info"):
        errors.append("Payment information is required")
    elif not order_data["payment_info"].get("method"):
        errors.append("Payment method is required")

    return {"valid": len(errors) == 0, "errors": errors}


def _load_customer_data(customer_id: str) -> Optional[Dict[str, Any]]:
    """Load customer data from file."""
    try:
        customer_file = f"data/customers/{customer_id}.json"
        if os.path.exists(customer_file):
            with open(customer_file, "r") as f:
                return json.load(f)
        return None
    except Exception as e:
        logging.error(f"Error loading customer data: {e}")
        return None


def _check_inventory_and_get_details(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check inventory and get product details."""
    result = {
        "success": True,
        "errors": [],
        "items_with_details": [],
        "inventory_updates": [],
        "subtotal": 0,
    }

    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]

        try:
            product_file = f"data/products/{product_id}.json"
            if not os.path.exists(product_file):
                result["errors"].append(f"Product not found: {product_id}")
                result["success"] = False
                return result

            with open(product_file, "r") as f:
                product_data = json.load(f)

            # Check if product is active
            if not product_data.get("active", True):
                result["errors"].append(f"Product is not available: {product_id}")
                result["success"] = False
                return result

            # Check inventory
            current_stock = product_data.get("stock", 0)
            if current_stock < quantity:
                result["errors"].append(f"Insufficient stock for product: {product_id}")
                result["success"] = False
                return result

            # Calculate item price
            price = product_data.get("price", 0)
            item_total = price * quantity
            result["subtotal"] += item_total

            # Prepare inventory update
            result["inventory_updates"].append(
                {
                    "product_id": product_id,
                    "old_stock": current_stock,
                    "new_stock": current_stock - quantity,
                    "change": -quantity,
                }
            )

            # Add item with details
            result["items_with_details"].append(
                {
                    "product_id": product_id,
                    "name": product_data.get("name", "Unknown Product"),
                    "price": price,
                    "quantity": quantity,
                    "total": item_total,
                }
            )

        except Exception as e:
            logging.error(f"Error processing product {product_id}: {e}")
            result["errors"].append(f"Error processing product: {product_id}")
            result["success"] = False
            return result

    return result


def _calculate_pricing(
    subtotal: float,
    address: Dict[str, Any],
    customer_data: Dict[str, Any],
    coupon_code: Optional[str],
) -> Dict[str, float]:
    """Calculate pricing including tax, shipping, and discounts."""
    result = {"subtotal": subtotal}

    # Calculate tax
    tax_rate = 0.08  # 8% tax rate
    if address["state"] in ["DE", "MT", "NH", "OR"]:
        tax_rate = 0  # No sales tax in these states
    elif address["state"] == "CA":
        tax_rate = 0.0725  # California tax rate
    elif address["state"] == "NY":
        tax_rate = 0.045  # New York tax rate

    tax_amount = subtotal * tax_rate
    result["tax"] = round(tax_amount, 2)

    # Calculate shipping cost
    shipping_cost = 0
    if address["country"] == "US":
        if subtotal >= 100:
            shipping_cost = 0  # Free shipping for orders over $100
        else:
            shipping_cost = 10  # Standard US shipping
    else:
        shipping_cost = 25  # International shipping

    result["shipping"] = shipping_cost

    # Apply discounts
    discount_amount = 0
    messages = []
    customer_type = customer_data.get("type", "regular")

    # Loyalty discount
    if customer_type == "premium":
        discount_amount += subtotal * 0.1  # 10% discount for premium customers
        messages.append("Applied 10% premium customer discount")
    elif customer_data.get("orders_count", 0) > 10:
        discount_amount += subtotal * 0.05  # 5% discount for loyal customers
        messages.append("Applied 5% loyalty discount")

    # Coupon code discount
    if coupon_code:
        # In a real system, this would validate against a database of coupon codes
        if coupon_code == "SAVE20":
            additional_discount = subtotal * 0.2
            discount_amount += additional_discount
            messages.append("Applied 20% coupon discount")
        elif coupon_code == "FREESHIP":
            shipping_cost = 0
            result["shipping"] = 0
            messages.append("Applied free shipping coupon")

    result["discount"] = round(discount_amount, 2)
    result["discount_messages"] = messages

    # Calculate total
    total = subtotal + tax_amount + shipping_cost - discount_amount
    result["total"] = round(total, 2)

    return result


def _process_payment(payment_info: Dict[str, Any], total: float) -> Dict[str, Any]:
    """Process payment."""
    payment_result = {"success": False, "transaction_id": None, "message": ""}

    try:
        payment_method = payment_info["method"]

        if payment_method == "credit_card":
            if not payment_info.get("card_number"):
                return {"success": False, "message": "Credit card number is required"}

            if not payment_info.get("expiry"):
                return {"success": False, "message": "Credit card expiry is required"}

            if not payment_info.get("cvv"):
                return {"success": False, "message": "Credit card CVV is required"}

            # In a real system, this would call a payment gateway API
            # Simulate payment processing
            time.sleep(0.2)

            # Simulate success or failure (90% success rate)
            if random.random() < 0.9:
                payment_result["success"] = True
                payment_result["transaction_id"] = (
                    f"CC-{int(time.time())}-{random.randint(1000, 9999)}"
                )
                payment_result["message"] = "Payment processed successfully"
            else:
                payment_result["message"] = "Payment declined by issuer"

        elif payment_method == "paypal":
            if not payment_info.get("email"):
                return {"success": False, "message": "PayPal email is required"}

            # In a real system, this would call PayPal's API
            # Simulate payment processing
            time.sleep(0.2)

            # Simulate success or failure (95% success rate)
            if random.random() < 0.95:
                payment_result["success"] = True
                payment_result["transaction_id"] = (
                    f"PP-{int(time.time())}-{random.randint(1000, 9999)}"
                )
                payment_result["message"] = "Payment processed successfully"
            else:
                payment_result["message"] = "PayPal payment failed"

        else:
            payment_result["message"] = f"Unsupported payment method: {payment_method}"

    except Exception as e:
        logging.error(f"Payment processing error: {e}")
        payment_result["message"] = f"Payment processing error: {str(e)}"

    return payment_result


def _update_inventory(inventory_updates: List[Dict[str, Any]]) -> None:
    """Update inventory for products."""
    for update in inventory_updates:
        product_id = update["product_id"]
        new_stock = update["new_stock"]

        try:
            product_file = f"data/products/{product_id}.json"
            with open(product_file, "r") as f:
                product_data = json.load(f)

            product_data["stock"] = new_stock

            with open(product_file, "w") as f:
                json.dump(product_data, f, indent=2)

        except Exception as e:
            logging.error(f"Error updating inventory for product {product_id}: {e}")
            # Continue processing, but log the error


def _generate_shipping_label(
    order_id: str,
    customer_data: Dict[str, Any],
    address: Dict[str, Any],
    shipping_method: str,
) -> Dict[str, Any]:
    """Generate a shipping label."""
    return {
        "order_id": order_id,
        "customer_name": f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}",
        "address": {
            "street": address["street"],
            "city": address["city"],
            "state": address["state"],
            "zip": address["zip"],
            "country": address["country"],
        },
        "shipping_method": shipping_method,
        "tracking_number": f"TRK-{int(time.time())}-{random.randint(10000, 99999)}",
        "generated_at": datetime.datetime.now().isoformat(),
    }


def _calculate_delivery_date(shipping_method: str, country: str) -> str:
    """Calculate estimated delivery date."""
    today = datetime.date.today()

    if shipping_method == "express":
        delivery_days = 2
    elif shipping_method == "priority":
        delivery_days = 3
    else:  # standard
        delivery_days = 5
        if country != "US":
            delivery_days = 10

    # Skip weekends
    delivery_date = today
    for _ in range(delivery_days):
        delivery_date += datetime.timedelta(days=1)
        while delivery_date.weekday() >= 5:  # Saturday or Sunday
            delivery_date += datetime.timedelta(days=1)

    return delivery_date.isoformat()


def _send_confirmation_email(
    customer_data: Dict[str, Any],
    order_data: Dict[str, Any],
    items: List[Dict[str, Any]],
    result: Dict[str, Any],
    shipping_label: Dict[str, Any],
) -> Dict[str, bool]:
    """Send order confirmation email."""
    try:
        if not customer_data.get("email"):
            return {"success": False}

        # In a real system, this would send an actual email
        email_subject = f"Order Confirmation #{order_data.get('order_id')}"

        # Build email body (simplified for brevity)
        email_body = f"Order confirmation for {customer_data.get('first_name')} {customer_data.get('last_name')}"

        # Simulate sending email
        print(f"Sending email to: {customer_data.get('email')}")
        print(f"Subject: {email_subject}")
        print("Email sent successfully")

        return {"success": True}

    except Exception as e:
        logging.error(f"Error sending confirmation email: {e}")
        return {"success": False}


def _update_customer_records(customer_data: Dict[str, Any], total: float) -> None:
    """Update customer records."""
    try:
        # Update order count
        customer_data["orders_count"] = customer_data.get("orders_count", 0) + 1

        # Update total spent
        customer_data["total_spent"] = customer_data.get("total_spent", 0) + total

        # Update last order date
        customer_data["last_order_date"] = datetime.date.today().isoformat()

        # Save updated customer data
        with open(f"data/customers/{customer_data['id']}.json", "w") as f:
            json.dump(customer_data, f, indent=2)

    except Exception as e:
        logging.error(f"Error updating customer records: {e}")
        # Continue processing, but log the error


def _save_order_to_database(
    order_data: Dict[str, Any],
    customer_data: Dict[str, Any],
    items: List[Dict[str, Any]],
    result: Dict[str, Any],
    shipping_label: Dict[str, Any],
    payment_result: Dict[str, Any],
) -> None:
    """Save order to database."""
    try:
        # Create order record
        order_record = {
            "order_id": order_data.get("order_id"),
            "customer_id": customer_data["id"],
            "order_date": datetime.date.today().isoformat(),
            "items": items,
            "subtotal": result["subtotal"],
            "tax": result["tax"],
            "shipping": result["shipping"],
            "discount": result["discount"],
            "total": result["total"],
            "payment": {
                "method": order_data["payment_info"]["method"],
                "transaction_id": payment_result["transaction_id"],
                "status": "completed",
            },
            "shipping_address": order_data["shipping_address"],
            "shipping_label": shipping_label,
            "estimated_delivery": result["estimated_delivery"],
            "status": "processing",
        }

        # Ensure orders directory exists
        os.makedirs("data/orders", exist_ok=True)

        # Save order to file (simulating database save)
        with open(f"data/orders/{order_data.get('order_id')}.json", "w") as f:
            json.dump(order_record, f, indent=2)

    except Exception as e:
        logging.error(f"Error saving order: {e}")
        # Continue processing, but log the error


def _log_transaction(
    order_id: str,
    customer_id: str,
    total: float,
    payment_method: str,
    transaction_id: str,
) -> None:
    """Log the transaction."""
    try:
        # Ensure logs directory exists
        os.makedirs("data/logs", exist_ok=True)

        # Append to transaction log
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "order_id": order_id,
            "customer_id": customer_id,
            "total": total,
            "payment_method": payment_method,
            "transaction_id": transaction_id,
            "status": "completed",
        }

        with open("data/logs/transactions.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        logging.error(f"Error logging transaction: {e}")
        # Non-critical error, just log it
