"""
Geometry utilities for 2D collision polygon generation.
"""

from src.geometry.vector2d import (
    Vector2D,
    perpendicular_distance,
    polygon_area,
    is_counter_clockwise
)

__version__ = "0.1.0"
__all__ = [
    'Vector2D',
    'perpendicular_distance',
    'polygon_area',
    'is_counter_clockwise'
]
