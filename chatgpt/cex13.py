from pos.order import Order
from pos.payment import OrderRepository


class OrderManagementSystem(OrderRepository):
    """
    Concrete implementation of OrderRepository.
    Manages order storage and calculations.
    """

    def __init__(self) -> None:
        self.orders: dict[str, Order] = {}

    def create_order(self, order_id: str, order: Order) -> None:
        """
        Add a new order to the system.

        Args:
            order_id: Unique identifier for the order.
            order: Order object to store.
        """
        self.orders[order_id] = order

    def find_order(self, order_id: str) -> Order:
        """
        Retrieve an order by its ID.

        Args:
            order_id: Unique identifier of the order.

        Returns:
            The corresponding Order object.
        """
        return self.orders[order_id]

    def compute_order_total_price(self, order: Order) -> int:
        """
        Calculate the total price of an order in cents.

        Args:
            order: The Order object.

        Returns:
            Total price in cents.
        """
        total_price = 0
        for index, price in enumerate(order.prices):
            quantity = order.quantities[index]
            total_price += price * quantity
        return total_price
