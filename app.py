import json
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class GiftItem:
    id: int
    name: str
    occasions: List[str]
    age_min: int
    age_max: int
    genders: List[str]
    price: float
    description: str


class GiftCatalog:
    def __init__(self, items: List[GiftItem]):
        self.items = items

    @staticmethod
    def from_file(path: str) -> 'GiftCatalog':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        items = [GiftItem(**item) for item in data]
        return GiftCatalog(items)

    def suggest(self, occasion: str, age: int, gender: str) -> List[GiftItem]:
        matches = []
        gender = gender.lower()
        for item in self.items:
            if occasion.lower() not in [o.lower() for o in item.occasions]:
                continue
            if not (item.age_min <= age <= item.age_max):
                continue
            if gender not in [g.lower() for g in item.genders] and 'any' not in [g.lower() for g in item.genders]:
                continue
            matches.append(item)
        return matches


def prompt_customer_requirements() -> Dict[str, str | int]:
    occasion = input('Occasion (e.g. birthday, anniversary): ').strip()
    age = int(input('Recipient age: '))
    gender = input('Recipient gender (male/female/other): ').strip()
    return {'occasion': occasion, 'age': age, 'gender': gender}


def choose_gift(suggestions: List[GiftItem]) -> GiftItem | None:
    if not suggestions:
        print('No gift suggestions match your criteria.')
        return None
    print('\nAvailable gift options:')
    for idx, item in enumerate(suggestions, 1):
        print(f"{idx}. {item.name} - ${item.price:.2f} -> {item.description}")
    choice = int(input('Select a gift by number (or 0 to cancel): '))
    if choice <= 0 or choice > len(suggestions):
        print('Cancelled.')
        return None
    return suggestions[choice - 1]


def collect_shipping_info() -> Dict[str, str]:
    print('\nShipping information:')
    name = input('Recipient name: ').strip()
    address = input('Shipping address: ').strip()
    return {'name': name, 'address': address}


def process_payment(amount: float) -> bool:
    print(f"\nPayment amount: ${amount:.2f}")
    card = input('Enter credit card number (dummy): ').strip()
    if card:
        print('Payment processed successfully!')
        return True
    print('Payment failed.')
    return False


def main():
    catalog = GiftCatalog.from_file('gifts.json')
    req = prompt_customer_requirements()
    suggestions = catalog.suggest(req['occasion'], req['age'], req['gender'])
    gift = choose_gift(suggestions)
    if not gift:
        return
    shipping = collect_shipping_info()
    if not process_payment(gift.price):
        print('Order not completed.')
        return
    print('\nOrder confirmation:')
    print(f"Gift: {gift.name}")
    print(f"Send to: {shipping['name']}, {shipping['address']}")
    print('Thank you for your purchase!')


if __name__ == '__main__':
    main()
gifts.json
New
+52
-0

[
  {
    "id": 1,
    "name": "Bouquet of Flowers",
    "occasions": ["birthday", "anniversary", "congratulations"],
    "age_min": 18,
    "age_max": 80,
    "genders": ["female", "male", "other"],
    "price": 29.99,
    "description": "Fresh flower arrangement"
  },
  {
    "id": 2,
    "name": "Box of Chocolates",
    "occasions": ["birthday", "valentine", "anniversary"],
    "age_min": 5,
    "age_max": 99,
    "genders": ["female", "male", "other"],
    "price": 19.99,
    "description": "Assorted chocolates in a gift box"
  },
  {
    "id": 3,
    "name": "Toy Car",
    "occasions": ["birthday"],
    "age_min": 3,
    "age_max": 12,
    "genders": ["male"],
    "price": 15.5,
    "description": "Remote controlled toy car"
  },
  {
    "id": 4,
    "name": "Spa Voucher",
    "occasions": ["birthday", "anniversary"],
    "age_min": 21,
    "age_max": 65,
    "genders": ["female", "other"],
    "price": 50.0,
    "description": "Relaxing day spa experience"
  },
  {
    "id": 5,
    "name": "Sports Watch",
    "occasions": ["birthday", "graduation"],
    "age_min": 16,
    "age_max": 45,
    "genders": ["male", "other"],
    "price": 100.0,
    "description": "Water-resistant digital watch"
  }
]
