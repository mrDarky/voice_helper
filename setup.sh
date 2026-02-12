#!/bin/bash
# Setup script for Voice Helper Application

echo "Voice Helper - Setup Script"
echo "============================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check for required system packages
echo ""
echo "Checking system dependencies..."

# Check for portaudio
if command -v pkg-config &> /dev/null; then
    if pkg-config --exists portaudio-2.0; then
        echo "✓ PortAudio found"
    else
        echo "✗ PortAudio not found"
        echo "  Install with: sudo apt-get install portaudio19-dev (Ubuntu/Debian)"
        echo "               brew install portaudio (macOS)"
    fi
fi

# Check for ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg found"
else
    echo "✗ FFmpeg not found"
    echo "  Install with: sudo apt-get install ffmpeg (Ubuntu/Debian)"
    echo "               brew install ffmpeg (macOS)"
fi

# Check for xclip (Linux only, optional but recommended)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v xclip &> /dev/null; then
        echo "✓ xclip found"
    else
        echo "⚠ xclip not found (optional, but recommended for clipboard support)"
        echo "  Install with: sudo apt-get install xclip (Ubuntu/Debian)"
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

echo ""
echo "============================"
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: python main.py"
echo ""
echo "Note: First time running may download Whisper models (can be large)"
