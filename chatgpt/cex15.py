from dataclasses import dataclass


@dataclass
class Customer:
    """
    Represents a customer with basic contact and location information.
    """
    id: int = 0
    name: str = ""
    address: str = ""
    postal_code: str = ""
    city: str = ""
    email: str = ""
