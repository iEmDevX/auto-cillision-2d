"""
Main collision polygon generation pipeline.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from src.geometry.vector2d import Vector2D
from src.core.image_processor import ImageProcessor
from src.core.polygon_simplifier import PolygonSimplifier

logger = logging.getLogger(__name__)


class CollisionMapper:
    """
    Generate collision polygon mappings from sprite images.
    
    Main pipeline that coordinates image processing, contour detection,
    polygon simplification, and output generation.
    """
    
    def __init__(
        self,
        alpha_threshold: int = 128,
        epsilon: float = 2.0,
        max_vertices: int = 8,
        min_area: float = 10.0
    ) -> None:
        """
        Initialize collision mapper.
        
        Args:
            alpha_threshold: Alpha channel threshold (0-255)
            epsilon: Douglas-Peucker simplification tolerance
            max_vertices: Maximum vertices per polygon (3-8)
            min_area: Minimum polygon area in square pixels
        """
        self.image_processor = ImageProcessor(alpha_threshold=alpha_threshold)
        self.polygon_simplifier = PolygonSimplifier(
            epsilon=epsilon,
            max_vertices=max_vertices
        )
        self.min_area = min_area
        
        logger.info(
            f"CollisionMapper initialized: alpha_threshold={alpha_threshold}, "
            f"epsilon={epsilon}, max_vertices={max_vertices}, min_area={min_area}"
        )
    
    def generate_collision_polygons(
        self,
        filepath: str
    ) -> List[List[List[float]]]:
        """
        Generate collision polygons from sprite image.
        
        Args:
            filepath: Path to PNG sprite file
            
        Returns:
            List of polygons in format [[[x1,y1],[x2,y2],...],...]
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If image processing fails
        """
        logger.info(f"Generating collision polygons for: {filepath}")
        
        # Process image and find contours
        img, contours, mask = self.image_processor.process_image(filepath)
        
        # Convert contours to simplified polygons
        all_polygons: List[List[List[float]]] = []
        
        for i, contour in enumerate(contours):
            try:
                # Simplify contour to polygon
                vertices = self.polygon_simplifier.simplify_contour(contour)
                
                # Merge close vertices
                vertices = self.polygon_simplifier.merge_close_vertices(vertices)
                
                # Validate polygon
                if not self.polygon_simplifier.validate_polygon(vertices):
                    logger.warning(f"Contour {i} failed validation, skipping")
                    continue
                
                # Check area
                from geometry.vector2d import polygon_area
                area = polygon_area(vertices)
                if area < self.min_area:
                    logger.debug(
                        f"Contour {i} area too small ({area:.1f} < {self.min_area}), skipping"
                    )
                    continue
                
                # If polygon has > max_vertices, split into triangles
                if len(vertices) > self.polygon_simplifier.max_vertices:
                    logger.info(
                        f"Polygon {i} has {len(vertices)} vertices, "
                        f"splitting into triangles"
                    )
                    triangles = self.polygon_simplifier.split_into_triangles(vertices)
                    
                    for triangle in triangles:
                        polygon_data = [v.to_list() for v in triangle]
                        all_polygons.append(polygon_data)
                else:
                    # Convert vertices to list format
                    polygon_data = [v.to_list() for v in vertices]
                    all_polygons.append(polygon_data)
                
            except Exception as e:
                logger.error(f"Failed to process contour {i}: {e}", exc_info=True)
                continue
        
        if not all_polygons:
            raise ValueError("No valid collision polygons generated")
        
        # Calculate statistics
        total_vertices = sum(len(p) for p in all_polygons)
        avg_vertices = total_vertices / len(all_polygons)
        
        logger.info(
            f"Generated {len(all_polygons)} polygon(s), "
            f"{total_vertices} total vertices, "
            f"{avg_vertices:.1f} avg vertices/polygon"
        )
        
        return all_polygons
    
    def generate_with_metadata(
        self,
        filepath: str
    ) -> Dict[str, Any]:
        """
        Generate collision polygons with metadata.
        
        Args:
            filepath: Path to PNG sprite file
            
        Returns:
            Dictionary with collision data and metadata
        """
        # Generate polygons
        polygons = self.generate_collision_polygons(filepath)
        
        # Get image info
        from src.image_processor import get_image_dimensions
        width, height = get_image_dimensions(filepath)
        
        # Calculate statistics
        vertex_counts = {}
        for polygon in polygons:
            count = len(polygon)
            vertex_counts[count] = vertex_counts.get(count, 0) + 1
        
        # Build metadata
        metadata = {
            "sprite_file": Path(filepath).name,
            "image_size": {"width": width, "height": height},
            "polygon_count": len(polygons),
            "total_vertices": sum(len(p) for p in polygons),
            "vertex_distribution": vertex_counts,
            "generation_params": {
                "alpha_threshold": self.image_processor.alpha_threshold,
                "epsilon": self.polygon_simplifier.epsilon,
                "max_vertices": self.polygon_simplifier.max_vertices,
                "min_area": self.min_area
            }
        }
        
        return {
            "polygons": polygons,
            "metadata": metadata
        }
    
    def batch_process(
        self,
        input_dir: str,
        output_dir: Optional[str] = None
    ) -> Dict[str, List[List[List[float]]]]:
        """
        Process all PNG files in a directory.
        
        Args:
            input_dir: Directory containing PNG files
            output_dir: Optional output directory for JSON files
            
        Returns:
            Dictionary mapping filenames to polygon data
        """
        from pathlib import Path
        
        input_path = Path(input_dir)
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Find all PNG files
        png_files = list(input_path.glob("*.png"))
        if not png_files:
            logger.warning(f"No PNG files found in {input_dir}")
            return {}
        
        logger.info(f"Processing {len(png_files)} PNG file(s) from {input_dir}")
        
        results = {}
        for png_file in png_files:
            try:
                logger.info(f"Processing: {png_file.name}")
                polygons = self.generate_collision_polygons(str(png_file))
                results[png_file.name] = polygons
                
                # Optionally save to output directory
                if output_dir:
                    from utils.json_writer import save_collision_json
                    output_path = Path(output_dir) / f"{png_file.stem}.json"
                    save_collision_json(polygons, str(output_path))
                    
            except Exception as e:
                logger.error(f"Failed to process {png_file.name}: {e}")
                continue
        
        logger.info(f"Batch processing complete: {len(results)}/{len(png_files)} successful")
        
        return results
