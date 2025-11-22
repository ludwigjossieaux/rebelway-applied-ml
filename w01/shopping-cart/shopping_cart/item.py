from dataclasses import dataclass, field
from shopping_cart.random_number_utils import RandomNumberUtils

@dataclass(frozen=True, order=True, slots=True)
class Item:
    name: str
    type: str
    _price: float = 0.0
    _id: str = field(default_factory=RandomNumberUtils.generate_random_id)

    @property
    def price(self) -> float:
        return round(self._price, 2)

    @property
    def search_string(self):
        return f"{self.name} {self.type}"