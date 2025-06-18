#!/usr/bin/env python3

"""
Geometric Shapes Example

This example demonstrates inheritance and composition in Python through geometric shapes.
It shows how to use abstract classes, protocols, and mixins to create a flexible
and extensible shape hierarchy.

Key concepts demonstrated:
1. Abstract Base Classes
2. Multiple Inheritance
3. Mixins
4. Protocols
5. Properties and Descriptors
6. Type Hints
7. Data Classes
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pi, sqrt
from typing import Protocol, List, Optional, Tuple, TypeVar, Generic


class Drawable(Protocol):
    """Protocol for objects that can be drawn."""
    def draw(self) -> str: ...


class Movable(Protocol):
    """Protocol for objects that can be moved."""
    def move(self, dx: float, dy: float) -> None: ...


class ColorMixin:
    """Mixin class providing color functionality."""
    
    def __init__(self, color: str = "black") -> None:
        self._color = color
    
    @property
    def color(self) -> str:
        """Get the color."""
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        """Set the color."""
        self._color = value.lower()


class Position:
    """Class representing a 2D position."""
    
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate distance to another position."""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


T = TypeVar('T')


class BoundingBox(Generic[T]):
    """Generic class representing a bounding box."""
    
    def __init__(
        self,
        min_x: float,
        min_y: float,
        max_x: float,
        max_y: float,
        content: Optional[T] = None
    ) -> None:
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.content = content
    
    @property
    def width(self) -> float:
        """Get the width of the bounding box."""
        return self.max_x - self.min_x
    
    @property
    def height(self) -> float:
        """Get the height of the bounding box."""
        return self.max_y - self.min_y
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if the box contains a point."""
        return (
            self.min_x <= x <= self.max_x and
            self.min_y <= y <= self.max_y
        )
    
    def intersects(self, other: 'BoundingBox[T]') -> bool:
        """Check if this box intersects with another."""
        return not (
            self.max_x < other.min_x or
            self.min_x > other.max_x or
            self.max_y < other.min_y or
            self.min_y > other.max_y
        )


class Shape(ABC, ColorMixin, Drawable, Movable):
    """Abstract base class for all shapes."""
    
    def __init__(
        self,
        position: Position,
        color: str = "black"
    ) -> None:
        super().__init__(color)
        self.position = position
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> BoundingBox['Shape']:
        """Get the bounding box of the shape."""
        pass
    
    def move(self, dx: float, dy: float) -> None:
        """Move the shape by the given offset."""
        self.position.x += dx
        self.position.y += dy
    
    def draw(self) -> str:
        """Draw the shape (returns ASCII art representation)."""
        return f"{self.__class__.__name__} at {self.position}"


@dataclass
class Circle(Shape):
    """Class representing a circle."""
    radius: float
    
    def __post_init__(self) -> None:
        super().__init__(Position(0, 0))
    
    def area(self) -> float:
        return pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * pi * self.radius
    
    def get_bounding_box(self) -> BoundingBox['Shape']:
        return BoundingBox(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.position.x + self.radius,
            self.position.y + self.radius,
            self
        )
    
    def draw(self) -> str:
        return f"○ ({self.radius})"


@dataclass
class Rectangle(Shape):
    """Class representing a rectangle."""
    width: float
    height: float
    
    def __post_init__(self) -> None:
        super().__init__(Position(0, 0))
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def get_bounding_box(self) -> BoundingBox['Shape']:
        return BoundingBox(
            self.position.x,
            self.position.y,
            self.position.x + self.width,
            self.position.y + self.height,
            self
        )
    
    def draw(self) -> str:
        return f"□ ({self.width}x{self.height})"


class Square(Rectangle):
    """Class representing a square (special case of rectangle)."""
    
    def __init__(self, side: float) -> None:
        super().__init__(side, side)
    
    @property
    def side(self) -> float:
        """Get the side length."""
        return self.width
    
    @side.setter
    def side(self, value: float) -> None:
        """Set the side length (updates both width and height)."""
        self.width = value
        self.height = value


class Triangle(Shape):
    """Class representing a triangle."""
    
    def __init__(
        self,
        p1: Position,
        p2: Position,
        p3: Position,
        color: str = "black"
    ) -> None:
        """Initialize with three points."""
        super().__init__(p1, color)
        self.p2 = p2
        self.p3 = p3
    
    def area(self) -> float:
        """Calculate area using Heron's formula."""
        a = self.position.distance_to(self.p2)
        b = self.p2.distance_to(self.p3)
        c = self.p3.distance_to(self.position)
        s = (a + b + c) / 2  # semi-perimeter
        return sqrt(s * (s - a) * (s - b) * (s - c))
    
    def perimeter(self) -> float:
        """Calculate perimeter as sum of side lengths."""
        return (
            self.position.distance_to(self.p2) +
            self.p2.distance_to(self.p3) +
            self.p3.distance_to(self.position)
        )
    
    def get_bounding_box(self) -> BoundingBox['Shape']:
        """Get the bounding box containing all points."""
        min_x = min(self.position.x, self.p2.x, self.p3.x)
        min_y = min(self.position.y, self.p2.y, self.p3.y)
        max_x = max(self.position.x, self.p2.x, self.p3.x)
        max_y = max(self.position.y, self.p2.y, self.p3.y)
        return BoundingBox(min_x, min_y, max_x, max_y, self)
    
    def draw(self) -> str:
        return "△"


class CompositeShape(Shape):
    """Class representing a shape composed of multiple shapes."""
    
    def __init__(
        self,
        shapes: List[Shape],
        position: Optional[Position] = None,
        color: str = "black"
    ) -> None:
        """Initialize with a list of shapes."""
        if not shapes:
            raise ValueError("CompositeShape must contain at least one shape")
        
        super().__init__(
            position or Position(0, 0),
            color
        )
        self.shapes = shapes
    
    def area(self) -> float:
        """Calculate total area of all shapes."""
        return sum(shape.area() for shape in self.shapes)
    
    def perimeter(self) -> float:
        """Calculate total perimeter of all shapes."""
        return sum(shape.perimeter() for shape in self.shapes)
    
    def get_bounding_box(self) -> BoundingBox['Shape']:
        """Get bounding box containing all shapes."""
        if not self.shapes:
            return BoundingBox(0, 0, 0, 0, self)
        
        boxes = [shape.get_bounding_box() for shape in self.shapes]
        return BoundingBox(
            min(box.min_x for box in boxes),
            min(box.min_y for box in boxes),
            max(box.max_x for box in boxes),
            max(box.max_y for box in boxes),
            self
        )
    
    def move(self, dx: float, dy: float) -> None:
        """Move all shapes by the given offset."""
        super().move(dx, dy)
        for shape in self.shapes:
            shape.move(dx, dy)
    
    def draw(self) -> str:
        """Draw all shapes."""
        return f"Composite({len(self.shapes)} shapes)"


def main() -> None:
    """Example usage of the shape hierarchy."""
    # Create some basic shapes
    circle = Circle(5.0)
    circle.color = "red"
    
    rectangle = Rectangle(4.0, 3.0)
    rectangle.color = "blue"
    
    square = Square(2.0)
    square.color = "green"
    
    triangle = Triangle(
        Position(0, 0),
        Position(3, 0),
        Position(0, 4),
        "yellow"
    )
    
    # Create a composite shape
    composite = CompositeShape([circle, rectangle, square, triangle])
    
    # Move some shapes
    circle.move(1, 1)
    rectangle.move(-2, 3)
    
    # Print shape information
    shapes = [circle, rectangle, square, triangle, composite]
    for shape in shapes:
        print(f"\n{shape.__class__.__name__}:")
        print(f"Color: {shape.color}")
        print(f"Area: {shape.area():.2f}")
        print(f"Perimeter: {shape.perimeter():.2f}")
        print(f"Drawing: {shape.draw()}")
        bbox = shape.get_bounding_box()
        print(f"Bounding Box: ({bbox.min_x:.1f}, {bbox.min_y:.1f}) to "
              f"({bbox.max_x:.1f}, {bbox.max_y:.1f})")


if __name__ == "__main__":
    main() 