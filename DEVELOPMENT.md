# Development Guide

## Setup Complete! ✅

Your Python environment has been successfully configured with all dependencies.

## Project Structure

```
py_auto_cillision_2d/
├── .github/
│   └── copilot-instructions.md  # AI coding assistant instructions
├── src/                         # Main processing modules (to be implemented)
│   ├── __init__.py
│   ├── image_processor.py       # PNG loading, alpha extraction
│   ├── polygon_simplifier.py    # Douglas-Peucker algorithm
│   ├── collision_mapper.py      # Main pipeline
│   ├── preview_generator.py     # Visualization
│   └── cli.py                   # Command-line interface
├── geometry/                    # 2D geometric utilities
├── utils/                       # Helper functions
├── input/                       # Put your PNG sprites here
├── output/                      # Generated files appear here
│   ├── json/                   # Collision polygon JSON
│   └── preview/                # Preview images
├── example/                     # Reference example
│   ├── base.png                # Sample sprite
│   └── base.json               # Sample collision data
├── tests/                       # Unit tests
├── venv/                        # Virtual environment
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                    # Full documentation

```

## Quick Start

### 1. Activate Environment

```bash
source venv/bin/activate
# or use the helper script
source activate.sh
```

### 2. Start Development

The project is now ready! Here's what you can do:

#### Option A: Implement the modules yourself
Start coding in the `src/`, `geometry/`, and `utils/` folders

#### Option B: Ask AI to generate the implementation
Use the `.github/copilot-instructions.md` to guide AI in generating the code

## Environment Info

- **Python**: 3.9.6
- **Virtual Environment**: `venv/` (activated)
- **Dependencies**: All installed ✅

### Installed Packages:
- opencv-python 4.12.0.88
- numpy 2.0.2
- Pillow 11.3.0
- matplotlib 3.9.4
- shapely 2.0.7
- pytest 8.4.2
- And more...

## Development Commands

```bash
# Activate environment
source venv/bin/activate

# Run tests (once implemented)
pytest tests/ -v

# Code formatting
black src/ geometry/ utils/ tests/

# Type checking
mypy src/

# Code linting
flake8 src/ geometry/ utils/

# Deactivate environment
deactivate
```

## Next Steps

### 1. Implement Core Modules

You need to create the following files in `src/`:

- **image_processor.py** - Load PNG, extract alpha channel, detect contours
- **polygon_simplifier.py** - Douglas-Peucker algorithm, vertex reduction
- **collision_mapper.py** - Main processing pipeline
- **preview_generator.py** - Generate preview images with overlays
- **cli.py** - Command-line interface

### 2. Implement Geometry Utilities

In `geometry/`:
- **vector2d.py** - 2D vector class
- **polygon.py** - Polygon operations

### 3. Implement Utilities

In `utils/`:
- **image_utils.py** - Image I/O helpers
- **json_writer.py** - JSON serialization

### 4. Write Tests

In `tests/`:
- **test_image_processor.py**
- **test_polygon_simplifier.py**
- **test_collision_mapper.py**

## Reference

Check `example/base.json` and `example/base.png` to understand the expected output format.

### JSON Format (Critical!)

```json
[
  [[x1, y1], [x2, y2], [x3, y3]],  // Triangle
  [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]  // Quad
]
```

- Pure nested arrays - NO objects
- Each polygon has 3-8 vertices
- Coordinates are pixel positions from top-left (0,0)
- Float precision for sub-pixel accuracy

## Using AI Copilot

The `.github/copilot-instructions.md` file contains detailed instructions for AI coding assistants. It includes:

- Project architecture and structure
- JSON output format specifications
- Algorithm pipeline details
- Code conventions and best practices
- Performance considerations
- Testing strategies

When working with GitHub Copilot or similar tools, they will automatically read these instructions to provide better suggestions.

## Tips

1. **Start Small**: Implement and test one module at a time
2. **Use Example**: Compare your output with `example/base.json`
3. **Visual Validation**: Always generate preview images to verify
4. **Test Edge Cases**: Transparent images, single pixels, complex shapes
5. **Performance**: Profile with large batches of sprites

## Troubleshooting

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

Make sure you're in the project root and the virtual environment is activated.

### Module Not Found

Install in development mode:
```bash
pip install -e .
```

## Resources

- **OpenCV Docs**: https://docs.opencv.org/
- **NumPy Docs**: https://numpy.org/doc/
- **Shapely Docs**: https://shapely.readthedocs.io/
- **Matplotlib Docs**: https://matplotlib.org/stable/contents.html

---

Happy coding! 🎮✨
