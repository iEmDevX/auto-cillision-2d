"""
Polygon triangulation using ear-clipping and Delaunay methods.

Godot uses ear-clipping triangulation for collision polygons.
This module provides triangulation compatible with Godot's approach.
"""

from typing import List, Tuple
import numpy as np
import logging
from shapely.geometry import Polygon as ShapelyPolygon
from shapely import ops
from earcut.earcut import earcut
from src.geometry.vector2d import Vector2D

logger = logging.getLogger(__name__)


class Triangulator:
    """
    Triangulate polygons into triangles for physics engine compatibility.
    
    Uses ear-clipping algorithm (similar to Godot) or Delaunay triangulation
    to decompose complex polygons into multiple triangles.
    """
    
    def __init__(self, method: str = "earcut"):
        """
        Initialize triangulator.
        
        Args:
            method: Triangulation method - "earcut" (recommended, like Godot)
        """
        self.method = method
        logger.info(f"Triangulator initialized with method: {method}")
    
    def triangulate_polygon(
        self, 
        vertices: List[Vector2D]
    ) -> List[List[Vector2D]]:
        """
        Triangulate a polygon into triangles.
        
        Args:
            vertices: List of polygon vertices in counter-clockwise order
            
        Returns:
            List of triangles, each as a list of 3 Vector2D vertices
        """
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")
        
        # Triangle is already triangulated
        if len(vertices) == 3:
            return [vertices]
        
        # Use earcut (ear clipping) - same as Godot
        return self._triangulate_earcut(vertices)
    
    def _triangulate_earcut(
        self, 
        vertices: List[Vector2D]
    ) -> List[List[Vector2D]]:
        """
        Ear clipping triangulation (same algorithm as Godot).
        
        This ensures triangles stay within polygon boundaries.
        
        Args:
            vertices: Polygon vertices
            
        Returns:
            List of triangles
        """
        try:
            # Flatten vertices to [x1, y1, x2, y2, ...]
            coords_flat = []
            for v in vertices:
                coords_flat.extend([v.x, v.y])
            
            # Use earcut library (earcut is already the function)
            triangle_indices = earcut(coords_flat)
            
            # Convert indices to triangle vertices
            triangles = []
            for i in range(0, len(triangle_indices), 3):
                idx1 = triangle_indices[i]
                idx2 = triangle_indices[i + 1]
                idx3 = triangle_indices[i + 2]
                
                triangle = [
                    vertices[idx1],
                    vertices[idx2],
                    vertices[idx3]
                ]
                triangles.append(triangle)
            
            logger.debug(
                f"Earcut triangulation: {len(vertices)} vertices -> "
                f"{len(triangles)} triangles"
            )
            
            return triangles
            
        except Exception as e:
            logger.error(f"Earcut triangulation failed: {e}")
            # Fallback to fan triangulation
            return self._fan_triangulation(vertices)
    
    def _fan_triangulation(
        self, 
        vertices: List[Vector2D]
    ) -> List[List[Vector2D]]:
        """
        Simple fan triangulation from first vertex.
        
        Fast but creates long thin triangles for concave polygons.
        
        Args:
            vertices: Polygon vertices
            
        Returns:
            List of triangles
        """
        if len(vertices) < 3:
            return []
        
        triangles = []
        v0 = vertices[0]
        
        for i in range(1, len(vertices) - 1):
            triangle = [v0, vertices[i], vertices[i + 1]]
            triangles.append(triangle)
        
        logger.debug(
            f"Fan triangulation: {len(vertices)} vertices -> "
            f"{len(triangles)} triangles"
        )
        
        return triangles
