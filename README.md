# Python 2D Sprite Collision Polygon Generator

🎮 Automated tool for generating collision polygon mappings from PNG sprite images.

## Overview

This tool analyzes PNG sprite images with alpha transparency and automatically generates optimized collision shapes (triangles/polygons with ≤8 vertices per shape). Perfect for game development, physics engines, and 2D sprite collision detection.

### Features

- ✅ Automatic collision polygon generation from PNG sprites
- ✅ Support for complex shapes with multiple disconnected regions
- ✅ Optimized output: 3-8 vertices per polygon
- ✅ Visual preview generation for verification
- ✅ Batch processing for multiple sprites
- ✅ JSON output compatible with game engines
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
  --max-vertices 6 \
  --epsilon 2.5
```

**Parameters:**
- `--alpha-threshold`: Alpha channel threshold (0-255, default: 128)
- `--max-vertices`: Maximum vertices per polygon (3-8, default: 8)
- `--epsilon`: Douglas-Peucker simplification epsilon (default: 2.0)

## Output Format

### JSON Structure

The output is a pure array of polygons, where each polygon is an array of `[x, y]` coordinates:

```json
[
  [[0.0, 272.0], [6.0, 303.0], [10.0, 299.0]],
  [[576.0, 822.0], [575.0, 897.0], [584.0, 1008.0]],
  [[527.0, 581.0], [563.0, 628.0], [575.0, 637.0], [876.0, 946.0]]
]
```

**Key specifications:**
- Top-level: Array of polygons
- Each polygon: Array of [x, y] coordinate pairs
- Coordinate system: Pixel coordinates from top-left (0,0)
- Vertex limit: 3-8 vertices per polygon
- No metadata: Pure coordinate data only

See `example/base.json` and `example/base.png` for reference.

## Project Structure

```
py_auto_cillision_2d/
├── src/                    # Main processing modules
│   ├── __init__.py
│   ├── image_processor.py  # PNG loading, alpha extraction
│   ├── polygon_simplifier.py  # Douglas-Peucker algorithm
│   ├── collision_mapper.py    # Main pipeline
│   ├── preview_generator.py   # Visualization
│   └── cli.py                 # Command-line interface
├── geometry/               # 2D geometric utilities
│   ├── __init__.py
│   ├── vector2d.py
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
│   └── base.json
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
5. **Vertex Reduction** → Ensure each polygon has ≤8 vertices
6. **Triangulation** → Convert complex polygons to triangles if needed
7. **JSON Export** → Write pure coordinate array
8. **Preview Generation** → Overlay polygons on original sprite

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
- **shapely** (≥2.0.0) - Advanced polygon operations
- **pytest** (≥7.4.0) - Testing framework

## Examples

Check the `example/` folder:
- `base.png` - Sample sprite image
- `base.json` - Generated collision polygons (80+ triangles)

## Performance

- Process 100 sprites (64x64) in <10 seconds
- Support sprites up to 2048x2048 pixels
- Optimized vertex count while maintaining ≥95% sprite coverage

## Troubleshooting

### Common Issues

**Issue**: "No contours found"
- **Solution**: Check alpha threshold, your sprite might be fully transparent

**Issue**: "Too many vertices"
- **Solution**: Increase epsilon parameter or enable triangulation

**Issue**: "Preview image doesn't match sprite"
- **Solution**: Check coordinate system, verify polygon winding order

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## Contact

For questions or issues, please open a GitHub issue.

---

**Made with ❤️ for game developers**
