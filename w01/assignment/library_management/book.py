"""
Book model representing a book in the library management system.

This module defines the Book dataclass which represents a book entity
with properties like title, author, ISBN, genre, and publication year.
"""

from dataclasses import dataclass, field
from library_management.utils import IDGenerator


@dataclass(frozen=True, order=True, slots=True)
class Book:
    """
    Immutable Book entity representing a book in the library.
    
    Attributes:
        title: The title of the book
        author: The author of the book
        isbn: International Standard Book Number (optional)
        genre: The genre/category of the book
        publication_year: Year the book was published
        _id: Unique identifier for the book (auto-generated)
    
    Properties:
        search_string: Combined searchable string for searching
    """
    title: str
    author: str
    genre: str
    publication_year: int = 0
    isbn: str = ""
    _id: str = field(default_factory=IDGenerator.generate_id)

    @property
    def search_string(self) -> str:
        """
        Returns a combined searchable string containing all searchable fields.
        
        Returns:
            str: Combined string of title, author, genre, and ISBN
        """
        return f"{self.title} {self.author} {self.genre} {self.isbn}".lower()

