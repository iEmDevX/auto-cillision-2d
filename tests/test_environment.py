"""
Basic tests to verify environment setup
"""

import pytest
import numpy as np
import cv2
from PIL import Image
import json
import os


def test_numpy_basic():
    """Test basic NumPy operations"""
    arr = np.array([[1, 2], [3, 4]])
    assert arr.shape == (2, 2)
    assert arr.sum() == 10


def test_opencv_basic():
    """Test basic OpenCV operations"""
    # Create a simple image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[25:75, 25:75] = [255, 255, 255]
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    assert gray.shape == (100, 100)
    
    # Find contours
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    assert len(contours) == 1


def test_pillow_rgba():
    """Test Pillow RGBA image creation"""
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
    assert img.size == (100, 100)
    assert img.mode == 'RGBA'
    
    # Test channel split
    channels = img.split()
    assert len(channels) == 4


def test_example_files_exist():
    """Test that example files exist"""
    assert os.path.exists('assets/examples/1.png')
    assert os.path.exists('assets/examples/1.json')


def test_example_json_format():
    """Test that example JSON has correct format"""
    with open('assets/examples/1.json', 'r') as f:
        data = json.load(f)
    
    # Should be a list
    assert isinstance(data, list)
    
    # Should have polygons
    assert len(data) > 0
    
    # Each polygon should be a list of coordinate pairs
    for polygon in data:
        assert isinstance(polygon, list)
        assert len(polygon) >= 3  # At least 3 vertices
        assert len(polygon) <= 8  # Max 8 vertices
        
        # Each vertex should be [x, y]
        for vertex in polygon:
            assert isinstance(vertex, list)
            assert len(vertex) == 2
            assert isinstance(vertex[0], (int, float))
            assert isinstance(vertex[1], (int, float))


def test_example_sprite_dimensions():
    """Test example sprite can be loaded"""
    img = Image.open('assets/examples/1.png')
    assert img.mode == 'RGBA'
    assert img.size[0] > 0
    assert img.size[1] > 0


def test_output_directories_exist():
    """Test that output directories exist"""
    assert os.path.exists('output/json')
    assert os.path.exists('output/preview')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
