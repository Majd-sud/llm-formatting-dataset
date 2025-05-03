from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class OrderStatus(Enum):
    """Possible statuses for an order."""
    OPEN = auto()
    PAID = auto()
    CANCELLED = auto()
    DELIVERED = auto()
    RETURNED = auto()


@dataclass
class Order:
    """Represents a customer order."""

    customer_id: int = 0
    customer_name: str = ""
    customer_address: str = ""
    customer_postal_code: str = ""
    customer_city: str = ""
    customer_email: str = ""
    items: List[str] = field(default_factory=list)
    quantities: List[int] = field(default_factory=list)
    prices: List[int] = field(default_factory=list)
    _status: OrderStatus = OrderStatus.OPEN
    id: str = ""

    def create_line_item(self, name: str, quantity: int, price: int) -> None:
        """
        Add a line item to the order.

        Args:
            name: Item name.
            quantity: Quantity of the item.
            price: Price per item.
        """
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def set_status(self, status: OrderStatus) -> None:
        """
        Update the status of the order.

        Args:
            status: A value from the OrderStatus enum.
        """
        self._status = status
