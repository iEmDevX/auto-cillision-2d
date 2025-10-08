"""
Command-line interface for collision polygon generator.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from src.core.collision_mapper import CollisionMapper
from src.core.preview_generator import create_preview
from src.utils.json_writer import save_collision_json


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging.
    
    Args:
        verbose: Enable debug logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
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
        input_file: Path to input PNG
        output_json: Optional output JSON path
        output_preview: Optional output preview path
        alpha_threshold: Alpha threshold (0-255)
        epsilon: Simplification epsilon
        max_vertices: Maximum vertices per polygon
        min_area: Minimum polygon area
        preview_dpi: Preview image DPI
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Create collision mapper
        mapper = CollisionMapper(
            alpha_threshold=alpha_threshold,
            epsilon=epsilon,
            max_vertices=max_vertices,
            min_area=min_area
        )
        
        # Generate collision polygons
        logger.info(f"Processing: {input_file}")
        polygons = mapper.generate_collision_polygons(input_file)
        
        # Auto-generate output paths if not provided
        input_path = Path(input_file)
        
        if output_json is None:
            output_json = f"output/json/{input_path.stem}.json"
        elif Path(output_json).is_dir():
            # If directory provided, create filename
            output_json = str(Path(output_json) / f"{input_path.stem}.json")
        
        if output_preview is None:
            output_preview = f"output/preview/{input_path.stem}.png"
        elif Path(output_preview).is_dir():
            # If directory provided, create filename
            output_preview = str(Path(output_preview) / f"{input_path.stem}.png")
        
        # Save JSON
        save_collision_json(polygons, output_json)
        logger.info(f"✓ JSON saved: {output_json}")
        
        # Generate preview
        create_preview(input_file, polygons, output_preview, dpi=preview_dpi)
        logger.info(f"✓ Preview saved: {output_preview}")
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"✓ Successfully processed: {input_path.name}")
        print(f"{'='*60}")
        print(f"Polygons generated: {len(polygons)}")
        print(f"Total vertices: {sum(len(p) for p in polygons)}")
        print(f"JSON output: {output_json}")
        print(f"Preview output: {output_preview}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to process {input_file}: {e}", exc_info=True)
        print(f"\n✗ Error processing {input_file}: {e}\n", file=sys.stderr)
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
        alpha_threshold: Alpha threshold (0-255)
        epsilon: Simplification epsilon
        max_vertices: Maximum vertices per polygon
        min_area: Minimum polygon area
        preview_dpi: Preview image DPI
        
    Returns:
        Number of successfully processed files
    """
    logger = logging.getLogger(__name__)
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"✗ Input directory not found: {input_dir}", file=sys.stderr)
        return 0
    
    # Find all PNG files
    png_files = list(input_path.glob("*.png"))
    
    if not png_files:
        print(f"✗ No PNG files found in {input_dir}", file=sys.stderr)
        return 0
    
    print(f"\n{'='*60}")
    print(f"Batch Processing: {len(png_files)} file(s)")
    print(f"{'='*60}\n")
    
    success_count = 0
    
    for png_file in png_files:
        output_json = f"{output_json_dir}/{png_file.stem}.json"
        output_preview = f"{output_preview_dir}/{png_file.stem}.png"
        
        if process_single_file(
            str(png_file),
            output_json=output_json,
            output_preview=output_preview,
            alpha_threshold=alpha_threshold,
            epsilon=epsilon,
            max_vertices=max_vertices,
            min_area=min_area,
            preview_dpi=preview_dpi
        ):
            success_count += 1
    
    # Print batch summary
    print(f"\n{'='*60}")
    print(f"Batch Processing Complete")
    print(f"{'='*60}")
    print(f"Total files: {len(png_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(png_files) - success_count}")
    print(f"{'='*60}\n")
    
    return success_count


def main() -> int:
    """
    Main CLI entry point.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description='Generate collision polygons from 2D sprite images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single sprite
  %(prog)s input/sprite.png
  
  # Process with custom parameters
  %(prog)s input/sprite.png --alpha-threshold 100 --max-vertices 6
  
  # Batch process directory
  %(prog)s input/ --output-json output/json/ --output-preview output/preview/
  
  # Specify output paths
  %(prog)s input/sprite.png --output-json my_collision.json --output-preview preview.png
        """
    )
    
    # Input argument
    parser.add_argument(
        'input',
        help='Input PNG file or directory containing PNG files'
    )
    
    # Output arguments
    parser.add_argument(
        '--output-json',
        help='Output JSON file path (for single file) or directory (for batch)'
    )
    
    parser.add_argument(
        '--output-preview',
        help='Output preview image path (for single file) or directory (for batch)'
    )
    
    # Processing parameters
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
    
    # Logging
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate parameters
    if not 0 <= args.alpha_threshold <= 255:
        print("✗ Alpha threshold must be 0-255", file=sys.stderr)
        return 1
    
    if not 3 <= args.max_vertices <= 8:
        print("✗ Max vertices must be 3-8", file=sys.stderr)
        return 1
    
    if args.epsilon <= 0:
        print("✗ Epsilon must be positive", file=sys.stderr)
        return 1
    
    # Check if input is file or directory
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"✗ Input not found: {args.input}", file=sys.stderr)
        return 1
    
    try:
        if input_path.is_file():
            # Process single file
            success = process_single_file(
                args.input,
                output_json=args.output_json,
                output_preview=args.output_preview,
                alpha_threshold=args.alpha_threshold,
                epsilon=args.epsilon,
                max_vertices=args.max_vertices,
                min_area=args.min_area,
                preview_dpi=args.preview_dpi
            )
            return 0 if success else 1
            
        elif input_path.is_dir():
            # Process directory
            output_json_dir = args.output_json or "output/json"
            output_preview_dir = args.output_preview or "output/preview"
            
            success_count = process_directory(
                args.input,
                output_json_dir=output_json_dir,
                output_preview_dir=output_preview_dir,
                alpha_threshold=args.alpha_threshold,
                epsilon=args.epsilon,
                max_vertices=args.max_vertices,
                min_area=args.min_area,
                preview_dpi=args.preview_dpi
            )
            return 0 if success_count > 0 else 1
            
        else:
            print(f"✗ Invalid input: {args.input}", file=sys.stderr)
            return 1
            
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
