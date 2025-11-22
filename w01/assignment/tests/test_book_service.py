import pytest
from library_management.book_service import BookService
from library_management.book import Book


@pytest.fixture
def book_service():
    """
    Fixture that provides a clean BookService instance for each test.
    """
    database = "./tests/test_library_database.json"
    service = BookService(database_path=database)
    service.clear_all_books()
    return service


@pytest.fixture
def sample_books():
    """
    Fixture that provides sample books for testing.
    """
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre="Fiction",
            publication_year=1925,
            isbn="978-0-7432-7356-5"
        ),
        Book(
            title="1984",
            author="George Orwell",
            genre="Dystopian Fiction",
            publication_year=1949,
            isbn="978-0-452-28423-4"
        ),
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Fiction",
            publication_year=1960,
            isbn="978-0-06-112008-4"
        ),
    ]


def test_create_book(book_service, sample_books):
    """
    Test creating a book (Create operation).
    """
    # Arrange
    book = sample_books[0]
    
    # Act
    created_book = book_service.create_book(book)
    
    # Assert
    assert created_book._id == book._id
    assert book_service.get_total_book_count() == 1
    retrieved_book = book_service.read_book(book._id)
    assert retrieved_book is not None
    assert retrieved_book.title == book.title


def test_create_duplicate_book(book_service, sample_books):
    """
    Test that creating a duplicate book raises an error.
    """
    # Arrange
    book = sample_books[0]
    book_service.create_book(book)
    
    # Act & Assert
    with pytest.raises(ValueError):
        book_service.create_book(book)


def test_read_book(book_service, sample_books):
    """
    Test reading a book by ID (Read operation).
    """
    # Arrange
    book = sample_books[0]
    book_service.create_book(book)
    
    # Act
    retrieved_book = book_service.read_book(book._id)
    
    # Assert
    assert retrieved_book is not None
    assert retrieved_book.title == book.title
    assert retrieved_book.author == book.author
    assert retrieved_book.genre == book.genre
    assert retrieved_book.publication_year == book.publication_year


def test_read_nonexistent_book(book_service):
    """
    Test reading a book that doesn't exist.
    """
    # Arrange
    nonexistent_id = "NONEXIST"
    
    # Act
    result = book_service.read_book(nonexistent_id)
    
    # Assert
    assert result is None


def test_read_all_books(book_service, sample_books):
    """
    Test reading all books from the library.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    all_books = book_service.read_all_books()
    
    # Assert
    assert len(all_books["Books"]) == len(sample_books)
    assert book_service.get_total_book_count() == len(sample_books)


def test_update_book(book_service, sample_books):
    """
    Test updating a book (Update operation).
    """
    # Arrange
    book = sample_books[0]
    book_service.create_book(book)
    new_genre = "Classic Fiction"
    
    # Act
    updated_book = book_service.update_book(book._id, genre=new_genre)
    
    # Assert
    assert updated_book is not None
    assert updated_book.genre == new_genre
    assert updated_book.title == book.title  # Other fields unchanged
    retrieved_book = book_service.read_book(book._id)
    assert retrieved_book.genre == new_genre


def test_update_nonexistent_book(book_service):
    """
    Test updating a book that doesn't exist.
    """
    # Arrange
    nonexistent_id = "NONEXIST"
    
    # Act
    result = book_service.update_book(nonexistent_id, title="New Title")
    
    # Assert
    assert result is None


def test_update_book_invalid_fields(book_service, sample_books):
    """
    Test that updating with invalid fields raises an error.
    """
    # Arrange
    book = sample_books[0]
    book_service.create_book(book)
    
    # Act & Assert
    with pytest.raises(ValueError):
        book_service.update_book(book._id, invalid_field="value")


def test_delete_book(book_service, sample_books):
    """
    Test deleting a book (Delete operation).
    """
    # Arrange
    book = sample_books[0]
    book_service.create_book(book)
    assert book_service.get_total_book_count() == 1
    
    # Act
    result = book_service.delete_book(book._id)
    
    # Assert
    assert result is True
    assert book_service.get_total_book_count() == 0
    assert book_service.read_book(book._id) is None


def test_delete_nonexistent_book(book_service):
    """
    Test deleting a book that doesn't exist.
    """
    # Arrange
    nonexistent_id = "NONEXIST"
    
    # Act
    result = book_service.delete_book(nonexistent_id)
    
    # Assert
    assert result is False


def test_search_books_general(book_service, sample_books):
    """
    Test general search across all fields.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books("Fitzgerald")
    
    # Assert
    assert len(results) == 1
    assert results[0].author == "F. Scott Fitzgerald"


def test_search_books_by_title(book_service, sample_books):
    """
    Test searching books by title.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books_by_title("1984")
    
    # Assert
    assert len(results) == 1
    assert results[0].title == "1984"


def test_search_books_by_author(book_service, sample_books):
    """
    Test searching books by author.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books_by_author("Orwell")
    
    # Assert
    assert len(results) == 1
    assert results[0].author == "George Orwell"


def test_search_books_by_genre(book_service, sample_books):
    """
    Test searching books by genre.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books_by_genre("Fiction")
    
    # Assert
    assert len(results) == 3
    titles = [book.title for book in results]
    assert "The Great Gatsby" in titles
    assert "1984" in titles  # Has "Dystopian Fiction"
    assert "To Kill a Mockingbird" in titles


def test_search_books_by_isbn(book_service, sample_books):
    """
    Test searching books by ISBN.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    result = book_service.search_books_by_isbn("978-0-452-28423-4")
    
    # Assert
    assert result is not None
    assert result.title == "1984"


def test_search_books_by_isbn_not_found(book_service, sample_books):
    """
    Test searching by ISBN when book doesn't exist.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    result = book_service.search_books_by_isbn("000-000-000-0")
    
    # Assert
    assert result is None


def test_search_books_by_year(book_service, sample_books):
    """
    Test searching books by publication year.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books_by_year(1949)
    
    # Assert
    assert len(results) == 1
    assert results[0].title == "1984"


def test_search_books_by_year_range(book_service, sample_books):
    """
    Test searching books by year range.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    
    # Act
    results = book_service.search_books_by_year_range(1940, 1970)
    
    # Assert
    assert len(results) == 2
    years = [book.publication_year for book in results]
    assert 1949 in years
    assert 1960 in years


def test_get_total_book_count(book_service, sample_books):
    """
    Test getting the total count of books.
    """
    # Arrange
    # Act
    for book in sample_books:
        book_service.create_book(book)
    
    # Assert
    assert book_service.get_total_book_count() == len(sample_books)


def test_clear_all_books(book_service, sample_books):
    """
    Test clearing all books from the library.
    """
    # Arrange
    for book in sample_books:
        book_service.create_book(book)
    assert book_service.get_total_book_count() == len(sample_books)
    
    # Act
    book_service.clear_all_books()
    
    # Assert
    assert book_service.get_total_book_count() == 0

