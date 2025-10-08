"""
Unit tests for Vector2D and geometry utilities.
"""

import pytest
import math
from src.geometry.vector2d import (
    Vector2D,
    perpendicular_distance,
    polygon_area,
    is_counter_clockwise
)


class TestVector2D:
    """Test Vector2D class."""
    
    def test_initialization(self):
        """Test vector initialization."""
        v = Vector2D(3.0, 4.0)
        assert v.x == 3.0
        assert v.y == 4.0
    
    def test_equality(self):
        """Test vector equality."""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(1.0, 2.0)
        v3 = Vector2D(2.0, 1.0)
        
        assert v1 == v2
        assert v1 != v3
    
    def test_addition(self):
        """Test vector addition."""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(3.0, 4.0)
        v3 = v1 + v2
        
        assert v3.x == 4.0
        assert v3.y == 6.0
    
    def test_subtraction(self):
        """Test vector subtraction."""
        v1 = Vector2D(5.0, 7.0)
        v2 = Vector2D(2.0, 3.0)
        v3 = v1 - v2
        
        assert v3.x == 3.0
        assert v3.y == 4.0
    
    def test_multiplication(self):
        """Test scalar multiplication."""
        v1 = Vector2D(2.0, 3.0)
        v2 = v1 * 3.0
        
        assert v2.x == 6.0
        assert v2.y == 9.0
    
    def test_division(self):
        """Test scalar division."""
        v1 = Vector2D(6.0, 9.0)
        v2 = v1 / 3.0
        
        assert v2.x == 2.0
        assert v2.y == 3.0
    
    def test_division_by_zero(self):
        """Test division by zero raises error."""
        v = Vector2D(1.0, 2.0)
        with pytest.raises(ValueError):
            v / 0.0
    
    def test_dot_product(self):
        """Test dot product."""
        v1 = Vector2D(1.0, 2.0)
        v2 = Vector2D(3.0, 4.0)
        
        assert v1.dot(v2) == 11.0  # 1*3 + 2*4
    
    def test_cross_product(self):
        """Test 2D cross product."""
        v1 = Vector2D(1.0, 0.0)
        v2 = Vector2D(0.0, 1.0)
        
        assert v1.cross(v2) == 1.0
    
    def test_length(self):
        """Test vector length."""
        v = Vector2D(3.0, 4.0)
        assert v.length() == 5.0
    
    def test_length_squared(self):
        """Test squared length."""
        v = Vector2D(3.0, 4.0)
        assert v.length_squared() == 25.0
    
    def test_distance_to(self):
        """Test distance calculation."""
        v1 = Vector2D(0.0, 0.0)
        v2 = Vector2D(3.0, 4.0)
        
        assert v1.distance_to(v2) == 5.0
    
    def test_normalized(self):
        """Test vector normalization."""
        v = Vector2D(3.0, 4.0)
        normalized = v.normalized()
        
        assert math.isclose(normalized.length(), 1.0)
        assert math.isclose(normalized.x, 0.6)
        assert math.isclose(normalized.y, 0.8)
    
    def test_normalized_zero_vector(self):
        """Test normalizing zero vector raises error."""
        v = Vector2D(0.0, 0.0)
        with pytest.raises(ValueError):
            v.normalized()
    
    def test_to_tuple(self):
        """Test conversion to tuple."""
        v = Vector2D(1.5, 2.5)
        assert v.to_tuple() == (1.5, 2.5)
    
    def test_to_list(self):
        """Test conversion to list."""
        v = Vector2D(1.5, 2.5)
        assert v.to_list() == [1.5, 2.5]
    
    def test_from_tuple(self):
        """Test creation from tuple."""
        v = Vector2D.from_tuple((3.0, 4.0))
        assert v.x == 3.0
        assert v.y == 4.0
    
    def test_from_list(self):
        """Test creation from list."""
        v = Vector2D.from_list([5.0, 6.0])
        assert v.x == 5.0
        assert v.y == 6.0
    
    def test_from_list_invalid_length(self):
        """Test creation from invalid list raises error."""
        with pytest.raises(ValueError):
            Vector2D.from_list([1.0])
        
        with pytest.raises(ValueError):
            Vector2D.from_list([1.0, 2.0, 3.0])


class TestGeometryFunctions:
    """Test geometry utility functions."""
    
    def test_perpendicular_distance_on_line(self):
        """Test perpendicular distance to line."""
        point = Vector2D(0.0, 1.0)
        line_start = Vector2D(-1.0, 0.0)
        line_end = Vector2D(1.0, 0.0)
        
        distance = perpendicular_distance(point, line_start, line_end)
        assert math.isclose(distance, 1.0)
    
    def test_perpendicular_distance_to_point(self):
        """Test distance when line is a point."""
        point = Vector2D(3.0, 4.0)
        line_start = Vector2D(0.0, 0.0)
        line_end = Vector2D(0.0, 0.0)
        
        distance = perpendicular_distance(point, line_start, line_end)
        assert math.isclose(distance, 5.0)
    
    def test_polygon_area_square(self):
        """Test area calculation for square."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(2.0, 0.0),
            Vector2D(2.0, 2.0),
            Vector2D(0.0, 2.0)
        ]
        
        area = polygon_area(vertices)
        assert math.isclose(area, 4.0)
    
    def test_polygon_area_triangle(self):
        """Test area calculation for triangle."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(4.0, 0.0),
            Vector2D(0.0, 3.0)
        ]
        
        area = polygon_area(vertices)
        assert math.isclose(area, 6.0)
    
    def test_is_counter_clockwise_ccw(self):
        """Test CCW detection for counter-clockwise polygon."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(1.0, 0.0),
            Vector2D(0.0, 1.0)
        ]
        
        assert is_counter_clockwise(vertices) is True
    
    def test_is_counter_clockwise_cw(self):
        """Test CCW detection for clockwise polygon."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(0.0, 1.0),
            Vector2D(1.0, 0.0)
        ]
        
        assert is_counter_clockwise(vertices) is False
