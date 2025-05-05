from dataclasses import dataclass

@dataclass
class LineItem:
    name: str
    quantity: int
    price: int

    def total_price(self) -> int:
        return self.quantity * self.price
