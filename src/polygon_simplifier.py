"""
Polygon simplification using Douglas-Peucker algorithm.
"""

from typing import List, Tuple
import numpy as np
import cv2
import logging
from geometry.vector2d import Vector2D, perpendicular_distance

logger = logging.getLogger(__name__)


class PolygonSimplifier:
    """
    Simplify polygons using Douglas-Peucker algorithm with vertex limits.
    
    Ensures each polygon has between 3 and max_vertices vertices while
    maintaining shape accuracy within epsilon tolerance.
    """
    
    def __init__(self, epsilon: float = 2.0, max_vertices: int = 8) -> None:
        """
        Initialize polygon simplifier.
        
        Args:
            epsilon: Douglas-Peucker simplification tolerance (in pixels)
            max_vertices: Maximum vertices per polygon (3-8)
            
        Raises:
            ValueError: If parameters are invalid
        """
        if epsilon <= 0:
            raise ValueError(f"Epsilon must be positive, got {epsilon}")
        
        if not 3 <= max_vertices <= 8:
            raise ValueError(f"Max vertices must be 3-8, got {max_vertices}")
        
        self.epsilon = epsilon
        self.max_vertices = max_vertices
    
    def simplify_contour(self, contour: np.ndarray) -> List[Vector2D]:
        """
        Simplify OpenCV contour to polygon with limited vertices.
        
        Args:
            contour: OpenCV contour array (Nx1x2)
            
        Returns:
            List of Vector2D vertices
            
        Raises:
            ValueError: If contour is invalid
        """
        if len(contour) < 3:
            raise ValueError("Contour must have at least 3 points")
        
        # Use cv2.approxPolyDP for Douglas-Peucker algorithm
        epsilon = self.epsilon
        simplified = cv2.approxPolyDP(contour, epsilon, closed=True)
        
        # If still too many vertices, increase epsilon
        max_iterations = 10
        iteration = 0
        while len(simplified) > self.max_vertices and iteration < max_iterations:
            epsilon *= 1.5
            simplified = cv2.approxPolyDP(contour, epsilon, closed=True)
            iteration += 1
        
        if len(simplified) > self.max_vertices:
            logger.warning(
                f"Could not reduce to {self.max_vertices} vertices "
                f"after {max_iterations} iterations. Got {len(simplified)} vertices."
            )
            # Take every nth point to reduce count
            n = len(simplified) // self.max_vertices
            simplified = simplified[::n][:self.max_vertices]
        
        # Convert to Vector2D list
        vertices = []
        for point in simplified:
            x, y = point[0]
            vertices.append(Vector2D(float(x), float(y)))
        
        logger.debug(
            f"Simplified contour: {len(contour)} -> {len(vertices)} vertices "
            f"(epsilon: {epsilon:.2f})"
        )
        
        return vertices
    
    def douglas_peucker(
        self,
        points: List[Vector2D],
        epsilon: float
    ) -> List[Vector2D]:
        """
        Pure Python implementation of Douglas-Peucker algorithm.
        
        Args:
            points: List of points forming a polyline
            epsilon: Simplification tolerance
            
        Returns:
            Simplified list of points
        """
        if len(points) < 3:
            return points
        
        # Find point with maximum distance from line start->end
        max_dist = 0.0
        max_index = 0
        
        start = points[0]
        end = points[-1]
        
        for i in range(1, len(points) - 1):
            dist = perpendicular_distance(points[i], start, end)
            if dist > max_dist:
                max_dist = dist
                max_index = i
        
        # If max distance is greater than epsilon, recursively simplify
        if max_dist > epsilon:
            # Recursive call on two segments
            left = self.douglas_peucker(points[:max_index + 1], epsilon)
            right = self.douglas_peucker(points[max_index:], epsilon)
            
            # Combine results (remove duplicate middle point)
            return left[:-1] + right
        else:
            # All points can be removed except endpoints
            return [start, end]
    
    def split_into_triangles(self, vertices: List[Vector2D]) -> List[List[Vector2D]]:
        """
        Split polygon into triangles using fan triangulation.
        
        Args:
            vertices: Polygon vertices
            
        Returns:
            List of triangles (each triangle is a list of 3 Vector2D)
        """
        if len(vertices) < 3:
            raise ValueError("Need at least 3 vertices to triangulate")
        
        if len(vertices) == 3:
            return [vertices]
        
        # Simple fan triangulation from first vertex
        triangles = []
        for i in range(1, len(vertices) - 1):
            triangle = [
                vertices[0],
                vertices[i],
                vertices[i + 1]
            ]
            triangles.append(triangle)
        
        logger.debug(f"Split polygon ({len(vertices)} vertices) into {len(triangles)} triangles")
        
        return triangles
    
    def merge_close_vertices(
        self,
        vertices: List[Vector2D],
        threshold: float = 2.0
    ) -> List[Vector2D]:
        """
        Merge vertices that are very close together.
        
        Args:
            vertices: List of vertices
            threshold: Distance threshold for merging
            
        Returns:
            List of merged vertices
        """
        if len(vertices) < 3:
            return vertices
        
        merged = [vertices[0]]
        
        for i in range(1, len(vertices)):
            if vertices[i].distance_to(merged[-1]) > threshold:
                merged.append(vertices[i])
        
        # Check if last vertex is too close to first
        if len(merged) > 2 and merged[-1].distance_to(merged[0]) < threshold:
            merged = merged[:-1]
        
        if len(merged) < 3:
            logger.warning(f"Merging vertices resulted in < 3 vertices, keeping original")
            return vertices
        
        if len(merged) != len(vertices):
            logger.debug(f"Merged vertices: {len(vertices)} -> {len(merged)}")
        
        return merged
    
    def validate_polygon(self, vertices: List[Vector2D]) -> bool:
        """
        Validate that polygon is acceptable.
        
        Args:
            vertices: Polygon vertices
            
        Returns:
            True if valid, False otherwise
        """
        # Must have 3-8 vertices
        if not 3 <= len(vertices) <= self.max_vertices:
            return False
        
        # Check for duplicate vertices
        unique_vertices = set(vertices)
        if len(unique_vertices) != len(vertices):
            logger.warning("Polygon has duplicate vertices")
            return False
        
        # Check minimum area (avoid degenerate polygons)
        from geometry.vector2d import polygon_area
        area = polygon_area(vertices)
        if area < 1.0:  # Less than 1 square pixel
            logger.warning(f"Polygon area too small: {area:.2f}")
            return False
        
        return True


def contour_to_polygon(
    contour: np.ndarray,
    epsilon: float = 2.0,
    max_vertices: int = 8
) -> List[Vector2D]:
    """
    Convert OpenCV contour to simplified polygon.
    
    Args:
        contour: OpenCV contour array
        epsilon: Simplification tolerance
        max_vertices: Maximum vertices
        
    Returns:
        List of Vector2D vertices
    """
    simplifier = PolygonSimplifier(epsilon=epsilon, max_vertices=max_vertices)
    return simplifier.simplify_contour(contour)
