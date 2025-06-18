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


class LibraryItem(ABC):
    """Abstract base class for all library items."""
    
    def __init__(
        self,
        title: str,
        item_id: str,
        location: str
    ) -> None:
        self.title = title
        self.item_id = item_id
        self.location = location
        self._status = ItemStatus.AVAILABLE
        self._due_date: Optional[datetime] = None
    
    @property
    def status(self) -> ItemStatus:
        return self._status
    
    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date
    
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
        item_id: str,
        location: str,
        author: str,
        isbn: str,
        pages: int,
        publisher: str,
        year: int
    ) -> None:
        super().__init__(title, item_id, location)
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self.publisher = publisher
        self.year = year
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=21)  # 3 weeks


class DVD(LibraryItem):
    """Represents a DVD in the library."""
    
    def __init__(
        self,
        title: str,
        item_id: str,
        location: str,
        director: str,
        runtime: int,
        rating: str
    ) -> None:
        super().__init__(title, item_id, location)
        self.director = director
        self.runtime = runtime  # in minutes
        self.rating = rating
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=7)  # 1 week


class Searchable(Protocol):
    """Protocol for searchable items."""
    def matches(self, query: str) -> bool: ...


class Reservable(Protocol):
    """Protocol for items that can be reserved."""
    def reserve(self, user: 'LibraryUser') -> bool: ...
    def cancel_reservation(self, user: 'LibraryUser') -> bool: ...


@dataclass
class LibraryUser(Person):
    """Represents a library user."""
    email: str = field(default="")  # Type hint for the descriptor
    library_card: str = field(default_factory=lambda: f"LIB{datetime.now().timestamp():.0f}")
    checked_out_items: List[LibraryItem] = field(default_factory=list)
    reserved_items: Set[LibraryItem] = field(default_factory=set)
    fines: float = field(default=0.0)
    
    # Email descriptor
    email_validator = EmailValidator()


class Observable(ABC):
    """Base class for objects that can be observed."""
    
    def __init__(self) -> None:
        self._observers: Set[Observer] = set()
    
    def attach(self, observer: 'Observer') -> None:
        self._observers.add(observer)
    
    def detach(self, observer: 'Observer') -> None:
        self._observers.discard(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class Observer(Protocol):
    """Protocol for observer objects."""
    def update(self, message: str) -> None: ...


class Library(Observable):
    """Main library class implementing the Observer pattern."""
    
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.items: Dict[str, LibraryItem] = {}
        self.users: Dict[str, LibraryUser] = {}
    
    def add_item(self, item: LibraryItem) -> None:
        """Add a new item to the library."""
        self.items[item.item_id] = item
        self.notify(f"New item added: {item}")
    
    def register_user(self, user: LibraryUser) -> None:
        """Register a new library user."""
        self.users[user.library_card] = user
        self.notify(f"New user registered: {user.name}")
    
    def check_out_item(
        self,
        item_id: str,
        user_card: str
    ) -> bool:
        """Check out an item to a user."""
        if item_id not in self.items or user_card not in self.users:
            return False
        
        item = self.items[item_id]
        user = self.users[user_card]
        
        if item.status != ItemStatus.AVAILABLE:
            return False
        
        item._status = ItemStatus.CHECKED_OUT
        item._due_date = datetime.now() + item.get_loan_period()
        user.checked_out_items.append(item)
        
        self.notify(f"{item} checked out to {user.name}")
        return True
    
    def return_item(self, item_id: str) -> bool:
        """Return an item to the library."""
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        if item.status != ItemStatus.CHECKED_OUT:
            return False
        
        # Find user who has this item
        for user in self.users.values():
            if item in user.checked_out_items:
                user.checked_out_items.remove(item)
                break
        
        item._status = ItemStatus.AVAILABLE
        item._due_date = None
        
        self.notify(f"{item} returned to library")
        return True


class LibraryLogger(Observer):
    """Observer that logs library events."""
    
    def __init__(self, log_file: str) -> None:
        self.log_file = log_file
    
    def update(self, message: str) -> None:
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")


def main() -> None:
    """Example usage of the library system."""
    # Create library and logger
    library = Library("Community Library")
    logger = LibraryLogger("library.log")
    library.attach(logger)
    
    # Create some books and DVDs
    book1 = Book(
        title="Python Programming",
        item_id="B001",
        location="Floor 1, Section A",
        author="John Smith",
        isbn="123-456-789",
        pages=300,
        publisher="Tech Books",
        year=2023
    )
    
    dvd1 = DVD(
        title="Python Tutorial Series",
        item_id="D001",
        location="Floor 2, Section B",
        director="Jane Doe",
        runtime=180,
        rating="E"
    )
    
    # Add items to library
    library.add_item(book1)
    library.add_item(dvd1)
    
    # Register a user
    user = LibraryUser(
        name="Alice Johnson",
        email="alice@example.com",
        phone="123-456-7890"
    )
    library.register_user(user)
    
    # Check out and return items
    library.check_out_item(book1.item_id, user.library_card)
    library.return_item(book1.item_id)


if __name__ == "__main__":
    main() 