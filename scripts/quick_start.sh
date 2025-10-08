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
    "Process Example Sprite"
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
        "Process Example Sprite")
            echo ""
            echo "🎮 Processing example sprite (input/1.png)..."
            python -m src.cli input/1.png --epsilon 2.5
            echo ""
            echo "📁 Output saved to:"
            echo "   - output/json/1.json"
            echo "   - output/preview/1.png"
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
            pip list | grep -E "(opencv|numpy|Pillow|matplotlib|shapely|pytest|earcut)"
            break
            ;;
        "View Example JSON")
            echo ""
            echo "📄 Example JSON format (first 5 triangles):"
            python -c "import json; data=json.load(open('assets/examples/1.json')); print(json.dumps(data[:5], indent=2))"
            echo "..."
            echo ""
            echo "Total triangles: $(python -c "import json; print(len(json.load(open('assets/examples/1.json'))))")"
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
            echo "  2. docs/DEVELOPMENT.md - Developer guide"
            echo "  3. docs/TEST_RESULTS.md - Test results summary"
            echo "  4. .github/copilot-instructions.md - AI assistant guide"
            echo ""
            read -p "Open which file? (1-4): " choice
            case $choice in
                1) cat README.md | less ;;
                2) cat docs/DEVELOPMENT.md | less ;;
                3) cat docs/TEST_RESULTS.md | less ;;
                4) cat .github/copilot-instructions.md | less ;;
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
