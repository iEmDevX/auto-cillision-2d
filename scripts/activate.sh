#!/bin/bash
# Activation script for py_auto_collision_2d

echo "🚀 Activating Python environment..."
source venv/bin/activate

echo "✅ Environment activated!"
echo ""
echo "Python version: $(python --version)"
echo ""
echo "📦 Key packages installed:"
pip list | grep -E "(opencv|numpy|Pillow|matplotlib|shapely|pytest)" | head -6
echo ""
echo "💡 Quick commands:"
echo "  - Process sprite:  python -m src.cli input/your_sprite.png"
echo "  - Batch process:   python -m src.cli input/"
echo "  - Run tests:       pytest tests/ -v"
echo "  - Deactivate:      deactivate"
echo ""
