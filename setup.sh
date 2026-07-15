#!/bin/bash
# Setup script for PythonLearningGame

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo "Virtual environment is active. To run the game:"
echo "  python main.py"
echo ""
echo "To deactivate the virtual environment later:"
echo "  deactivate"
