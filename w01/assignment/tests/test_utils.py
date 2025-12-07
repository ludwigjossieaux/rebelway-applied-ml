import pytest
from library_management.utils import DataFormatter, IDGenerator


def test_print_json_structure_with_books(capsys):
    """
    Test that print_json_structure correctly prints book data.
    """
    # Arrange
    data = {
        "Books": {
            "ABC123": {
                "title": "Test Book",
                "author": "Test Author",
                "genre": "Fiction",
                "publication_year": 2020,
                "isbn": "123-456-789"
            },
            "XYZ789": {
                "title": "Another Book",
                "author": "Another Author",
                "genre": "Non-Fiction",
                "publication_year": 2021,
                "isbn": "987-654-321"
            }
        }
    }
    
    # Act
    DataFormatter.print_json_structure(data)
    
    # Assert
    captured = capsys.readouterr()
    output = captured.out
    
    # Verify first book is printed
    assert "ID: ABC123" in output
    assert "Title: Test Book" in output
    assert "Author: Test Author" in output
    assert "Genre: Fiction" in output
    assert "Year: 2020" in output
    assert "ISBN: 123-456-789" in output
    
    # Verify second book is printed
    assert "ID: XYZ789" in output
    assert "Title: Another Book" in output
    assert "Author: Another Author" in output
    assert "Genre: Non-Fiction" in output
    assert "Year: 2021" in output
    assert "ISBN: 987-654-321" in output


def test_print_json_structure_with_missing_fields(capsys):
    """
    Test that print_json_structure handles missing fields gracefully.
    """
    # Arrange
    data = {
        "Books": {
            "TEST123": {
                "title": "Incomplete Book",
                "author": "Some Author"
                # Missing genre, publication_year, and isbn
            }
        }
    }
    
    # Act
    DataFormatter.print_json_structure(data)
    
    # Assert
    captured = capsys.readouterr()
    output = captured.out
    
    assert "ID: TEST123" in output
    assert "Title: Incomplete Book" in output
    assert "Author: Some Author" in output
    assert "Genre: N/A" in output
    assert "Year: N/A" in output
    assert "ISBN: N/A" in output


def test_print_json_structure_with_empty_books(capsys):
    """
    Test that print_json_structure handles empty Books dictionary.
    """
    # Arrange
    data = {
        "Books": {}
    }
    
    # Act
    DataFormatter.print_json_structure(data)
    
    # Assert
    captured = capsys.readouterr()
    output = captured.out
    
    # Should not print anything (or just empty output)
    assert "ID:" not in output


def test_print_json_structure_without_books_key(capsys):
    """
    Test that print_json_structure handles data without Books key.
    """
    # Arrange
    data = {
        "OtherData": {
            "key": "value"
        }
    }
    
    # Act
    DataFormatter.print_json_structure(data)
    
    # Assert
    captured = capsys.readouterr()
    output = captured.out
    
    # Should not print anything when Books key is missing
    assert "ID:" not in output


def test_id_generator_generate_id():
    """
    Test that IDGenerator generates IDs of the correct length.
    """
    # Arrange
    expected_length = 8
    
    # Act
    generated_id = IDGenerator.generate_id()
    
    # Assert
    assert len(generated_id) == expected_length
    assert generated_id.isalnum()
    assert generated_id.isupper() or any(c.isdigit() for c in generated_id)


def test_id_generator_generate_id_custom_length():
    """
    Test that IDGenerator generates IDs with custom length.
    """
    # Arrange
    custom_length = 12
    
    # Act
    generated_id = IDGenerator.generate_id(length=custom_length)
    
    # Assert
    assert len(generated_id) == custom_length
    assert generated_id.isalnum()


def test_id_generator_generate_id_uniqueness():
    """
    Test that IDGenerator generates unique IDs.
    """
    # Arrange
    num_ids = 100
    
    # Act
    generated_ids = [IDGenerator.generate_id() for _ in range(num_ids)]
    
    # Assert
    # All IDs should be unique
    assert len(generated_ids) == len(set(generated_ids))


def test_id_generator_generate_id_characters():
    """
    Test that IDGenerator generates IDs with only uppercase letters and digits.
    """
    # Arrange
    # Act
    generated_id = IDGenerator.generate_id()
    
    # Assert
    assert all(c.isalnum() for c in generated_id)
    assert all(c.isupper() or c.isdigit() for c in generated_id)
    assert not any(c.islower() for c in generated_id)

