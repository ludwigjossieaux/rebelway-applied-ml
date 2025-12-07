from typing import List, Optional, Dict, Any
from library_management.book import Book
from library_management.file_io import FileIO
from library_management.utils import DataFormatter


class BookService:

    def __init__(self, database_path: str):
        """
        Initialize the BookService with a database file path.
        
        Args:
            database_path: Path to the JSON file storing book data
        """
        self.database_path = database_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self) -> None:
        """
        Ensure the database file exists with proper structure.
        Private method following encapsulation principles.
        """
        try:
            data = FileIO.load_json_file(self.database_path)
            # Ensure backward compatibility - convert list to dict if needed
            if isinstance(data.get("Books"), list):
                data["Books"] = {}
                FileIO.save_json_file(self.database_path, data)
        except Exception:
            # Create new database if it doesn't exist or is corrupted
            FileIO.save_json_file(self.database_path, {"Books": {}})
    
    def create_book(self, book: Book) -> Book:
        """
        Create a new book in the library (Create operation).
        
        Args:
            book: Book object to add to the library
        
        Returns:
            Book: The created book with its generated ID
        
        Raises:
            ValueError: If book with same ID already exists
        """
        data = FileIO.load_json_file(self.database_path)
        
        # Check if book already exists
        if book._id in data.get("Books", {}):
            raise ValueError(f"Book with ID {book._id} already exists")
        
        # Add book to database
        book_data = {
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "publication_year": book.publication_year,
            "isbn": book.isbn
        }
        
        data.setdefault("Books", {})[book._id] = book_data
        FileIO.save_json_file(self.database_path, data)
        
        print(f"Created book: {book.title} by {book.author}")
        return book
    
    def read_book(self, book_id: str) -> Optional[Book]:
        """
        Read a book by its ID (Read operation).
        
        Args:
            book_id: Unique identifier of the book
        
        Returns:
            Optional[Book]: Book object if found, None otherwise
        """
        data = FileIO.load_json_file(self.database_path)
        book_data = data.get("Books", {}).get(book_id)
        
        if not book_data:
            return None
        
        return Book(
            title=book_data["title"],
            author=book_data["author"],
            genre=book_data["genre"],
            publication_year=book_data.get("publication_year", 0),
            isbn=book_data.get("isbn", ""),
            _id=book_id
        )
    
    def read_all_books(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Read all books from the library.
        
        Args:
            verbose: If True, print all books to console
        
        Returns:
            dict: Dictionary containing all books
        """
        data = FileIO.load_json_file(self.database_path)
        
        if verbose:
            DataFormatter.print_json_structure(data)
        
        return data
    
    def update_book(self, book_id: str, **kwargs) -> Optional[Book]:
        """
        Update a book's information (Update operation).
        
        Args:
            book_id: Unique identifier of the book to update
            **kwargs: Fields to update (title, author, genre, publication_year, isbn)
        
        Returns:
            Optional[Book]: Updated Book object if found, None otherwise
        
        Raises:
            ValueError: If no valid fields are provided for update
        """
        data = FileIO.load_json_file(self.database_path)
        
        if book_id not in data.get("Books", {}):
            print(f"Book with ID {book_id} not found")
            return None
        
        # Valid fields that can be updated
        valid_fields = {"title", "author", "genre", "publication_year", "isbn"}
        update_fields = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not update_fields:
            raise ValueError("No valid fields provided for update")
        
        # Update the book data
        book_data = data["Books"][book_id]
        book_data.update(update_fields)
        
        FileIO.save_json_file(self.database_path, data)
        
        # Return updated book object
        updated_book = Book(
            title=book_data["title"],
            author=book_data["author"],
            genre=book_data["genre"],
            publication_year=book_data.get("publication_year", 0),
            isbn=book_data.get("isbn", ""),
            _id=book_id
        )
        
        print(f"Updated book: {updated_book.title}")
        return updated_book
    
    def delete_book(self, book_id: str) -> bool:
        """
        Delete a book from the library (Delete operation).
        
        Args:
            book_id: Unique identifier of the book to delete
        
        Returns:
            bool: True if book was deleted, False if not found
        """
        data = FileIO.load_json_file(self.database_path)
        
        if book_id not in data.get("Books", {}):
            print(f"Book with ID {book_id} not found")
            return False
        
        book_title = data["Books"][book_id]["title"]
        del data["Books"][book_id]
        
        FileIO.save_json_file(self.database_path, data)
        
        print(f"Deleted book: {book_title}")
        return True
    
    def search_books_by_title(self, query: str) -> List[Book]:
        """
        Search for books by title (case-insensitive partial match).
        
        Args:
            query: Search query to match against book titles
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(lambda book: query.lower() in book.title.lower())
    
    def search_books_by_author(self, query: str) -> List[Book]:
        """
        Search for books by author (case-insensitive partial match).
        
        Args:
            query: Search query to match against book authors
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(lambda book: query.lower() in book.author.lower())
    
    def search_books_by_genre(self, query: str) -> List[Book]:
        """
        Search for books by genre (case-insensitive partial match).
        
        Args:
            query: Search query to match against book genres
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(lambda book: query.lower() in book.genre.lower())
    
    def search_books_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Search for a book by ISBN (exact match).
        
        Args:
            isbn: ISBN to search for
        
        Returns:
            Optional[Book]: Book object if found, None otherwise
        """
        data = FileIO.load_json_file(self.database_path)
        
        for book_id, book_data in data.get("Books", {}).items():
            if book_data.get("isbn", "").lower() == isbn.lower():
                return Book(
                    title=book_data["title"],
                    author=book_data["author"],
                    genre=book_data["genre"],
                    publication_year=book_data.get("publication_year", 0),
                    isbn=book_data.get("isbn", ""),
                    _id=book_id
                )
        
        return None
    
    def search_books(self, query: str) -> List[Book]:
        """
        General search across all book fields (title, author, genre, ISBN).
        
        Args:
            query: Search query to match against all searchable fields
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(lambda book: query.lower() in book.search_string)
    
    def search_books_by_year(self, year: int) -> List[Book]:
        """
        Search for books by publication year (exact match).
        
        Args:
            year: Publication year to search for
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(lambda book: book.publication_year == year)
    
    def search_books_by_year_range(self, start_year: int, end_year: int) -> List[Book]:
        """
        Search for books published within a year range.
        
        Args:
            start_year: Start of the year range (inclusive)
            end_year: End of the year range (inclusive)
        
        Returns:
            List[Book]: List of matching Book objects
        """
        return self._search_books(
            lambda book: start_year <= book.publication_year <= end_year
        )
    
    def _search_books(self, predicate) -> List[Book]:
        """
        Internal method for searching books using a predicate function.
        
        Args:
            predicate: Function that takes a Book and returns bool
        
        Returns:
            List[Book]: List of matching Book objects
        """
        data = FileIO.load_json_file(self.database_path)
        results = []
        
        for book_id, book_data in data.get("Books", {}).items():
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                genre=book_data["genre"],
                publication_year=book_data.get("publication_year", 0),
                isbn=book_data.get("isbn", ""),
                _id=book_id
            )
            
            if predicate(book):
                results.append(book)
        
        return results
    
    def get_total_book_count(self) -> int:
        """
        Get the total number of books in the library.
        
        Returns:
            int: Total number of books
        """
        data = FileIO.load_json_file(self.database_path)
        return len(data.get("Books", {}))
    
    def clear_all_books(self) -> None:
        """
        Clear all books from the library.
        """
        FileIO.save_json_file(self.database_path, {"Books": {}})
        print("All books cleared from library")

