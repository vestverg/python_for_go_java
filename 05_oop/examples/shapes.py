from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pi


@dataclass
class Shape(ABC):
    """Abstract base class for all shapes."""
    color: str

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass


@dataclass
class Circle(Shape):
    """Class representing a circle."""
    radius: float

    def area(self) -> float:
        return pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * pi * self.radius


@dataclass
class Rectangle(Shape):
    """Class representing a rectangle."""
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


def main():
    """Main function to demonstrate the shape classes."""
    circle = Circle(radius=10, color="red")
    rectangle = Rectangle(width=5, height=10, color="blue")

    print(f"Circle area: {circle.area()}")
    print(f"Circle perimeter: {circle.perimeter()}")
    print(f"Rectangle area: {rectangle.area()}")
    print(f"Rectangle perimeter: {rectangle.perimeter()}")


if __name__ == "__main__":
    main()