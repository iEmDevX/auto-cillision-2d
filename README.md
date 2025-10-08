# Python 2D Sprite Collision Polygon Generator

🎮 Automated tool for generating collision polygon mappings from PNG sprite images using **Ear Clipping Triangulation** (Godot-compatible).

## Overview

This tool analyzes PNG sprite images with alpha transparency and automatically generates optimized collision triangles using the **ear clipping algorithm** (same as Godot). Perfect for game development, physics engines, and 2D sprite collision detection with guaranteed boundary preservation.

### Features

- ✅ **Ear Clipping Triangulation** - Same algorithm as Godot engine
- ✅ **Boundary Preservation** - Triangles never extend outside polygon edges
- ✅ Automatic collision polygon generation from PNG sprites
- ✅ Support for complex shapes with multiple disconnected regions
- ✅ Visual preview generation for verification
- ✅ Batch processing for multiple sprites
- ✅ JSON output compatible with Godot and other game engines
- ✅ Sub-pixel precision for accurate collision detection

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd py_auto_cillision_2d
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

1. **Place your PNG sprites in the `input/` folder**

2. **Run the collision generator:**

```bash
python -m src.cli input/your_sprite.png
```

3. **Check the output:**
   - JSON file: `output/json/your_sprite.json`
   - Preview image: `output/preview/your_sprite.png`

### Batch Processing

Process all sprites in the input folder:

```bash
python -m src.cli input/
```

### Advanced Options

```bash
python -m src.cli input/ \
  --output-json output/json/ \
  --output-preview output/preview/ \
  --alpha-threshold 100 \
  --epsilon 2.5
```

**Parameters:**
- `--alpha-threshold`: Alpha channel threshold (0-255, default: 128)
- `--epsilon`: Douglas-Peucker simplification tolerance (default: 2.0)
- Smaller epsilon = more detail, more triangles
- Larger epsilon = simpler shapes, fewer triangles

## Output Format

### JSON Structure

The output is a pure array of triangulated polygons, where each polygon is an array of `[x, y]` coordinates:

```json
[
  [[139.0, 1.0], [163.0, 5.0], [169.0, 21.0]],
  [[67.0, 85.0], [49.0, 144.0], [49.0, 152.0]],
  [[39.0, 155.0], [32.0, 162.0], [20.0, 189.0]]
]
```

**Key specifications:**
- Top-level: Array of triangles
- Each triangle: Array of 3 [x, y] coordinate pairs
- Coordinate system: Pixel coordinates from top-left (0,0)
- Triangulation: Ear clipping algorithm (Godot-compatible)
- Boundary safe: Triangles never extend outside polygon boundaries
- No metadata: Pure coordinate data only

See `assets/examples/1.json` for reference (23 triangles for star shape).

## Project Structure

```
py_auto_cillision_2d/
├── src/
│   ├── core/                  # Core processing modules
│   │   ├── image_processor.py    # PNG loading, contour detection
│   │   ├── polygon_simplifier.py # Douglas-Peucker algorithm
│   │   ├── triangulator.py       # Ear clipping triangulation
│   │   ├── collision_mapper.py   # Main pipeline
│   │   └── preview_generator.py  # Visualization
│   ├── geometry/              # 2D geometric utilities
│   │   └── vector2d.py
│   ├── utils/                 # Helper functions
│   │   └── json_writer.py
│   └── cli.py                 # Command-line interface
│   └── polygon.py
├── utils/                  # Helper functions
│   ├── __init__.py
│   ├── image_utils.py
│   └── json_writer.py
├── input/                  # Source PNG sprites
├── output/                 # Generated files
│   ├── json/              # Collision JSON files
│   └── preview/           # Preview images
├── example/               # Reference examples
│   ├── base.png
├── input/                 # Input PNG sprites
├── output/                # Generated output
│   ├── json/             # Collision JSON files
│   └── preview/          # Preview images
├── assets/examples/       # Reference examples
│   └── 1.json
├── tests/                 # Unit tests
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Algorithm Pipeline

1. **Load PNG** → Extract RGBA channels using Pillow/OpenCV
2. **Alpha Masking** → Threshold alpha channel (default: α > 128 = opaque)
3. **Contour Detection** → `cv2.findContours()` to find sprite boundaries
4. **Polygon Simplification** → Douglas-Peucker algorithm (`cv2.approxPolyDP()`)
5. **Ear Clipping Triangulation** → Convert polygon to triangles (Godot algorithm)
6. **JSON Export** → Write pure coordinate array
7. **Preview Generation** → Overlay triangles on original sprite

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_polygon_simplifier.py -v
```

### Code Formatting

```bash
# Format code with black
black src/ geometry/ utils/ tests/

# Check with flake8
flake8 src/ geometry/ utils/

# Type checking with mypy
mypy src/
```

### Adding New Features

1. Create a new branch
2. Implement your feature with tests
3. Run tests and code quality checks
4. Submit a pull request

## Dependencies

- **opencv-python** (≥4.8.0) - Image processing, contour detection
- **numpy** (≥1.24.0) - Array operations
- **Pillow** (≥10.0.0) - PNG loading with alpha support
- **matplotlib** (≥3.7.0) - Preview image generation
- **earcut** (≥1.1.5) - Ear clipping triangulation (Godot-compatible)
- **shapely** (≥2.0.0) - Polygon geometric operations
- **scipy** (≥1.10.0) - Scientific computing utilities
- **pytest** (≥7.4.0) - Testing framework

## Examples

Check the `assets/examples/` folder:
- `1.json` - Generated collision triangles (23 triangles for star shape)

Example output for a star sprite with epsilon=2.5:
- **Input**: 268x238 PNG sprite
- **Output**: 23 triangles, 69 total vertices
- **Algorithm**: Ear clipping (Godot-compatible)

## Performance

- Process 100 sprites (64x64) in <10 seconds
- Support sprites up to 2048x2048 pixels
- Ear clipping ensures triangles stay within boundaries
- No triangle overflow beyond polygon edges

## Troubleshooting

### Common Issues

**Issue**: "No contours found"
- **Solution**: Check alpha threshold, your sprite might be fully transparent

**Issue**: "Triangles extending outside polygon"
- **Solution**: This should not happen with ear clipping. If it does, please report as bug.

**Issue**: "Too many/few triangles"
- **Solution**: Adjust epsilon parameter (smaller = more detail, larger = simpler shapes)

**Issue**: "Preview image doesn't match sprite"
- **Solution**: Check coordinate system, verify polygon winding order

## Algorithm Compatibility

This tool uses the **ear clipping triangulation algorithm**, which is the same algorithm used by:
- ✅ Godot Engine (`Geometry2D.triangulate_polygon()`)
- ✅ Most 2D physics engines
- ✅ Game frameworks requiring triangulated collision shapes

The triangulation ensures:
- All triangles stay within polygon boundaries
- No self-intersecting triangles
- Counter-clockwise vertex ordering
- Optimal triangle count for physics simulation

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## Contact

For questions or issues, please open a GitHub issue.

---

**Made with ❤️ for game developers**
