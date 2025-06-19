"""
Test module for OOP examples demonstrating Python's testing capabilities.
"""
import pytest
from typing import List, Dict, Any
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add the parent directory to the Python path to import OOP modules
sys.path.append(str(Path(__file__).parent.parent / "05_oop" / "examples"))
from library_system import (
    Book, DVD, Library, LibraryUser, LibraryLogger,
    LibraryItem, Observable, Observer
)
from shapes import Circle, Rectangle, Shape


class TestLibrarySystem:
    """Test suite for the library management system."""
    
    def test_book_creation(self) -> None:
        """Test book creation and properties."""
        book = Book(
            title="Python Programming",
            author="John Doe",
            isbn="123-456-789",
            pages=300,
            publisher="Tech Books",
            year=2023
        )
        
        assert book.title == "Python Programming"
        assert book.author == "John Doe"
        assert book.isbn == "123-456-789"
        assert book.pages == 300
        assert book.get_loan_period() == timedelta(days=14)
    
    def test_dvd_creation(self) -> None:
        """Test DVD creation and properties."""
        dvd = DVD(
            title="Python Tutorial",
            director="Jane Smith",
            runtime=120,
            rating="PG"
        )
        
        assert dvd.title == "Python Tutorial"
        assert dvd.director == "Jane Smith"
        assert dvd.runtime == 120
        assert dvd.rating == "PG"
        assert dvd.get_loan_period() == timedelta(days=7)
    
    def test_library_operations(self) -> None:
        """Test library add/remove operations."""
        library = Library()
        book = Book(
            title="Test Book",
            author="Test Author",
            isbn="111-222-333",
            pages=200,
            publisher="Test Pub",
            year=2023
        )
        
        # Test adding item
        library.add_item(book)
        assert len(library.items) == 1
        assert book.item_id in library.items
        
        # Test finding item
        found_item = library.find_item(book.item_id)
        assert found_item == book
        
        # Test removing item
        library.remove_item(book.item_id)
        assert len(library.items) == 0
    
    def test_library_user(self) -> None:
        """Test library user functionality."""
        user = LibraryUser(
            name="Test User",
            email="test@example.com",
            user_id="U001"
        )
        
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.user_id == "U001"
        assert len(user.borrowed_items) == 0
    
    def test_observer_pattern(self) -> None:
        """Test observer pattern implementation."""
        library = Library()
        logger = LibraryLogger()
        
        # Add observer
        library.add_observer(logger)
        
        # Create and add item (should trigger notification)
        book = Book(
            title="Observer Test",
            author="Test Author",
            isbn="999-888-777",
            pages=150,
            publisher="Test Pub",
            year=2023
        )
        library.add_item(book)
        
        # Verify observer was notified
        assert len(logger.logs) > 0


class TestShapes:
    """Test suite for the shapes examples."""
    
    def test_circle_creation(self) -> None:
        """Test circle creation and calculations."""
        circle = Circle(radius=5.0, color="red")
        
        assert circle.radius == 5.0
        assert circle.color == "red"
        assert abs(circle.area() - 78.54) < 0.01  # π * 5²
        assert abs(circle.perimeter() - 31.42) < 0.01  # 2 * π * 5
    
    def test_rectangle_creation(self) -> None:
        """Test rectangle creation and calculations."""
        rect = Rectangle(width=4.0, height=3.0, color="blue")
        
        assert rect.width == 4.0
        assert rect.height == 3.0
        assert rect.color == "blue"
        assert rect.area() == 12.0  # 4 * 3
        assert rect.perimeter() == 14.0  # 2 * (4 + 3)
    
    def test_shape_equality(self) -> None:
        """Test shape equality comparison."""
        circle1 = Circle(radius=5.0, color="red")
        circle2 = Circle(radius=5.0, color="red")
        circle3 = Circle(radius=3.0, color="red")
        
        assert circle1 == circle2  # Same radius and color
        assert circle1 != circle3  # Different radius
    
    def test_shape_string_representation(self) -> None:
        """Test shape string representations."""
        circle = Circle(radius=5.0, color="red")
        rect = Rectangle(width=4.0, height=3.0, color="blue")
        
        assert "Circle" in str(circle)
        assert "radius=5.0" in str(circle)
        assert "Rectangle" in str(rect)
        assert "width=4.0" in str(rect)


@pytest.fixture
def sample_library() -> Library:
    """Fixture to create a sample library with items."""
    library = Library()
    
    book = Book(
        title="Fixture Book",
        author="Fixture Author",
        isbn="111-111-111",
        pages=250,
        publisher="Fixture Pub",
        year=2023
    )
    
    dvd = DVD(
        title="Fixture DVD",
        director="Fixture Director",
        runtime=90,
        rating="G"
    )
    
    library.add_item(book)
    library.add_item(dvd)
    
    return library


def test_library_with_fixture(sample_library: Library) -> None:
    """Test library operations using fixture."""
    assert len(sample_library.items) == 2
    
    # Test search functionality
    books = [item for item in sample_library.items.values() if isinstance(item, Book)]
    dvds = [item for item in sample_library.items.values() if isinstance(item, DVD)]
    
    assert len(books) == 1
    assert len(dvds) == 1


if __name__ == "__main__":
    pytest.main([__file__]) 