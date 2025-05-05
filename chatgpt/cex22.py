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

    result = {
        "order_id": order_data.get("order_id"),
        "status": "pending",
        "messages": [],
        "timestamps": {
            "started": datetime.datetime.now().isoformat()
        }
    }

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

    logger.debug(f"Loading customer data for ID: {order_data['customer_id']}")
    customer_data = {}
    try:
        customer_file = f"data/customers/{order_data['customer_id']}.json"
        if os.path.exists(customer_file):
            with open(customer_file, 'r') as f:
                customer_data = json.load(f)
        else:
            result["messages"].append(f"Customer not found: {order_data['customer_id']}")
            result["status"] = "error"
            return result
    except Exception as e:
        logger.error(f"Error loading customer data: {e}")
        result["messages"].append("Error loading customer data")
        result["status"] = "error"
        return result

    logger.debug("Checking inventory")
    items_with_details = []
    subtotal = 0
    inventory_updates = []

    for item in order_data["items"]:
        product_id = item["product_id"]
        quantity = item["quantity"]

        try:
            product_file = f"data/products/{product_id}.json"
            if not os.path.exists(product_file):
                result["messages"].append(f"Product not found: {product_id}")
                result["status"] = "error"
                return result

            with open(product_file, 'r') as f:
                product_data = json.load(f)

            if not product_data.get("active", True):
                result["messages"].append(f"Product is not available: {product_id}")
                result["status"] = "error"
                return result

            current_stock = product_data.get("stock", 0)
            if current_stock < quantity:
                result["messages"].append(f"Insufficient stock for product: {product_id}")
                result["status"] = "error"
                return result

            price = product_data.get("price", 0)
            item_total = price * quantity
            subtotal += item_total

            inventory_updates.append({
                "product_id": product_id,
                "old_stock": current_stock,
                "new_stock": current_stock - quantity,
                "change": -quantity
            })

            items_with_details.append({
                "product_id": product_id,
                "name": product_data.get("name", "Unknown Product"),
                "price": price,
                "quantity": quantity,
                "total": item_total
            })

        except Exception as e:
            logger.error(f"Error processing product {product_id}: {e}")
            result["messages"].append(f"Error processing product: {product_id}")
            result["status"] = "error"
            return result

    logger.debug("Calculating pricing")
    result["subtotal"] = subtotal

    tax_rate = 0.08
    if address["state"] in ["DE", "MT", "NH", "OR"]:
        tax_rate = 0
    elif address["state"] == "CA":
        tax_rate = 0.0725
    elif address["state"] == "NY":
        tax_rate = 0.045

    tax_amount = subtotal * tax_rate
    result["tax"] = round(tax_amount, 2)

    shipping_cost = 0
    if address["country"] == "US":
        shipping_cost = 0 if subtotal >= 100 else 10
    else:
        shipping_cost = 25

    result["shipping"] = shipping_cost

    discount_amount = 0
    customer_type = customer_data.get("type", "regular")
    if customer_type == "premium":
        discount_amount += subtotal * 0.1
        result["messages"].append("Applied 10% premium customer discount")
    elif customer_data.get("orders_count", 0) > 10:
        discount_amount += subtotal * 0.05
        result["messages"].append("Applied 5% loyalty discount")

    if order_data.get("coupon_code"):
        coupon_code = order_data["coupon_code"]
        if coupon_code == "SAVE20":
            additional_discount = subtotal * 0.2
            discount_amount += additional_discount
            result["messages"].append("Applied 20% coupon discount")
        elif coupon_code == "FREESHIP":
            shipping_cost = 0
            result["shipping"] = 0
            result["messages"].append("Applied free shipping coupon")

    result["discount"] = round(discount_amount, 2)
    total = subtotal + tax_amount + shipping_cost - discount_amount
    result["total"] = round(total, 2)

    logger.debug("Processing payment")
    payment_method = payment_info["method"]
    payment_result = {
        "success": False,
        "transaction_id": None,
        "message": ""
    }

    try:
        if payment_method == "credit_card":
            required_fields = ["card_number", "expiry", "cvv"]
            for field in required_fields:
                if not payment_info.get(field):
                    result["messages"].append(f"Credit card {field} is required")
                    result["status"] = "payment_error"
                    return result

            time.sleep(1)
            if random.random() < 0.9:
                payment_result["success"] = True
                payment_result["transaction_id"] = f"CC-{int(time.time())}-{random.randint(1000, 9999)}"
                payment_result["message"] = "Payment processed successfully"
            else:
                payment_result["message"] = "Payment declined by issuer"

        elif payment_method == "paypal":
            if not payment_info.get("email"):
                result["messages"].append("PayPal email is required")
                result["status"] = "payment_error"
                return result

            time.sleep(1)
            if random.random() < 0.95:
                payment_result["success"] = True
                payment_result["transaction_id"] = f"PP-{int(time.time())}-{random.randint(1000, 9999)}"
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

    result["status"] = "completed"
    result["timestamps"]["completed"] = datetime.datetime.now().isoformat()
    result["processing_time"] = (
        datetime.datetime.fromisoformat(result["timestamps"]["completed"]) -
        datetime.datetime.fromisoformat(result["timestamps"]["started"])
    ).total_seconds()

    logger.info(f"Order processed successfully: {order_data.get('order_id')}")
    return result
