from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Protocol
import math

# Protocol for drawable objects
class Drawable(Protocol):
    def draw(self) -> None:
        pass

# Abstract base class for shapes
class Shape(ABC, Drawable):
    """Abstract base class for all shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass
    
    @abstractmethod
    def draw(self) -> None:
        """Draw the shape."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} (Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f})"

# Mixin class for color
class ColorMixin:
    """Mixin class to add color functionality."""
    
    def __init__(self, color: str = "black"):
        self._color = color
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        self._color = value.lower()

# Circle implementation
@dataclass
class Circle(Shape, ColorMixin):
    """Circle shape with radius."""
    radius: float
    
    def __post_init__(self):
        super().__init__()  # Initialize ColorMixin
        if self.radius <= 0:
            raise ValueError("Radius must be positive")
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    def draw(self) -> None:
        print(f"Drawing {self.color} circle with radius {self.radius}")

# Rectangle implementation
class Rectangle(Shape, ColorMixin):
    """Rectangle shape with width and height."""
    
    def __init__(self, width: float, height: float, color: str = "black"):
        super().__init__(color)
        self._width = width
        self._height = height
        
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
    
    # Property example
    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def draw(self) -> None:
        print(f"Drawing {self.color} rectangle {self.width}x{self.height}")
    
    # Special method example
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self.width == other.width and 
                self.height == other.height and 
                self.color == other.color)

# Square as a special case of Rectangle
class Square(Rectangle):
    """Square is a special case of Rectangle with equal sides."""
    
    def __init__(self, side: float, color: str = "black"):
        super().__init__(side, side, color)
    
    @property
    def side(self) -> float:
        return self.width
    
    @side.setter
    def side(self, value: float) -> None:
        self.width = value
        self.height = value
    
    def draw(self) -> None:
        print(f"Drawing {self.color} square with side {self.side}")

# Canvas class to demonstrate composition
class Canvas:
    """Canvas that can contain multiple shapes."""
    
    def __init__(self):
        self._shapes: List[Shape] = []
    
    def add_shape(self, shape: Shape) -> None:
        self._shapes.append(shape)
    
    def remove_shape(self, shape: Shape) -> None:
        self._shapes.remove(shape)
    
    def total_area(self) -> float:
        return sum(shape.area() for shape in self._shapes)
    
    def draw_all(self) -> None:
        for shape in self._shapes:
            shape.draw()
    
    # Context manager example
    def __enter__(self):
        print("Starting to draw on canvas")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Finished drawing on canvas")
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        return False  # Don't suppress exceptions

def main():
    # Create some shapes
    circle = Circle(5.0)
    circle.color = "red"
    
    rectangle = Rectangle(4.0, 6.0, "blue")
    square = Square(3.0, "green")
    
    # Demonstrate canvas usage with context manager
    with Canvas() as canvas:
        # Add shapes to canvas
        canvas.add_shape(circle)
        canvas.add_shape(rectangle)
        canvas.add_shape(square)
        
        # Draw all shapes
        print("\nDrawing all shapes:")
        canvas.draw_all()
        
        # Calculate total area
        print(f"\nTotal area: {canvas.total_area():.2f}")
        
        # Demonstrate shape information
        print("\nShape details:")
        for shape in [circle, rectangle, square]:
            print(shape)
        
        # Demonstrate property usage
        print("\nModifying square:")
        square.side = 4.0
        print(f"New square area: {square.area():.2f}")
        
        # Demonstrate equality comparison
        rect1 = Rectangle(2.0, 3.0, "black")
        rect2 = Rectangle(2.0, 3.0, "black")
        print(f"\nRectangles equal: {rect1 == rect2}")

if __name__ == "__main__":
    main() 