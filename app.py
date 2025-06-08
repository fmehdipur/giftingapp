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
