#!/bin/bash

# AI Web Crawler - Quick Start Script

echo "🤖 AI Web Crawler - Starting Server"
echo "=================================="

# Navigate to the correct directory
cd /Users/ehabshobaki/Desktop/headless/crawler

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if virtual environment is activated
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated successfully"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start the server
echo "🚀 Starting web server..."
echo "📊 Server will be available at:"
echo "   - Main Interface: http://localhost:8080"
echo "   - Dashboard: http://localhost:8080/dashboard"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python start.py 