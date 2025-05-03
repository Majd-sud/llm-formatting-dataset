from dataclasses import dataclass


@dataclass
class LineItem:
    """
    Represents an item in an order with its quantity and unit price.
    """
    name: str
    quantity: int
    price: int  # Price in cents (e.g., 500 = $5.00)

    def total_price(self) -> int:
        """
        Calculate total price for this line item.

        Returns:
            Total price as quantity × unit price (in cents).
        """
        return self.quantity * self.price
