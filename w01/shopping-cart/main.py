from shopping_cart.cart import Cart
from shopping_cart.item import Item

if __name__ == "__main__":
    database = "shopping_cart.json"
    my_cart = Cart(database_path=database)

    # clean all items
    my_cart.empty_cart()

    # init database with fruits
    my_cart.add_item_to_cart(Item(name="Apple", type="Fruit", _price=1.0))
    my_cart.add_item_to_cart(Item(name="Banana", type="Fruit", _price=2.0))
    my_cart.add_item_to_cart(Item(name="Cherry", type="Fruit", _price=3.0))

    # search for an item
    print("Searching for 'apple'...")
    my_cart.search_items("apple")
    
    # get the total amount of the items in the cart
    print("Total amount of items in the cart: ", my_cart.get_total_item_count())

    # create more items 
    my_cart.add_item_to_cart(Item(name="Milk", type="Drink", _price=4.0))
    my_cart.add_item_to_cart(Item(name="Onion", type="Vegetable", _price=5.0))

    # print all the items in the cart
    my_cart.get_all_items(verbose=1)

    # remove the milk
    my_cart.remove_item_from_cart("milk")

    # prompt selection for removing an item
    my_cart.remove_items_from_cart_by_selection()

    # now all the items in the cart
    my_cart.get_all_items(verbose=1)

    # total price of the items in the cart
    print("Total price of the items in the cart: ", my_cart.get_total_price_of_items())



