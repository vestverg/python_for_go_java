"""
Library Management System Example

This example demonstrates various OOP concepts in Python:
1. Abstract Base Classes
2. Multiple Inheritance
3. Properties and Descriptors
4. Special Methods
5. Data Classes
6. Type Hints and Protocols
7. Design Patterns
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Protocol, Set, Dict
from enum import Enum, auto
import uuid


class ItemStatus(Enum):
    """Status of library items."""
    AVAILABLE = auto()
    CHECKED_OUT = auto()
    RESERVED = auto()
    LOST = auto()


@dataclass
class Person:
    """Base class for library users and staff."""
    name: str
    email: str
    phone: Optional[str] = None


class EmailValidator:
    """Descriptor for email validation."""
    
    def __init__(self) -> None:
        self.name = ""  # Will be set by __set_name__
    
    def __get__(
        self,
        instance: Optional[object],
        owner: Optional[type] = None
    ) -> Optional[str]:
        if instance is None:
            return None
        return getattr(instance, f"_{self.name}", None)
    
    def __set__(self, instance: object, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        setattr(instance, f"_{self.name}", value.lower())
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Observer(Protocol):
    """Protocol for observer objects."""
    def update(self, message: str) -> None: ...


class Observable:
    """Base class for objects that can be observed."""
    
    def __init__(self) -> None:
        self._observers: Set[Observer] = set()
    
    def add_observer(self, observer: 'Observer') -> None:
        self._observers.add(observer)
    
    def detach(self, observer: 'Observer') -> None:
        self._observers.discard(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class LibraryItem(ABC, Observable):
    """Abstract base class for all library items."""
    
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
        self.item_id = str(uuid.uuid4())

    @abstractmethod
    def get_loan_period(self) -> timedelta:
        """Return the loan period for this item."""
        pass

    def __str__(self) -> str:
        return f"{self.title} ({self.item_id})"


class Book(LibraryItem):
    """Represents a book in the library."""
    
    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        pages: int,
        publisher: str,
        year: int
    ) -> None:
        super().__init__(title)
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self.publisher = publisher
        self.year = year
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=14)


class DVD(LibraryItem):
    """Represents a DVD in the library."""
    
    def __init__(
        self,
        title: str,
        director: str,
        runtime: int,
        rating: str
    ) -> None:
        super().__init__(title)
        self.director = director
        self.runtime = runtime
        self.rating = rating
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=7)


class Searchable(Protocol):
    """Protocol for searchable items."""
    def matches(self, query: str) -> bool: ...


class Reservable(Protocol):
    """Protocol for items that can be reserved."""
    def reserve(self, user: 'LibraryUser') -> bool: ...
    def cancel_reservation(self, user: 'LibraryUser') -> bool: ...


@dataclass
class LibraryUser:
    """Represents a library user."""
    name: str
    email: str
    user_id: str
    borrowed_items: List[LibraryItem] = field(default_factory=list)


class Library(Observable):
    """Main library class implementing the Observer pattern."""
    
    def __init__(self) -> None:
        super().__init__()
        self.items: Dict[str, LibraryItem] = {}
    
    def add_item(self, item: LibraryItem) -> None:
        """Add a new item to the library."""
        self.items[item.item_id] = item
        self.notify(f"New item added: {item}")
    
    def remove_item(self, item_id: str) -> None:
        """Remove an item from the library."""
        if item_id in self.items:
            del self.items[item_id]
            self.notify(f"Item {item_id} removed.")

    def find_item(self, item_id: str) -> Optional[LibraryItem]:
        """Find an item by its ID."""
        return self.items.get(item_id)


class LibraryLogger:
    """A simple logger that observes the library."""
    
    def __init__(self) -> None:
        self.logs: List[str] = []
        
    def update(self, message: str) -> None:
        """Receives notification from the observable."""
        self.logs.append(f"[{datetime.now()}] {message}")


def main():
    """Main function to demonstrate the library system."""
    # Create a library
    library = Library()
    
    # Create a logger and attach it to the library
    logger = LibraryLogger()
    library.add_observer(logger)
    
    # Create some library items
    book = Book(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0-345-39180-2",
        pages=224,
        publisher="Pan Books",
        year=1979
    )
    
    dvd = DVD(
        title="The Princess Bride",
        director="Rob Reiner",
        runtime=98,
        rating="PG"
    )
    
    # Add items to the library
    library.add_item(book)
    library.add_item(dvd)
    
    # Create a library user
    user = LibraryUser(
        name="John Doe",
        email="johndoe@example.com",
        user_id="USER001"
    )
    
    # Print out the logs
    for log in logger.logs:
        print(log)


if __name__ == "__main__":
    main() 