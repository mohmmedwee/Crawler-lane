#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script for AI Web Crawler
"""

import sys
import os
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('flask', 'flask'),
        ('flask_cors', 'flask_cors'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('plotly', 'plotly'),
        ('wordcloud', 'wordcloud')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} (missing)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip3 install -r requirements.txt")
        return False
    
    return True


def start_web_server():
    """Start the web server."""
    print("\n🚀 Starting AI Web Crawler...")
    
    # We're already in the crawler directory
    print("✅ Running from crawler directory")
    
    try:
        # Import and run the Flask app
        from api import app
        
        print("✅ Web server started successfully!")
        print("🌐 Open your browser and visit: http://localhost:8080")
        print("📊 Use the 'Smart Filtering' tab for AI-focused text extraction")
        print("\nPress Ctrl+C to stop the server")
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=8080, debug=False)
        
    except ImportError as e:
        print(f"❌ Failed to import API: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False


def main():
    """Main startup function."""
    print("🤖 AI Web Crawler - Startup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)
    
    # Start web server
    start_web_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 