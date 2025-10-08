"""
Command-line interface for collision polygon generator.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.collision_mapper import CollisionMapper
from src.preview_generator import PreviewGenerator
from utils.json_writer import save_collision_json


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration.
    
    Args:
        verbose: Enable verbose (DEBUG) logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def process_single_file(
    input_file: str,
    output_json: Optional[str] = None,
    output_preview: Optional[str] = None,
    alpha_threshold: int = 128,
    epsilon: float = 2.0,
    max_vertices: int = 8,
    min_area: float = 10.0,
    preview_dpi: int = 150
) -> bool:
    """
    Process a single sprite file.
    
    Args:
        input_file: Path to input PNG file
        output_json: Path to output JSON file (optional)
        output_preview: Path to output preview image (optional)
        alpha_threshold: Alpha channel threshold
        epsilon: Simplification tolerance
        max_vertices: Maximum vertices per polygon
        min_area: Minimum polygon area
        preview_dpi: Preview image DPI
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize mapper
        mapper = CollisionMapper(
            alpha_threshold=alpha_threshold,
            epsilon=epsilon,
            max_vertices=max_vertices,
            min_area=min_area
        )
        
        # Generate collision polygons
        logger.info(f"Processing: {input_file}")
        polygons = mapper.generate_collision_polygons(input_file)
        
        # Determine output paths
        input_path = Path(input_file)
        
        if output_json is None:
            output_json = f"output/json/{input_path.stem}.json"
        
        if output_preview is None:
            output_preview = f"output/preview/{input_path.stem}.png"
        
        # Save JSON
        save_collision_json(polygons, output_json)
        logger.info(f"✓ Saved JSON: {output_json}")
        
        # Generate preview
        preview_gen = PreviewGenerator(show_vertices=True, show_labels=False)
        preview_gen.generate_preview(
            input_file,
            polygons,
            output_preview,
            dpi=preview_dpi
        )
        logger.info(f"✓ Saved preview: {output_preview}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to process {input_file}: {e}", exc_info=True)
        return False


def process_directory(
    input_dir: str,
    output_json_dir: str = "output/json",
    output_preview_dir: str = "output/preview",
    alpha_threshold: int = 128,
    epsilon: float = 2.0,
    max_vertices: int = 8,
    min_area: float = 10.0,
    preview_dpi: int = 150
) -> int:
    """
    Process all PNG files in a directory.
    
    Args:
        input_dir: Input directory path
        output_json_dir: Output directory for JSON files
        output_preview_dir: Output directory for preview images
        alpha_threshold: Alpha channel threshold
        epsilon: Simplification tolerance
        max_vertices: Maximum vertices per polygon
        min_area: Minimum polygon area
        preview_dpi: Preview image DPI
        
    Returns:
        Number of successfully processed files
    """
    logger = logging.getLogger(__name__)
    
    # Find PNG files
    input_path = Path(input_dir)
    png_files = list(input_path.glob("*.png"))
    
    if not png_files:
        logger.warning(f"No PNG files found in {input_dir}")
        return 0
    
    logger.info(f"Found {len(png_files)} PNG file(s) in {input_dir}")
    
    # Process each file
    success_count = 0
    
    for png_file in png_files:
        output_json = Path(output_json_dir) / f"{png_file.stem}.json"
        output_preview = Path(output_preview_dir) / f"{png_file.stem}.png"
        
        if process_single_file(
            str(png_file),
            str(output_json),
            str(output_preview),
            alpha_threshold,
            epsilon,
            max_vertices,
            min_area,
            preview_dpi
        ):
            success_count += 1
    
    logger.info(f"\nProcessing complete: {success_count}/{len(png_files)} successful")
    
    return success_count


def main() -> int:
    """
    Main CLI entry point.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Generate collision polygons from 2D sprite images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  python -m src.cli input/sprite.png
  
  # Process directory
  python -m src.cli input/
  
  # Custom parameters
  python -m src.cli input/sprite.png --alpha-threshold 100 --epsilon 3.0
  
  # Specify output paths
  python -m src.cli input/sprite.png --output-json custom.json --output-preview custom.png
        """
    )
    
    parser.add_argument(
        'input',
        help='Input PNG file or directory'
    )
    
    parser.add_argument(
        '--output-json',
        help='Output JSON file path (for single file mode)'
    )
    
    parser.add_argument(
        '--output-preview',
        help='Output preview image path (for single file mode)'
    )
    
    parser.add_argument(
        '--output-json-dir',
        default='output/json',
        help='Output directory for JSON files (for directory mode, default: output/json)'
    )
    
    parser.add_argument(
        '--output-preview-dir',
        default='output/preview',
        help='Output directory for preview images (for directory mode, default: output/preview)'
    )
    
    parser.add_argument(
        '--alpha-threshold',
        type=int,
        default=128,
        help='Alpha channel threshold 0-255 (default: 128)'
    )
    
    parser.add_argument(
        '--epsilon',
        type=float,
        default=2.0,
        help='Douglas-Peucker simplification epsilon (default: 2.0)'
    )
    
    parser.add_argument(
        '--max-vertices',
        type=int,
        default=8,
        help='Maximum vertices per polygon 3-8 (default: 8)'
    )
    
    parser.add_argument(
        '--min-area',
        type=float,
        default=10.0,
        help='Minimum polygon area in square pixels (default: 10.0)'
    )
    
    parser.add_argument(
        '--preview-dpi',
        type=int,
        default=150,
        help='Preview image DPI (default: 150)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate parameters
    if not 0 <= args.alpha_threshold <= 255:
        logger.error("Alpha threshold must be 0-255")
        return 1
    
    if not 3 <= args.max_vertices <= 8:
        logger.error("Max vertices must be 3-8")
        return 1
    
    if args.epsilon <= 0:
        logger.error("Epsilon must be positive")
        return 1
    
    # Check if input is file or directory
    input_path = Path(args.input)
    
    if not input_path.exists():
        logger.error(f"Input path does not exist: {args.input}")
        return 1
    
    try:
        if input_path.is_file():
            # Single file mode
            success = process_single_file(
                args.input,
                args.output_json,
                args.output_preview,
                args.alpha_threshold,
                args.epsilon,
                args.max_vertices,
                args.min_area,
                args.preview_dpi
            )
            return 0 if success else 1
            
        elif input_path.is_dir():
            # Directory mode
            success_count = process_directory(
                args.input,
                args.output_json_dir,
                args.output_preview_dir,
                args.alpha_threshold,
                args.epsilon,
                args.max_vertices,
                args.min_area,
                args.preview_dpi
            )
            return 0 if success_count > 0 else 1
            
        else:
            logger.error(f"Input is neither file nor directory: {args.input}")
            return 1
            
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
