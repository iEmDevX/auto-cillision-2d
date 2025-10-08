#!/bin/bash
# Quick Reference - Python Environment Commands
# chmod +x quick_start.sh to make executable

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Python 2D Collision Polygon Generator - Quick Start      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo ""
    echo "Run: source venv/bin/activate"
    echo "or:  source activate.sh"
    echo ""
    exit 1
fi

echo "✅ Virtual environment: ACTIVE"
echo "📍 Python: $(python --version)"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Quick Commands                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

PS3="Select an option: "
options=(
    "Test Environment"
    "Run Demo Visualization"
    "Run Pytest Tests"
    "Show Package Versions"
    "View Example JSON"
    "List Project Structure"
    "Open Documentation"
    "Exit"
)

select opt in "${options[@]}"
do
    case $opt in
        "Test Environment")
            echo ""
            echo "🧪 Running environment test..."
            python test_env.py
            break
            ;;
        "Run Demo Visualization")
            echo ""
            echo "🎨 Running demo visualization..."
            python demo.py
            echo ""
            echo "📁 Output saved to: output/preview/demo_visualization.png"
            break
            ;;
        "Run Pytest Tests")
            echo ""
            echo "🧪 Running pytest tests..."
            pytest tests/ -v
            break
            ;;
        "Show Package Versions")
            echo ""
            echo "📦 Installed packages:"
            pip list | grep -E "(opencv|numpy|Pillow|matplotlib|shapely|pytest|black|flake8|mypy)"
            break
            ;;
        "View Example JSON")
            echo ""
            echo "📄 Example JSON format (first 5 polygons):"
            python -c "import json; data=json.load(open('data/examples/1.json')); print(json.dumps(data[:5], indent=2))"
            echo "..."
            echo ""
            echo "Total polygons: $(python -c "import json; print(len(json.load(open('data/examples/1.json'))))")"
            break
            ;;
        "List Project Structure")
            echo ""
            echo "📁 Project structure:"
            find . -maxdepth 2 -not -path './venv/*' -not -path '*/__pycache__/*' -not -path './.git/*' | head -30
            break
            ;;
        "Open Documentation")
            echo ""
            echo "📚 Documentation files:"
            echo "  1. README.md - Project overview and usage"
            echo "  2. DEVELOPMENT.md - Developer guide"
            echo "  3. TEST_RESULTS.md - Test results summary"
            echo "  4. .github/copilot-instructions.md - AI assistant guide"
            echo ""
            read -p "Open which file? (1-4): " choice
            case $choice in
                1) cat README.md | head -50 ;;
                2) cat DEVELOPMENT.md | head -50 ;;
                3) cat TEST_RESULTS.md ;;
                4) cat .github/copilot-instructions.md | head -50 ;;
                *) echo "Invalid choice" ;;
            esac
            break
            ;;
        "Exit")
            echo ""
            echo "👋 Goodbye!"
            break
            ;;
        *) 
            echo "Invalid option $REPLY"
            ;;
    esac
done

echo ""
