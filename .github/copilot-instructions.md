# Copilot Instructions - Python 2D Sprite Collision Polygon Generator

## Project Overview
Automated tool for generating collision polygon mappings from PNG sprite images. The tool analyzes sprite transparency to create optimized collision shapes (triangles/polygons with ≤8 vertices) and outputs both JSON collision data and visual preview images.

## Core Purpose
**Input**: PNG sprite images with alpha transparency (from `input/` or `example/` folders)
**Output**: 
1. JSON array of triangle/polygon coordinates (see `example/1.json`)
2. Preview image showing original sprite + collision polygon overlay (see `example/1.png`)

## Architecture & Core Components

### Project Structure
- `src/` - Main processing pipeline modules
  - `image_processor.py` - PNG loading, alpha channel extraction, edge detection
  - `polygon_simplifier.py` - Douglas-Peucker algorithm, vertex reduction
  - `collision_mapper.py` - Main collision generation pipeline
  - `preview_generator.py` - Visualization overlay creator
  - `cli.py` - Command-line batch processing interface
- `geometry/` - 2D geometric utilities (Vector2D, polygon operations)
- `utils/` - Helper functions (image I/O, JSON serialization)
- `input/` - Source PNG sprites for processing
- `output/` - Generated JSON and preview images
  - `json/` - Collision polygon JSON files
  - `preview/` - Visual debug overlays
- `example/` - Reference examples (base.png, base.json)
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
- **Top-level**: Array of polygons
- **Each polygon**: Array of [x, y] coordinate pairs
- **Coordinate system**: Pixel coordinates from top-left (0,0), matching PNG dimensions
- **Vertex limit**: Each polygon can have 3-8 vertices maximum
- **Multiple shapes**: Complex sprites decompose into multiple polygons (e.g., `base.json` has 80+ triangles)
- **Precision**: Float coordinates (e.g., `587.1911764705883`) for sub-pixel accuracy
- **No metadata**: Pure coordinate data only - no object wrappers, IDs, or type labels

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
- **Triangulation Focus**: Prefer triangles (3 vertices) for physics engine compatibility
- **Convex Decomposition**: Split concave shapes into multiple convex polygons
- **Visual Validation**: Always generate preview images for manual verification

## Development Guidelines

### Algorithm Pipeline
1. **Load PNG** → Extract RGBA channels using Pillow/OpenCV
2. **Alpha Masking** → Threshold alpha channel (default: α > 128 = opaque)
3. **Contour Detection** → `cv2.findContours()` to find sprite boundaries
4. **Polygon Simplification** → Douglas-Peucker algorithm (`cv2.approxPolyDP()`)
5. **Vertex Reduction** → Ensure each polygon has ≤8 vertices
6. **Triangulation** → Convert complex polygons to triangles if needed
7. **JSON Export** → Write pure coordinate array (no metadata)
8. **Preview Generation** → Overlay polygons on original sprite using matplotlib

### Performance Considerations
- Process 100 sprites (64x64) in <10 seconds
- Support sprites up to 2048x2048 pixels
- Minimize total vertex count while maintaining ≥95% sprite coverage
- Use NumPy arrays for coordinate transformations and batch operations

### Code Conventions
- Use type hints: `def simplify_polygon(vertices: List[Tuple[float, float]], max_vertices: int) -> List[Tuple[float, float]]`
- **Coordinate system**: Top-left origin (0,0), +X right, +Y down (standard image coordinates)
- **JSON format**: Pure nested arrays - NO objects, NO metadata, NO field names
- **Vertex order**: Counter-clockwise winding for polygon vertices
- **File naming**: `input/sprite.png` → `output/json/sprite.json` + `output/preview/sprite.png`

### Testing Strategy
- Verify JSON output matches exact format: `[[[x,y],[x,y],...],...]`
- Test edge cases: fully transparent, single pixel, line sprites, disconnected regions
- Validate vertex count: all polygons have 3-8 vertices
- Check coverage: collision area covers ≥95% of opaque sprite pixels
- Visual validation: preview images must clearly show polygon overlays

### Key Dependencies
- `opencv-python` - Image processing, contour detection (`cv2.findContours`, `cv2.approxPolyDP`)
- `numpy` - Array operations, coordinate transformations
- `Pillow` (PIL) - PNG loading with alpha channel support
- `matplotlib` - Preview image generation with polygon overlays
- `pytest` - Testing framework

### Common Workflows
```bash
# Process single sprite
python -m src.cli input/sprite.png

# Batch process entire input folder
python -m src.cli input/ --output-json output/json/ --output-preview output/preview/

# Adjust parameters
python -m src.cli input/ --alpha-threshold 100 --max-vertices 6 --epsilon 2.5

# Run tests
pytest tests/ -v

# Check example reference
# Input:  example/1.png
# Output: example/1.json (80+ triangular polygons)
```

## AI Assistant Guidelines

### When working with polygon generation:
1. **JSON format is strict**: Output must be pure nested arrays `[[[x,y],[x,y],...],...]` - NO objects, NO metadata
2. **Vertex limits**: Each polygon MUST have 3-8 vertices. If shape is complex, split into multiple polygons
3. **Coordinate precision**: Use float coordinates for sub-pixel accuracy (e.g., `587.1911764705883`)
4. **Reference example**: Always check `example/1.json` and `example/1.png` for format validation

### When implementing image processing:
- Use `cv2.findContours()` with `RETR_EXTERNAL` to find outer boundaries only
- Apply alpha threshold before contour detection (default: α > 128)
- Handle sprites with multiple disconnected regions (create separate polygons for each)
- Validate that generated polygons don't have self-intersections

### When debugging polygon issues:
- Generate preview images to visually verify polygon placement
- Check vertex winding order (should be counter-clockwise)
- Ensure polygons cover ≥95% of opaque sprite area
- Verify total vertex count is minimized while maintaining accuracy
- Test edge cases: fully transparent images, single-pixel sprites, thin lines

### Performance optimization focus areas:
- Batch process multiple sprites efficiently using multiprocessing
- Use NumPy vectorized operations for coordinate transformations
- Cache contour detection results to avoid redundant processing
- Optimize Douglas-Peucker epsilon parameter for speed vs accuracy balance
