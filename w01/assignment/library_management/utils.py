import random
import string
from typing import Dict, Any


class IDGenerator:
    """
    Utility class for generating unique identifiers.
    """
    
    @staticmethod
    def generate_id(length: int = 8) -> str:
        """
        Generate a random alphanumeric ID.
        
        Args:
            length: Length of the ID to generate (default: 8)
        
        Returns:
            str: A random alphanumeric string of specified length
        """
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))


class DataFormatter:
    """
    Utility class for formatting and displaying data.
    """
    
    @staticmethod
    def print_json_structure(data: Dict[str, Any]) -> None:
        """
        Pretty print the JSON structure for display.
        
        Args:
            data: Dictionary data to print
        """
        if "Books" in data:
            for book_id, book_data in data["Books"].items():
                print(f"ID: {book_id}")
                print(f"  Title: {book_data.get('title', 'N/A')}")
                print(f"  Author: {book_data.get('author', 'N/A')}")
                print(f"  Genre: {book_data.get('genre', 'N/A')}")
                print(f"  Year: {book_data.get('publication_year', 'N/A')}")
                print(f"  ISBN: {book_data.get('isbn', 'N/A')}")
                print()

