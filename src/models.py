from dataclasses import dataclass


@dataclass
class Product:
    name: str
    brand: str
    price: int
    rating: float
