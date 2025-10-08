#!/usr/bin/env python3
"""
Test script to verify Python environment setup
"""

import sys
print("=" * 60)
print("🧪 Testing Python Environment")
print("=" * 60)
print()

# Test Python version
print(f"✅ Python Version: {sys.version}")
print()

# Test imports
print("📦 Testing package imports...")
try:
    import cv2
    print(f"  ✅ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"  ❌ OpenCV: {e}")

try:
    import numpy as np
    print(f"  ✅ NumPy: {np.__version__}")
except ImportError as e:
    print(f"  ❌ NumPy: {e}")

try:
    from PIL import Image
    import PIL
    print(f"  ✅ Pillow: {PIL.__version__}")
except ImportError as e:
    print(f"  ❌ Pillow: {e}")

try:
    import matplotlib
    print(f"  ✅ Matplotlib: {matplotlib.__version__}")
except ImportError as e:
    print(f"  ❌ Matplotlib: {e}")

try:
    import shapely
    print(f"  ✅ Shapely: {shapely.__version__}")
except ImportError as e:
    print(f"  ❌ Shapely: {e}")

try:
    import pytest
    print(f"  ✅ Pytest: {pytest.__version__}")
except ImportError as e:
    print(f"  ❌ Pytest: {e}")

print()

# Test basic NumPy operations
print("🔢 Testing NumPy operations...")
try:
    arr = np.array([[1, 2], [3, 4]])
    print(f"  ✅ Array creation: {arr.shape}")
    print(f"  ✅ Array sum: {arr.sum()}")
except Exception as e:
    print(f"  ❌ NumPy operations failed: {e}")

print()

# Test OpenCV basic functionality
print("🖼️  Testing OpenCV functionality...")
try:
    # Create a simple test image
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    test_img[25:75, 25:75] = [255, 255, 255]
    print(f"  ✅ Image creation: {test_img.shape}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    print(f"  ✅ Color conversion: {gray.shape}")
    
    # Find contours
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"  ✅ Contour detection: {len(contours)} contour(s) found")
except Exception as e:
    print(f"  ❌ OpenCV operations failed: {e}")

print()

# Test Pillow
print("🎨 Testing Pillow functionality...")
try:
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
    print(f"  ✅ Image creation: {img.size}, mode: {img.mode}")
    
    # Test alpha channel
    r, g, b, a = img.split()
    print(f"  ✅ Channel split: {len(img.split())} channels")
except Exception as e:
    print(f"  ❌ Pillow operations failed: {e}")

print()

# Test Shapely
print("🔷 Testing Shapely functionality...")
try:
    from shapely.geometry import Polygon
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    print(f"  ✅ Polygon creation: {poly.area} area")
    print(f"  ✅ Is valid: {poly.is_valid}")
except Exception as e:
    print(f"  ❌ Shapely operations failed: {e}")

print()

# Test example files
print("📁 Testing example files...")
import os
example_dir = "example"
if os.path.exists(f"{example_dir}/base.png"):
    print(f"  ✅ base.png found")
    try:
        img = Image.open(f"{example_dir}/base.png")
        print(f"     Size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"     ⚠️  Could not load: {e}")
else:
    print(f"  ⚠️  base.png not found")

if os.path.exists(f"{example_dir}/base.json"):
    print(f"  ✅ base.json found")
    try:
        import json
        with open(f"{example_dir}/base.json", 'r') as f:
            data = json.load(f)
        print(f"     Polygons: {len(data)}")
        print(f"     First polygon vertices: {len(data[0])}")
    except Exception as e:
        print(f"     ⚠️  Could not load: {e}")
else:
    print(f"  ⚠️  base.json not found")

print()
print("=" * 60)
print("✨ Environment test complete!")
print("=" * 60)
print()
print("Next steps:")
print("  1. Implement modules in src/")
print("  2. Run: python -m src.cli input/your_sprite.png")
print("  3. Run tests: pytest tests/ -v")
print()
