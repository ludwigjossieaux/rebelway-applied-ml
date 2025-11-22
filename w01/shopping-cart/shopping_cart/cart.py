import json
from dataclasses import dataclass, field
from shopping_cart.item import Item
from shopping_cart.file_io import FStream
from shopping_cart.random_number_utils import RandomNumberUtils

@dataclass
class Cart:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(default_factory=RandomNumberUtils.generate_random_id)

    def get_all_items(self, verbose=0) -> dict:
        """
        Reads and returns a hash map of all the available items

        Args:
            if verbose is 1, it will print the hash map of the items

        Returns:
            dict: A hash map with the items
        """
        data_file = FStream.load_json_file(self.database_path)

        # Convert Items from list to dict if needed (for backward compatibility)
        if isinstance(data_file.get("Items"), list):
            data_file["Items"] = {}

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                FStream.print_json_structure(data_file)
            
            return data_file
        except:
            raise ValueError("The value for the verbose has to be 0 or 1")


    def search_items(self, query: str) -> list[Item]:
        """
        Searches for items in the database based on the query
        
        Args:
            query: The query to search for
        Returns:
            list[Item]: A list of items that match the query
        """
        data_file = FStream.load_json_file(self.database_path)
        results = []
        for item_id, item_data in data_file["Items"].items():
            item = Item(name=item_data["name"], type=item_data["type"], _price=item_data["price"], _id=item_id)
            if query.lower() in item.search_string.lower():
                results.append(item)

        if len(results) == 0:
            print("No items found matching the query")
        else:
            for item in results:
                print(f"Found item: {item.name} {item.type} {item.price}")
        
        return results

    def get_total_item_count(self) -> int:
        """
        Returns the total number of items in the cart

        Returns:
            int: The total number of items in the cart
        """
        data_file = self.get_all_items()
        return len(data_file["Items"].items())

    def add_item_to_cart(self, item: Item):
        """
        Adds an item to the cart

        Args:
            item (Item): The item to add to the cart
        """
        data = self.get_all_items()
        new_item = {"name": item.name, "type": item.type, "price": item.price}
        data["Items"][item._id] = new_item

        with open(self.database_path, 'w') as data_file:
            json.dump(data, data_file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added item {item.name} to the cart")

    def remove_item_from_cart(self, query: str):
        """
        Removes all the instances of an item from the cart

        Args:
            query (str): The query to remove the item from the cart
        """
        data = self.get_all_items()
        items_to_remove = []

        for item_id, item_data in data["Items"].items():
            if query.lower() in item_data["name"].lower() or query.lower() in item_data["type"].lower():
                items_to_remove.append(item_id)

        if not items_to_remove:
            print(f"No items found matching the query matching '{query}'")
            return

        for item_id in items_to_remove:
            item_name = data["Items"][item_id]["name"]
            del data["Items"][item_id]
            print(f"Removed item {item_name} from the cart")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

        print(f"Removed all items matching the query '{query}' from the cart")

    def remove_items_from_cart_by_selection(self):
        """
        Remove the selected item by index
        """

        data = self.get_all_items()
        items = []
        i = 0
        for item_id, item_data in data["Items"].items():
            items.append(item_id)
            print(f"{i}: {item_data}")
            i += 1
        try:
            usr_choice = int(input("Enter the index of the item to remove: "))
        except:
            raise ValueError("The input is not a valid index")

        if usr_choice > len(items):
            print("Item not found")
            return

        item_to_remove = items[usr_choice]
        item_name = data["Items"][item_to_remove]["name"]
        del data["Items"][item_to_remove]
        print(f"Removed item {item_name} from the cart")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def get_total_price_of_items(self) -> float:
        """
        Returns the total price of the items in the cart

        Returns:
            float: The total price of the items in the cart
        """
        data = self.get_all_items()
        total = 0.0
        for item_id, item_data in data["Items"].items():
            total += item_data["price"]
        return total

    def empty_cart(self):
        """
        Clear all the items from the cart
        """
        data = self.get_all_items()
        if len(data["Items"].items()) > 0:
            data = {"Items": {}}
            with open(self.database_path, 'w') as file:
                json.dump(data, file, indent=4)
            self.isEmpty = True
            self.isActive = False
            print("Cart emptied")
        else:
            print("Cart is already empty")


# @dataclass
# class Cart:
#     _items: list[Item] = field(default_factory=list)
#     _total: float = 0.0

#     @property
#     def total(self) -> float:
#         return round(self._total, 2)

#     def add_item(self, item: Item):