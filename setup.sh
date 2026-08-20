#!/bin/bash
# Setup script for PythonLearningGame

if [ ! -d venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
else
  echo "Virtual environment already exists."
fi

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
