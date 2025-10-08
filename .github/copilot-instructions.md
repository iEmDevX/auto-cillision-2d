# Copilot Instructions - Python 2D Sprite Collision Polygon Generator

## Project Overview
Automated tool for generating collision polygon mappings from PNG sprite images using **Ear Clipping Triangulation** (Godot-compatible). The tool analyzes sprite transparency to create optimized collision triangles and outputs both JSON collision data and visual preview images.

## Core Purpose
**Input**: PNG sprite images with alpha transparency (from `input/` folder)
**Output**: 
1. JSON array of triangulated collision polygons (see `assets/examples/1.json`)
2. Preview image showing original sprite + collision polygon overlay

## Architecture & Core Components

### Project Structure
- `src/core/` - Main processing pipeline modules
  - `image_processor.py` - PNG loading, alpha channel extraction, contour detection
  - `polygon_simplifier.py` - Douglas-Peucker algorithm, vertex reduction
  - `triangulator.py` - **Ear clipping triangulation (Godot-compatible)**
  - `collision_mapper.py` - Main collision generation pipeline with triangulation
  - `preview_generator.py` - Visualization overlay creator
- `src/` - Entry points and utilities
  - `cli.py` - Command-line batch processing interface
- `src/geometry/` - 2D geometric utilities (Vector2D, polygon operations)
- `src/utils/` - Helper functions (image I/O, JSON serialization)
- `input/` - Source PNG sprites for processing
- `output/` - Generated JSON and preview images
  - `json/` - Collision polygon JSON files
  - `preview/` - Visual debug overlays
- `assets/examples/` - Reference examples (1.json)
- `tests/` - Unit tests for polygon algorithms


## JSON Output Format (Critical)

Based on `example/1.json`, the output format is:
```json
[
  [[x1, y1], [x2, y2], [x3, y3]],           // Triangle (3 vertices)
  [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], // Quad (4 vertices)
  [[x1, y1], ..., [x8, y8]]                 // Polygon (up to 8 vertices)
]
```

**Key specifications**:
- **Top-level**: Array of triangles/polygons
- **Each polygon**: Array of [x, y] coordinate pairs
- **Coordinate system**: Pixel coordinates from top-left (0,0), matching PNG dimensions
- **Triangulation**: Uses **ear clipping algorithm** (same as Godot)
- **No overflow**: Triangles guaranteed to stay within polygon boundaries
- **Multiple triangles**: Complex sprites decompose into multiple triangles (e.g., star shape = 23 triangles)
- **Precision**: Float coordinates (e.g., `139.0, 1.0`) for accuracy
- **No metadata**: Pure coordinate data only - no object wrappers, IDs, or type labels

**Example from assets/examples/1.json**:
```json
[
  [[139.0,1.0],[108.0,7.0],[89.0,15.0]],
  [[67.0,85.0],[49.0,144.0],[49.0,152.0]],
  [[39.0,155.0],[32.0,162.0],[20.0,189.0]]
]
```

**Example from base.json**:
```json
[
  [[0.0, 272.0], [6.0, 303.0], [10.0, 299.0]],
  [[576.0, 822.0], [575.0, 897.0], [584.0, 1008.0]],
  [[527.0, 581.0], [563.0, 628.0], [575.0, 637.0], [876.0, 946.0]]
]
```

### Key Design Patterns
- **Batch Processing**: Process entire `input/` folder in one command
- **Ear Clipping Triangulation**: Same algorithm as Godot for consistency
- **Boundary Preservation**: Triangles never extend outside polygon boundaries
- **Visual Validation**: Always generate preview images for manual verification

## Development Guidelines

### Algorithm Pipeline
1. **Load PNG** → Extract RGBA channels using Pillow/OpenCV
2. **Alpha Masking** → Threshold alpha channel (default: α > 128 = opaque)
3. **Contour Detection** → `cv2.findContours()` to find sprite boundaries
4. **Polygon Simplification** → Douglas-Peucker algorithm (`cv2.approxPolyDP()`)
5. **Ear Clipping Triangulation** → Convert polygon to triangles using earcut library
6. **JSON Export** → Write pure coordinate array (no metadata)
7. **Preview Generation** → Overlay polygons on original sprite using matplotlib

### Performance Considerations
- Process 100 sprites (64x64) in <10 seconds
- Support sprites up to 2048x2048 pixels
- Minimize total vertex count while maintaining ≥95% sprite coverage
- Use NumPy arrays for coordinate transformations and batch operations

### Code Conventions
- Use type hints: `def triangulate_polygon(vertices: List[Vector2D]) -> List[List[Vector2D]]`
- **Coordinate system**: Top-left origin (0,0), +X right, +Y down (standard image coordinates)
- **JSON format**: Pure nested arrays - NO objects, NO metadata, NO field names
- **Vertex order**: Counter-clockwise winding for polygon vertices
- **File naming**: `input/sprite.png` → `output/json/sprite.json` + `output/preview/sprite.png`

### Testing Strategy
- Verify JSON output matches exact format: `[[[x,y],[x,y],...],...]`
- Test edge cases: fully transparent, single pixel, line sprites, disconnected regions
- Verify JSON output matches exact format: `[[[x,y],[x,y],...],...]`
- Test edge cases: fully transparent, single pixel, line sprites, disconnected regions
- Validate triangulation: all triangles stay within polygon boundaries
- Check coverage: collision area covers ≥95% of opaque sprite pixels
- Visual validation: preview images must clearly show polygon overlays

### Key Dependencies
- `opencv-python` - Image processing, contour detection (`cv2.findContours`, `cv2.approxPolyDP`)
- `numpy` - Array operations, coordinate transformations
- `Pillow` (PIL) - PNG loading with alpha channel support
- `matplotlib` - Preview image generation with polygon overlays
- `earcut` - Ear clipping triangulation (Godot-compatible)
- `shapely` - Polygon geometric operations
- `scipy` - Scientific computing utilities
- `pytest` - Testing framework

### Common Workflows
```bash
# Process single sprite
python -m src.cli input/sprite.png

# Batch process entire input folder
python -m src.cli input/ --output-json output/json/ --output-preview output/preview/

# Adjust parameters
python -m src.cli input/ --alpha-threshold 100 --epsilon 2.5

# Run tests
pytest tests/ -v

# Check example reference
# Input:  input/1.png
# Output: assets/examples/1.json (23 triangles)
```

## AI Assistant Guidelines

### When working with polygon generation:
1. **JSON format is strict**: Output must be pure nested arrays `[[[x,y],[x,y],...],...]` - NO objects, NO metadata
2. **Triangulation**: Use ear clipping to ensure triangles stay within polygon boundaries
3. **Coordinate precision**: Use float coordinates for accuracy (e.g., `139.0, 1.0`)
4. **Reference example**: Always check `assets/examples/1.json` for format validation

### When implementing image processing:
- Use `cv2.findContours()` with `RETR_EXTERNAL` to find outer boundaries only
- Apply alpha threshold before contour detection (default: α > 128)
- Handle sprites with multiple disconnected regions (create separate polygons for each)
- Simplify contours with Douglas-Peucker before triangulation

### When debugging polygon issues:
- Generate preview images to visually verify polygon placement
- Ensure triangles don't extend outside polygon boundaries (no overflow)
- Verify ear clipping triangulation produces correct results
- Check vertex winding order (should be counter-clockwise)
- Ensure polygons cover ≥95% of opaque sprite area
- Test edge cases: fully transparent images, single-pixel sprites, thin lines

### Performance optimization focus areas:
- Batch process multiple sprites efficiently using multiprocessing
- Use NumPy vectorized operations for coordinate transformations
- Cache contour detection results to avoid redundant processing
- Optimize Douglas-Peucker epsilon parameter for speed vs accuracy balance
- Use earcut for fast, accurate triangulation
