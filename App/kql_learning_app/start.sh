#!/bin/bash

# Must Learn KQL Learning Hub - Startup Script

echo "🔍 Must Learn KQL Learning Hub"
echo "===================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Check if requirements are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "⚙️  Please edit .env and add your Grok API key:"
    echo "   XAI_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit and configure .env..."
fi

echo ""
echo "🚀 Starting Must Learn KQL Learning Hub..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Run the app
streamlit run app.py
