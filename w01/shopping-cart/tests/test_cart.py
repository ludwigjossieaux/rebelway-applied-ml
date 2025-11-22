import pytest
from shopping_cart.cart import Cart
from shopping_cart.item import Item

@pytest.fixture
def cart():
    database= "./tests/test_database.json"
    cart = Cart(database_path=database)
    cart.empty_cart()
    return cart

def test_total_price_of_cart(cart):
    item1 = Item(name="Apple", type="Fruit", _price=1.0)
    item2 = Item(name="Pineapple", type="Fruit", _price=2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    assert cart.get_total_price_of_items() == 3.0

def test_empty_cart(cart):
    item = Item(name="Apple", type="Fruit", _price=1.0)
    cart.add_item_to_cart(item)
    cart.empty_cart()
    assert len(cart.get_all_items()["Items"].items()) == 0

def test_search_item(cart):
    item = Item(name="Tomato", type="Vegetable", _price=1.0)
    cart.add_item_to_cart(item)
    items_list = cart.search_items("Tomato")
    assert items_list[0].name == "Tomato"

def test_get_all_items(cart):
    item1 = Item(name="Apple", type="Fruit", _price=1.0)
    item2 = Item(name="Pineapple", type="Fruit", _price=2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    items_list = cart.get_all_items()
    print(items_list)
    assert len(items_list["Items"].items()) == 2
    # Convert dict_items to list and access the values (which are dicts)
    item_values = list(items_list["Items"].values())
    item_names = [item["name"] for item in item_values]
    assert "Apple" in item_names
    assert "Pineapple" in item_names

def test_get_total_item_count(cart):
    item1 = Item(name="Apple", type="Fruit", _price=1.0)
    item2 = Item(name="Pineapple", type="Fruit", _price=2.0)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    assert cart.get_total_item_count() == 2
    
