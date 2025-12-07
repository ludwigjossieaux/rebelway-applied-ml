import pytest
from library_management.book import Book


def test_book_creation():
    """
    Test that a book can be created with all required fields.
    """
    # Arrange
    title = "Test Book"
    author = "Test Author"
    genre = "Fiction"
    year = 2020
    isbn = "123-456-789"
    
    # Act
    book = Book(title=title, author=author, genre=genre, 
                publication_year=year, isbn=isbn)
    
    # Assert
    assert book.title == title
    assert book.author == author
    assert book.genre == genre
    assert book.publication_year == year
    assert book.isbn == isbn
    assert book._id is not None
    assert len(book._id) > 0


def test_book_search_string():
    """
    Test that the search_string property includes all searchable fields.
    """
    # Arrange
    book = Book(
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        publication_year=2020,
        isbn="123-456-789"
    )
    
    # Act
    search_string = book.search_string
    
    # Assert
    assert "test book" in search_string
    assert "test author" in search_string
    assert "fiction" in search_string
    assert "123-456-789" in search_string


def test_book_immutability():
    """
    Test that Book objects are immutable (frozen dataclass).
    """
    # Arrange
    book = Book(title="Test", author="Author", genre="Genre")
    
    # Act & Assert
    with pytest.raises(Exception):  
        book.title = "New Title" # will raise a dataclass.FrozenInstanceError

