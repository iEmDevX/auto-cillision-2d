"""
JSON file writer for collision polygon data.
"""

import json
from typing import List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def save_collision_json(
    polygons: List[List[List[float]]],
    filepath: str,
    indent: Optional[int] = None
) -> None:
    """
    Save collision polygons to JSON file.
    
    Output format matches example/base.json:
    [
      [[x1, y1], [x2, y2], [x3, y3]],
      [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    ]
    
    Args:
        polygons: List of polygons (pure nested arrays)
        filepath: Output JSON file path
        indent: JSON indentation (None for compact)
        
    Raises:
        ValueError: If data format is invalid
    """
    # Validate format
    if not isinstance(polygons, list):
        raise ValueError("Polygons must be a list")
    
    for i, polygon in enumerate(polygons):
        if not isinstance(polygon, list):
            raise ValueError(f"Polygon {i} must be a list")
        
        if not 3 <= len(polygon) <= 8:
            raise ValueError(
                f"Polygon {i} must have 3-8 vertices, got {len(polygon)}"
            )
        
        for j, vertex in enumerate(polygon):
            if not isinstance(vertex, list) or len(vertex) != 2:
                raise ValueError(
                    f"Vertex {j} in polygon {i} must be [x, y] list"
                )
    
    # Ensure directory exists
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON file
    try:
        with open(filepath, 'w') as f:
            # Use minimal separators for compact output (no spaces)
            json.dump(polygons, f, indent=indent, separators=(',', ':'))
        
        logger.info(f"Saved collision JSON: {filepath} ({len(polygons)} polygons)")
        
    except Exception as e:
        logger.error(f"Failed to save JSON to {filepath}: {e}")
        raise


def load_collision_json(filepath: str) -> List[List[List[float]]]:
    """
    Load collision polygons from JSON file.
    
    Args:
        filepath: Input JSON file path
        
    Returns:
        List of polygons
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON format is invalid
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise ValueError(f"Invalid JSON file: {filepath}") from e
    
    # Validate format
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of polygons")
    
    logger.info(f"Loaded collision JSON: {filepath} ({len(data)} polygons)")
    
    return data


from typing import Optional
