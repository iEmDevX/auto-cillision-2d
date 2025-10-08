"""
Preview image generation with polygon overlays.
"""

from typing import List, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PreviewGenerator:
    """
    Generate preview images showing sprite with collision polygon overlays.
    """
    
    def __init__(
        self,
        show_vertices: bool = True,
        show_labels: bool = False,
        alpha_sprite: float = 0.5
    ) -> None:
        """
        Initialize preview generator.
        
        Args:
            show_vertices: Whether to show vertex points
            show_labels: Whether to show vertex labels
            alpha_sprite: Sprite transparency in overlay (0.0-1.0)
        """
        self.show_vertices = show_vertices
        self.show_labels = show_labels
        self.alpha_sprite = alpha_sprite
    
    def generate_preview(
        self,
        sprite_path: str,
        polygons: List[List[List[float]]],
        output_path: str,
        dpi: int = 150
    ) -> None:
        """
        Generate preview image with polygon overlays.
        
        Args:
            sprite_path: Path to original sprite PNG
            polygons: List of collision polygons
            output_path: Path to save preview image
            dpi: Output image DPI
        """
        logger.info(f"Generating preview: {output_path}")
        
        # Load sprite
        sprite = Image.open(sprite_path)
        width, height = sprite.size
        
        # Create figure with two subplots
        fig, axes = plt.subplots(1, 2, figsize=(16, 10))
        
        # Left: Original sprite
        axes[0].imshow(sprite)
        axes[0].set_title("Original Sprite", fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # Right: Sprite with collision overlay
        axes[1].imshow(sprite, alpha=self.alpha_sprite)
        
        # Draw collision polygons
        colors = plt.cm.rainbow(np.linspace(0, 1, len(polygons)))
        
        for i, (polygon, color) in enumerate(zip(polygons, colors)):
            # Convert to numpy array
            poly_array = np.array(polygon)
            
            # Close polygon by adding first point at end
            poly_closed = np.vstack([poly_array, poly_array[0]])
            
            # Draw polygon edge
            axes[1].plot(
                poly_closed[:, 0],
                poly_closed[:, 1],
                color=color,
                linewidth=2,
                alpha=0.8,
                zorder=10
            )
            
            # Draw vertices
            if self.show_vertices:
                axes[1].scatter(
                    poly_array[:, 0],
                    poly_array[:, 1],
                    color=color,
                    s=30,
                    alpha=0.9,
                    zorder=15,
                    edgecolors='white',
                    linewidths=0.5
                )
            
            # Draw vertex labels
            if self.show_labels:
                for j, (x, y) in enumerate(poly_array):
                    axes[1].text(
                        x, y,
                        str(j),
                        fontsize=8,
                        color='white',
                        ha='center',
                        va='center',
                        bbox=dict(
                            boxstyle='circle',
                            facecolor=color,
                            alpha=0.7,
                            edgecolor='white',
                            linewidth=0.5
                        ),
                        zorder=20
                    )
        
        axes[1].set_title(
            f"Collision Polygons ({len(polygons)} shapes)",
            fontsize=14,
            fontweight='bold'
        )
        axes[1].axis('off')
        
        # Add statistics text
        total_vertices = sum(len(p) for p in polygons)
        avg_vertices = total_vertices / len(polygons) if polygons else 0
        
        # Count vertex distribution
        vertex_counts = {}
        for polygon in polygons:
            count = len(polygon)
            vertex_counts[count] = vertex_counts.get(count, 0) + 1
        
        vertex_dist = ", ".join(
            f"{count}v:{num}" for count, num in sorted(vertex_counts.items())
        )
        
        info_text = (
            f"Sprite: {Path(sprite_path).name}\n"
            f"Size: {width}×{height} px\n"
            f"Polygons: {len(polygons)}\n"
            f"Total vertices: {total_vertices}\n"
            f"Avg vertices/polygon: {avg_vertices:.1f}\n"
            f"Distribution: {vertex_dist}"
        )
        
        fig.text(
            0.5, 0.02,
            info_text,
            ha='center',
            fontsize=10,
            family='monospace',
            bbox=dict(
                boxstyle='round',
                facecolor='wheat',
                alpha=0.8,
                pad=0.8
            )
        )
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        
        # Save
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"Preview saved: {output_path}")
    
    def generate_simple_overlay(
        self,
        sprite_path: str,
        polygons: List[List[List[float]]],
        output_path: str,
        dpi: int = 150
    ) -> None:
        """
        Generate simple single-panel overlay preview.
        
        Args:
            sprite_path: Path to original sprite PNG
            polygons: List of collision polygons
            output_path: Path to save preview image
            dpi: Output image DPI
        """
        # Load sprite
        sprite = Image.open(sprite_path)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Show sprite
        ax.imshow(sprite, alpha=self.alpha_sprite)
        
        # Draw polygons
        colors = plt.cm.rainbow(np.linspace(0, 1, len(polygons)))
        
        for polygon, color in zip(polygons, colors):
            poly_array = np.array(polygon)
            poly_closed = np.vstack([poly_array, poly_array[0]])
            
            ax.plot(
                poly_closed[:, 0],
                poly_closed[:, 1],
                color=color,
                linewidth=2,
                alpha=0.8
            )
            
            if self.show_vertices:
                ax.scatter(
                    poly_array[:, 0],
                    poly_array[:, 1],
                    color=color,
                    s=30,
                    alpha=0.9,
                    edgecolors='white',
                    linewidths=0.5
                )
        
        ax.set_title(
            f"{Path(sprite_path).name} - {len(polygons)} Collision Polygons",
            fontsize=12,
            fontweight='bold'
        )
        ax.axis('off')
        
        # Save
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"Simple overlay saved: {output_path}")


def create_preview(
    sprite_path: str,
    polygons: List[List[List[float]]],
    output_path: str,
    show_vertices: bool = True,
    dpi: int = 150
) -> None:
    """
    Convenience function to create preview image.
    
    Args:
        sprite_path: Path to original sprite PNG
        polygons: List of collision polygons
        output_path: Path to save preview image
        show_vertices: Whether to show vertex points
        dpi: Output image DPI
    """
    generator = PreviewGenerator(show_vertices=show_vertices)
    generator.generate_preview(sprite_path, polygons, output_path, dpi=dpi)
