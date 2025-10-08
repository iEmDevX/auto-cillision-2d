"""
Preview image generator for visualizing collision polygons.
"""

from typing import List, Optional, Tuple
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class PreviewGenerator:
    """
    Generate preview images showing collision polygons overlaid on sprites.
    
    Creates visualization images for manual verification of collision shapes.
    """
    
    def __init__(
        self,
        show_vertices: bool = True,
        show_labels: bool = False,
        line_width: float = 1.5
    ) -> None:
        """
        Initialize preview generator.
        
        Args:
            show_vertices: Draw vertex markers
            show_labels: Show polygon/vertex labels
            line_width: Polygon outline width
        """
        self.show_vertices = show_vertices
        self.show_labels = show_labels
        self.line_width = line_width
    
    def generate_preview(
        self,
        sprite_path: str,
        polygons: List[List[List[float]]],
        output_path: str,
        dpi: int = 150
    ) -> None:
        """
        Generate and save preview image.
        
        Args:
            sprite_path: Path to original sprite PNG
            polygons: Collision polygons data
            output_path: Output path for preview image
            dpi: Image resolution
            
        Raises:
            FileNotFoundError: If sprite file doesn't exist
            ValueError: If polygon data is invalid
        """
        logger.info(f"Generating preview for {sprite_path}")
        
        # Load sprite
        sprite = Image.open(sprite_path)
        if sprite.mode != 'RGBA':
            sprite = sprite.convert('RGBA')
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
        
        # Left: Original sprite
        ax1.imshow(sprite)
        ax1.set_title('Original Sprite', fontsize=16, fontweight='bold')
        ax1.axis('off')
        
        # Right: Sprite with collision overlay
        ax2.imshow(sprite, alpha=0.5)
        
        # Draw polygons
        colors = plt.cm.rainbow(np.linspace(0, 1, len(polygons)))
        
        for i, (polygon, color) in enumerate(zip(polygons, colors)):
            self._draw_polygon(ax2, polygon, color, i)
        
        title = f'Collision Polygons ({len(polygons)} shapes)'
        ax2.set_title(title, fontsize=16, fontweight='bold')
        ax2.axis('off')
        
        # Add statistics
        total_vertices = sum(len(p) for p in polygons)
        avg_vertices = total_vertices / len(polygons) if polygons else 0
        
        stats_text = (
            f"Sprite: {Path(sprite_path).name}\n"
            f"Size: {sprite.size[0]}x{sprite.size[1]} pixels\n"
            f"Polygons: {len(polygons)}\n"
            f"Total vertices: {total_vertices}\n"
            f"Avg vertices/polygon: {avg_vertices:.1f}"
        )
        
        fig.text(
            0.5, 0.02, stats_text,
            ha='center', fontsize=10,
            family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        # Save
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Preview saved: {output_path}")
    
    def _draw_polygon(
        self,
        ax: plt.Axes,
        polygon: List[List[float]],
        color: Tuple[float, float, float, float],
        index: int
    ) -> None:
        """
        Draw a single polygon on axes.
        
        Args:
            ax: Matplotlib axes
            polygon: Polygon vertices [[x, y], ...]
            color: RGBA color tuple
            index: Polygon index for labeling
        """
        # Convert to numpy array
        points = np.array(polygon)
        
        # Close the polygon
        points_closed = np.vstack([points, points[0]])
        
        # Draw polygon outline
        ax.plot(
            points_closed[:, 0],
            points_closed[:, 1],
            color=color,
            linewidth=self.line_width,
            alpha=0.8
        )
        
        # Draw vertices
        if self.show_vertices:
            ax.scatter(
                points[:, 0],
                points[:, 1],
                color=color,
                s=30,
                alpha=0.9,
                zorder=5,
                edgecolors='white',
                linewidth=0.5
            )
        
        # Draw labels
        if self.show_labels:
            # Polygon label at centroid
            centroid_x = np.mean(points[:, 0])
            centroid_y = np.mean(points[:, 1])
            ax.text(
                centroid_x, centroid_y,
                str(index),
                color='white',
                fontsize=8,
                ha='center',
                va='center',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.7)
            )
    
    def generate_simple_overlay(
        self,
        sprite_path: str,
        polygons: List[List[List[float]]],
        output_path: str,
        dpi: int = 150
    ) -> None:
        """
        Generate simple overlay (single image, no side-by-side).
        
        Args:
            sprite_path: Path to original sprite PNG
            polygons: Collision polygons data
            output_path: Output path for preview image
            dpi: Image resolution
        """
        logger.info(f"Generating simple overlay for {sprite_path}")
        
        # Load sprite
        sprite = Image.open(sprite_path)
        if sprite.mode != 'RGBA':
            sprite = sprite.convert('RGBA')
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # Show sprite with transparency
        ax.imshow(sprite, alpha=0.6)
        
        # Draw polygons
        colors = plt.cm.rainbow(np.linspace(0, 1, len(polygons)))
        
        for i, (polygon, color) in enumerate(zip(polygons, colors)):
            self._draw_polygon(ax, polygon, color, i)
        
        ax.set_title(
            f'Collision Polygons ({len(polygons)} shapes)',
            fontsize=14,
            fontweight='bold'
        )
        ax.axis('off')
        
        plt.tight_layout()
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Simple overlay saved: {output_path}")


def create_preview(
    sprite_path: str,
    polygons: List[List[List[float]]],
    output_path: str,
    simple: bool = False,
    dpi: int = 150
) -> None:
    """
    Convenience function to create preview image.
    
    Args:
        sprite_path: Path to sprite PNG
        polygons: Collision polygon data
        output_path: Output preview path
        simple: Use simple overlay instead of side-by-side
        dpi: Image resolution
    """
    generator = PreviewGenerator()
    
    if simple:
        generator.generate_simple_overlay(sprite_path, polygons, output_path, dpi)
    else:
        generator.generate_preview(sprite_path, polygons, output_path, dpi)
