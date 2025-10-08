"""
2D Vector and geometric primitives for collision polygon generation.
"""

from typing import Tuple, List
import math


class Vector2D:
    """
    Immutable 2D vector class with common vector operations.
    
    Attributes:
        x: X-coordinate
        y: Y-coordinate
    """
    
    __slots__ = ('_x', '_y')
    
    def __init__(self, x: float, y: float) -> None:
        """
        Initialize a 2D vector.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
        """
        self._x = float(x)
        self._y = float(y)
    
    @property
    def x(self) -> float:
        """Get x-coordinate."""
        return self._x
    
    @property
    def y(self) -> float:
        """Get y-coordinate."""
        return self._y
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Vector2D({self._x}, {self._y})"
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another vector."""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return math.isclose(self._x, other._x) and math.isclose(self._y, other._y)
    
    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""
        return hash((self._x, self._y))
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Add two vectors."""
        return Vector2D(self._x + other._x, self._y + other._y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Subtract two vectors."""
        return Vector2D(self._x - other._x, self._y - other._y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        """Multiply vector by scalar."""
        return Vector2D(self._x * scalar, self._y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2D':
        """Divide vector by scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self._x / scalar, self._y / scalar)
    
    def dot(self, other: 'Vector2D') -> float:
        """
        Compute dot product with another vector.
        
        Args:
            other: Another vector
            
        Returns:
            Dot product
        """
        return self._x * other._x + self._y * other._y
    
    def cross(self, other: 'Vector2D') -> float:
        """
        Compute 2D cross product (z-component).
        
        Args:
            other: Another vector
            
        Returns:
            Z-component of cross product
        """
        return self._x * other._y - self._y * other._x
    
    def length(self) -> float:
        """Calculate vector length/magnitude."""
        return math.sqrt(self._x * self._x + self._y * self._y)
    
    def length_squared(self) -> float:
        """Calculate squared length (faster than length())."""
        return self._x * self._x + self._y * self._y
    
    def distance_to(self, other: 'Vector2D') -> float:
        """
        Calculate distance to another vector.
        
        Args:
            other: Target vector
            
        Returns:
            Distance
        """
        return (self - other).length()
    
    def normalized(self) -> 'Vector2D':
        """
        Get normalized (unit length) vector.
        
        Returns:
            Normalized vector
            
        Raises:
            ValueError: If vector is zero-length
        """
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize zero-length vector")
        return self / length
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple (x, y)."""
        return (self._x, self._y)
    
    def to_list(self) -> List[float]:
        """Convert to list [x, y]."""
        return [self._x, self._y]
    
    @classmethod
    def from_tuple(cls, coords: Tuple[float, float]) -> 'Vector2D':
        """
        Create vector from tuple.
        
        Args:
            coords: (x, y) tuple
            
        Returns:
            New Vector2D
        """
        return cls(coords[0], coords[1])
    
    @classmethod
    def from_list(cls, coords: List[float]) -> 'Vector2D':
        """
        Create vector from list.
        
        Args:
            coords: [x, y] list
            
        Returns:
            New Vector2D
        """
        if len(coords) != 2:
            raise ValueError(f"Expected 2 coordinates, got {len(coords)}")
        return cls(coords[0], coords[1])


def perpendicular_distance(point: Vector2D, line_start: Vector2D, line_end: Vector2D) -> float:
    """
    Calculate perpendicular distance from point to line segment.
    
    Args:
        point: Point to measure from
        line_start: Start of line segment
        line_end: End of line segment
        
    Returns:
        Perpendicular distance
    """
    # Vector from line_start to line_end
    line_vec = line_end - line_start
    line_length_sq = line_vec.length_squared()
    
    if line_length_sq == 0:
        # Line segment is a point
        return point.distance_to(line_start)
    
    # Vector from line_start to point
    point_vec = point - line_start
    
    # Project point onto line
    t = point_vec.dot(line_vec) / line_length_sq
    
    if t < 0:
        # Closest point is line_start
        return point.distance_to(line_start)
    elif t > 1:
        # Closest point is line_end
        return point.distance_to(line_end)
    else:
        # Closest point is on the line segment
        closest = line_start + line_vec * t
        return point.distance_to(closest)


def polygon_area(vertices: List[Vector2D]) -> float:
    """
    Calculate area of polygon using shoelace formula.
    
    Args:
        vertices: List of polygon vertices in order
        
    Returns:
        Polygon area (positive for counter-clockwise, negative for clockwise)
    """
    if len(vertices) < 3:
        return 0.0
    
    area = 0.0
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % len(vertices)]
        area += v1.x * v2.y - v2.x * v1.y
    
    return abs(area) / 2.0


def is_counter_clockwise(vertices: List[Vector2D]) -> bool:
    """
    Check if polygon vertices are in counter-clockwise order.
    
    Args:
        vertices: List of polygon vertices
        
    Returns:
        True if counter-clockwise, False if clockwise
    """
    if len(vertices) < 3:
        return True
    
    # Calculate signed area
    area = 0.0
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % len(vertices)]
        area += v1.x * v2.y - v2.x * v1.y
    
    return area > 0
