"""
Unit tests for polygon simplifier.
"""

import pytest
import numpy as np
from src.core.polygon_simplifier import PolygonSimplifier, contour_to_polygon
from src.geometry.vector2d import Vector2D


class TestPolygonSimplifier:
    """Test PolygonSimplifier class."""
    
    def test_initialization(self):
        """Test simplifier initialization."""
        simplifier = PolygonSimplifier(epsilon=2.0, max_vertices=6)
        assert simplifier.epsilon == 2.0
        assert simplifier.max_vertices == 6
    
    def test_invalid_epsilon(self):
        """Test invalid epsilon raises error."""
        with pytest.raises(ValueError):
            PolygonSimplifier(epsilon=0.0)
        
        with pytest.raises(ValueError):
            PolygonSimplifier(epsilon=-1.0)
    
    def test_invalid_max_vertices(self):
        """Test invalid max_vertices raises error."""
        with pytest.raises(ValueError):
            PolygonSimplifier(max_vertices=2)
        
        with pytest.raises(ValueError):
            PolygonSimplifier(max_vertices=9)
    
    def test_simplify_contour(self):
        """Test contour simplification."""
        # Create a square contour
        contour = np.array([
            [[0, 0]],
            [[10, 0]],
            [[10, 10]],
            [[0, 10]]
        ])
        
        simplifier = PolygonSimplifier(epsilon=1.0, max_vertices=8)
        vertices = simplifier.simplify_contour(contour)
        
        assert len(vertices) >= 3
        assert len(vertices) <= 8
        assert all(isinstance(v, Vector2D) for v in vertices)
    
    def test_merge_close_vertices(self):
        """Test merging close vertices."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(0.1, 0.1),  # Very close to first
            Vector2D(10.0, 0.0),
            Vector2D(10.0, 10.0)
        ]
        
        simplifier = PolygonSimplifier()
        merged = simplifier.merge_close_vertices(vertices, threshold=1.0)
        
        assert len(merged) < len(vertices)
    
    def test_split_into_triangles(self):
        """Test polygon triangulation."""
        # Pentagon
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(2.0, 0.0),
            Vector2D(2.5, 1.0),
            Vector2D(1.0, 2.0),
            Vector2D(-0.5, 1.0)
        ]
        
        simplifier = PolygonSimplifier()
        triangles = simplifier.split_into_triangles(vertices)
        
        assert len(triangles) == 3  # Pentagon = 3 triangles
        assert all(len(t) == 3 for t in triangles)
    
    def test_validate_polygon_valid(self):
        """Test polygon validation for valid polygon."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(10.0, 0.0),
            Vector2D(0.0, 10.0)
        ]
        
        simplifier = PolygonSimplifier()
        assert simplifier.validate_polygon(vertices) is True
    
    def test_validate_polygon_too_few_vertices(self):
        """Test polygon validation for too few vertices."""
        vertices = [
            Vector2D(0.0, 0.0),
            Vector2D(1.0, 0.0)
        ]
        
        simplifier = PolygonSimplifier()
        assert simplifier.validate_polygon(vertices) is False
    
    def test_validate_polygon_too_many_vertices(self):
        """Test polygon validation for too many vertices."""
        vertices = [Vector2D(float(i), 0.0) for i in range(10)]
        
        simplifier = PolygonSimplifier(max_vertices=8)
        assert simplifier.validate_polygon(vertices) is False


def test_contour_to_polygon():
    """Test convenience function."""
    contour = np.array([
        [[0, 0]],
        [[10, 0]],
        [[10, 10]],
        [[0, 10]]
    ])
    
    vertices = contour_to_polygon(contour, epsilon=1.0, max_vertices=6)
    
    assert len(vertices) >= 3
    assert len(vertices) <= 6
