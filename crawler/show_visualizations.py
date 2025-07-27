#!/usr/bin/env python3
"""
Show Visualizations Demo Script
Demonstrates the visualizations available in the AI Web Crawler API
"""

import requests
import json
import time
import webbrowser
from pathlib import Path

def test_dashboard():
    """Test the dashboard endpoint."""
    print("🌐 Testing Dashboard Endpoint...")
    
    try:
        response = requests.get('http://localhost:8080/dashboard')
        if response.status_code == 200:
            print("✅ Dashboard is accessible!")
            return True
        else:
            print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running.")
        return False

def test_visualize_endpoint():
    """Test the visualize endpoint with sample data."""
    print("\n📊 Testing Visualization Endpoint...")
    
    # Sample crawl data
    sample_data = {
        "urls": [
            "https://example.com/article1",
            "https://example.com/article2",
            "https://example.com/blog1"
        ],
        "pages": [
            {
                "url": "https://example.com/article1",
                "title": "Sample Article 1",
                "content": "This is a sample article about AI and machine learning.",
                "word_count": 150,
                "quality_score": 85,
                "content_type": "Article",
                "language": "en",
                "sentiment": "positive"
            },
            {
                "url": "https://example.com/article2",
                "title": "Sample Article 2",
                "content": "Another sample article about web crawling and data extraction.",
                "word_count": 200,
                "quality_score": 78,
                "content_type": "Article",
                "language": "en",
                "sentiment": "neutral"
            },
            {
                "url": "https://example.com/blog1",
                "title": "Sample Blog Post",
                "content": "A blog post about technology and innovation.",
                "word_count": 120,
                "quality_score": 92,
                "content_type": "Blog",
                "language": "en",
                "sentiment": "positive"
            }
        ]
    }
    
    try:
        response = requests.post(
            'http://localhost:8080/visualize',
            json=sample_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Visualization endpoint working!")
            print(f"📁 Generated files: {result.get('files', [])}")
            return True
        else:
            print(f"❌ Visualization endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server.")
        return False

def open_dashboard():
    """Open the dashboard in the default browser."""
    print("\n🌐 Opening Dashboard in Browser...")
    try:
        webbrowser.open('http://localhost:8080/dashboard')
        print("✅ Dashboard opened in browser!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("📋 Please manually open: http://localhost:8080/dashboard")

def show_available_endpoints():
    """Show all available API endpoints."""
    print("\n📋 Available API Endpoints:")
    print("=" * 50)
    print("🌐 Main Interface:     http://localhost:8080")
    print("📊 Dashboard:          http://localhost:8080/dashboard")
    print("🔍 Health Check:       http://localhost:8080/health")
    print("")
    print("📤 POST Endpoints:")
    print("   /crawl              - Basic web crawling")
    print("   /advanced-crawl     - Advanced crawling with Selenium")
    print("   /smart-filter-crawl - Smart content filtering")
    print("   /visualize          - Generate data visualizations")

def main():
    """Main function to demonstrate visualizations."""
    print("🤖 AI Web Crawler - Visualization Demo")
    print("=" * 50)
    
    # Check if server is running
    if not test_dashboard():
        print("\n💡 To start the server, run:")
        print("   cd /Users/ehabshobaki/Desktop/headless/crawler")
        print("   source venv/bin/activate")
        print("   python api.py")
        return
    
    # Show available endpoints
    show_available_endpoints()
    
    # Test visualization endpoint
    test_visualize_endpoint()
    
    # Open dashboard
    open_dashboard()
    
    print("\n🎉 Visualization Demo Complete!")
    print("📊 Check your browser for the interactive dashboard")
    print("🔍 You can also test the other endpoints using curl or Postman")

if __name__ == "__main__":
    main() 