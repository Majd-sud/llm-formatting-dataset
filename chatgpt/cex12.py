from typing import Protocol
from pos.order import Order


class PaymentServiceConnectionError(Exception):
    """
    Custom error that is raised when we couldn't connect to the payment service.
    """
    pass


class OrderRepository(Protocol):
    """
    Protocol for accessing and processing order data.
    """

    def find_order(self, order_id: str) -> Order:
        """Fetch an order by ID."""
        ...

    def compute_order_total_price(self, order: Order) -> int:
        """Compute total price in cents for the given order."""
        ...


class StripePaymentProcessor:
    """
    Simulated Stripe payment processor that uses an OrderRepository.
    """

    def __init__(self, system: OrderRepository):
        self.connected = False
        self.system = system

    def connect_to_service(self, url: str) -> None:
        """
        Simulate connecting to an external payment service.

        Args:
            url: The URL of the payment provider.
        """
        print(f"Connecting to payment processing service at {url}... done!")
        self.connected = True

    def process_payment(self, order_id: str) -> None:
        """
        Process payment for an order by ID.

        Args:
            order_id: The ID of the order to process.

        Raises:
            PaymentServiceConnectionError: If not connected to the payment service.
        """
        if not self.connected:
            raise PaymentServiceConnectionError("Payment service is not connected.")

        order = self.system.find_order(order_id)
        total_price = self.system.compute_order_total_price(order)

        print(f"Processing payment of ${(total_price / 100):.2f}, reference: {order.id}.")
