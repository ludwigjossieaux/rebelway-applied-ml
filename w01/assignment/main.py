from library_management.book_service import BookService
from library_management.book import Book


if __name__ == "__main__":
    # Initialize the book service with a database file
    database = "library_database.json"
    book_service = BookService(database_path=database)
    
    # Clear all books to start fresh
    book_service.clear_all_books()
    
    # Create some books (Create operation)
    print("=== Creating Books ===")
    book1 = Book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        genre="Fiction",
        publication_year=1925,
        isbn="978-0-7432-7356-5"
    )
    book_service.create_book(book1)
    
    book2 = Book(
        title="1984",
        author="George Orwell",
        genre="Dystopian Fiction",
        publication_year=1949,
        isbn="978-0-452-28423-4"
    )
    book_service.create_book(book2)
    
    book3 = Book(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        genre="Fiction",
        publication_year=1960,
        isbn="978-0-06-112008-4"
    )
    book_service.create_book(book3)
    
    book4 = Book(
        title="Pride and Prejudice",
        author="Jane Austen",
        genre="Romance",
        publication_year=1813,
        isbn="978-0-14-143951-8"
    )
    book_service.create_book(book4)
    
    # Read all books (Read operation)
    print("\n=== Reading All Books ===")
    book_service.read_all_books(verbose=True)
    
    # Read a specific book
    print("\n=== Reading a Specific Book ===")
    if book1._id:
        found_book = book_service.read_book(book1._id)
        if found_book:
            print(f"Found: {found_book.title} by {found_book.author}")
    
    # Update a book (Update operation)
    print("\n=== Updating a Book ===")
    if book2._id:
        updated_book = book_service.update_book(
            book2._id,
            genre="Science Fiction"
        )
        if updated_book:
            print(f"Updated genre to: {updated_book.genre}")
    
    # Search operations
    print("\n=== Searching Books ===")
    
    # General search
    print("\nSearching for 'Fitzgerald'...")
    results = book_service.search_books("Fitzgerald")
    for book in results:
        print(f"  - {book.title} by {book.author}")
    
    # Search by title
    print("\nSearching by title '1984'...")
    results = book_service.search_books_by_title("1984")
    for book in results:
        print(f"  - {book.title} by {book.author}")
    
    # Search by author
    print("\nSearching by author 'Austen'...")
    results = book_service.search_books_by_author("Austen")
    for book in results:
        print(f"  - {book.title} by {book.author}")
    
    # Search by genre
    print("\nSearching by genre 'Fiction'...")
    results = book_service.search_books_by_genre("Fiction")
    for book in results:
        print(f"  - {book.title} by {book.author}")
    
    # Search by year range
    print("\nSearching books published between 1900 and 1950...")
    results = book_service.search_books_by_year_range(1900, 1950)
    for book in results:
        print(f"  - {book.title} ({book.publication_year})")
    
    # Search by ISBN
    print("\nSearching by ISBN...")
    found_book = book_service.search_books_by_isbn("978-0-06-112008-4")
    if found_book:
        print(f"  - Found: {found_book.title} by {found_book.author}")
    
    # Get total count
    print(f"\n=== Total Books in Library: {book_service.get_total_book_count()} ===")
    
    # Delete a book (Delete operation)
    print("\n=== Deleting a Book ===")
    if book3._id:
        book_service.delete_book(book3._id)
    
    # Final state
    print("\n=== Final Library State ===")
    book_service.read_all_books(verbose=True)
    print(f"Total books: {book_service.get_total_book_count()}")

