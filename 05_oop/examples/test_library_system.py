"""
Test suite for the library management system.

This module demonstrates testing OOP code with pytest, including:
1. Fixtures
2. Mocking
3. Parametrized tests
4. Exception testing
"""

import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from typing import Generator

from library_system import (
    Library,
    LibraryUser,
    Book,
    DVD,
    ItemStatus,
    LibraryLogger,
    EmailValidator
)


@pytest.fixture
def library() -> Library:
    """Fixture providing a library instance."""
    return Library("Test Library")


@pytest.fixture
def user() -> LibraryUser:
    """Fixture providing a library user."""
    return LibraryUser(
        name="Test User",
        email="test@example.com",
        phone="123-456-7890"
    )


@pytest.fixture
def book() -> Book:
    """Fixture providing a book."""
    return Book(
        title="Test Book",
        item_id="B001",
        location="Test Location",
        author="Test Author",
        isbn="123-456-789",
        pages=200,
        publisher="Test Publisher",
        year=2023
    )


@pytest.fixture
def dvd() -> DVD:
    """Fixture providing a DVD."""
    return DVD(
        title="Test DVD",
        item_id="D001",
        location="Test Location",
        director="Test Director",
        runtime=120,
        rating="PG"
    )


@pytest.fixture
def temp_log_file(tmp_path) -> Generator[str, None, None]:
    """Fixture providing a temporary log file."""
    log_file = tmp_path / "test.log"
    yield str(log_file)
    if log_file.exists():
        os.unlink(str(log_file))


class TestLibraryUser:
    """Test cases for LibraryUser class."""
    
    def test_user_creation(self, user: LibraryUser) -> None:
        """Test user creation with valid data."""
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.phone == "123-456-7890"
        assert isinstance(user.library_card, str)
        assert user.library_card.startswith("LIB")
    
    @pytest.mark.parametrize("invalid_email", [
        "",
        "invalid",
        "invalid@",
        "@invalid",
        "invalid@invalid",
    ])
    def test_invalid_email(self, invalid_email: str) -> None:
        """Test user creation with invalid email."""
        with pytest.raises(ValueError):
            LibraryUser(
                name="Test User",
                email=invalid_email
            )
    
    def test_checked_out_items_default_empty(self, user: LibraryUser) -> None:
        """Test that checked out items is empty by default."""
        assert len(user.checked_out_items) == 0
    
    def test_reserved_items_default_empty(self, user: LibraryUser) -> None:
        """Test that reserved items is empty by default."""
        assert len(user.reserved_items) == 0


class TestLibraryItem:
    """Test cases for LibraryItem subclasses."""
    
    def test_book_loan_period(self, book: Book) -> None:
        """Test book loan period is 21 days."""
        assert book.get_loan_period() == timedelta(days=21)
    
    def test_dvd_loan_period(self, dvd: DVD) -> None:
        """Test DVD loan period is 7 days."""
        assert dvd.get_loan_period() == timedelta(days=7)
    
    def test_item_string_representation(self, book: Book) -> None:
        """Test string representation of library items."""
        assert str(book) == "Test Book (B001)"
    
    def test_item_initial_status(self, book: Book) -> None:
        """Test initial status of library items."""
        assert book.status == ItemStatus.AVAILABLE
        assert book.due_date is None


class TestLibrary:
    """Test cases for Library class."""
    
    def test_add_item(
        self,
        library: Library,
        book: Book
    ) -> None:
        """Test adding an item to the library."""
        library.add_item(book)
        assert book.item_id in library.items
        assert library.items[book.item_id] == book
    
    def test_register_user(
        self,
        library: Library,
        user: LibraryUser
    ) -> None:
        """Test registering a user."""
        library.register_user(user)
        assert user.library_card in library.users
        assert library.users[user.library_card] == user
    
    def test_check_out_item(
        self,
        library: Library,
        book: Book,
        user: LibraryUser
    ) -> None:
        """Test checking out an item."""
        library.add_item(book)
        library.register_user(user)
        
        success = library.check_out_item(book.item_id, user.library_card)
        assert success
        assert book.status == ItemStatus.CHECKED_OUT
        assert book.due_date is not None
        assert book in user.checked_out_items
    
    def test_return_item(
        self,
        library: Library,
        book: Book,
        user: LibraryUser
    ) -> None:
        """Test returning an item."""
        library.add_item(book)
        library.register_user(user)
        library.check_out_item(book.item_id, user.library_card)
        
        success = library.return_item(book.item_id)
        assert success
        assert book.status == ItemStatus.AVAILABLE
        assert book.due_date is None
        assert book not in user.checked_out_items
    
    def test_check_out_unavailable_item(
        self,
        library: Library,
        book: Book,
        user: LibraryUser
    ) -> None:
        """Test checking out an unavailable item."""
        library.add_item(book)
        library.register_user(user)
        book._status = ItemStatus.LOST
        
        success = library.check_out_item(book.item_id, user.library_card)
        assert not success
        assert book not in user.checked_out_items
    
    def test_return_unchecked_item(
        self,
        library: Library,
        book: Book
    ) -> None:
        """Test returning an item that wasn't checked out."""
        library.add_item(book)
        success = library.return_item(book.item_id)
        assert not success


class TestLibraryLogger:
    """Test cases for LibraryLogger class."""
    
    def test_logger_writes_to_file(
        self,
        temp_log_file: str,
        library: Library,
        book: Book
    ) -> None:
        """Test that logger writes events to file."""
        logger = LibraryLogger(temp_log_file)
        library.attach(logger)
        
        library.add_item(book)
        
        with open(temp_log_file, "r") as f:
            log_content = f.read()
        
        assert "New item added:" in log_content
        assert book.title in log_content
    
    def test_logger_format(
        self,
        temp_log_file: str
    ) -> None:
        """Test log message format."""
        logger = LibraryLogger(temp_log_file)
        test_message = "Test message"
        
        logger.update(test_message)
        
        with open(temp_log_file, "r") as f:
            log_content = f.read()
        
        assert "[" in log_content
        assert "]" in log_content
        assert test_message in log_content


class TestEmailValidator:
    """Test cases for EmailValidator descriptor."""
    
    def test_valid_email(self) -> None:
        """Test setting a valid email."""
        user = LibraryUser(
            name="Test",
            email="valid@example.com"
        )
        assert user.email == "valid@example.com"
    
    def test_email_lowercase(self) -> None:
        """Test email is converted to lowercase."""
        user = LibraryUser(
            name="Test",
            email="VALID@EXAMPLE.COM"
        )
        assert user.email == "valid@example.com"
    
    def test_invalid_email_type(self) -> None:
        """Test setting invalid email type."""
        with pytest.raises(TypeError):
            LibraryUser(name="Test", email=123)  # type: ignore
    
    @pytest.mark.parametrize("invalid_email,expected_error", [
        ("", ValueError),
        ("invalid", ValueError),
        ("invalid@", ValueError),
        ("@invalid", ValueError),
    ])
    def test_invalid_email_format(
        self,
        invalid_email: str,
        expected_error: type
    ) -> None:
        """Test setting invalid email format."""
        with pytest.raises(expected_error):
            LibraryUser(name="Test", email=invalid_email) 