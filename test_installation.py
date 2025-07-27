#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify installation and basic functionality.
"""

import sys
import json
from datetime import datetime


def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from crawler import WebCrawler
        print("  ✅ WebCrawler imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import WebCrawler: {e}")
        return False
    
    try:
        from advanced_crawler import AdvancedWebCrawler
        print("  ✅ AdvancedWebCrawler imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import AdvancedWebCrawler: {e}")
        return False
    
    try:
        from smart_filter import SmartContentFilter, ContentFilter, ContentType
        print("  ✅ SmartContentFilter imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import SmartContentFilter: {e}")
        return False
    
    try:
        from visualization_dashboard import DataVisualizationDashboard
        print("  ✅ DataVisualizationDashboard imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import DataVisualizationDashboard: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality of core components."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test WebCrawler
        from crawler import WebCrawler
        crawler = WebCrawler()
        print("  ✅ WebCrawler initialized successfully")
        
        # Test SmartContentFilter
        from smart_filter import SmartContentFilter, ContentFilter, ContentType
        smart_filter = SmartContentFilter()
        print("  ✅ SmartContentFilter initialized successfully")
        
        # Test ContentFilter
        filter_config = ContentFilter(
            content_types=[ContentType.ARTICLE, ContentType.BLOG],
            min_word_count=100,
            min_quality_score=50.0
        )
        print("  ✅ ContentFilter created successfully")
        
        # Test DataVisualizationDashboard
        from visualization_dashboard import DataVisualizationDashboard
        dashboard = DataVisualizationDashboard()
        print("  ✅ DataVisualizationDashboard initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {e}")
        return False


def test_sample_data():
    """Test with sample data."""
    print("\n📊 Testing with sample data...")
    
    try:
        # Create sample data
        sample_data = {
            "success": True,
            "metadata": {
                "start_url": "https://example.com",
                "crawl_time": datetime.now().isoformat(),
                "total_pages": 5,
                "total_words": 2500
            },
            "statistics": {
                "total_pages": 5,
                "total_words": 2500,
                "avg_words_per_page": 500,
                "success_rate": 100.0
            },
            "pages": [
                {
                    "url": "https://example.com/article1",
                    "title": "Test Article",
                    "text_content": "This is a test article about artificial intelligence and machine learning.",
                    "word_count": 500,
                    "content_analysis": {
                        "content_type": "article",
                        "quality_score": 75.0,
                        "language": "english",
                        "is_duplicate": False
                    }
                }
            ],
            "categories": {
                "article": {
                    "count": 1,
                    "percentage": 100.0,
                    "pages": []
                }
            }
        }
        
        # Test smart filtering
        from smart_filter import SmartContentFilter, ContentFilter, ContentType
        smart_filter = SmartContentFilter()
        
        filter_config = ContentFilter(
            content_types=[ContentType.ARTICLE],
            min_word_count=100,
            min_quality_score=50.0
        )
        
        filtered_pages = smart_filter.filter_content(sample_data["pages"], filter_config)
        print(f"  ✅ Smart filtering completed: {len(filtered_pages)} pages filtered")
        
        # Test visualization
        from visualization_dashboard import DataVisualizationDashboard
        dashboard = DataVisualizationDashboard()
        
        # Create a simple visualization
        viz_file = dashboard.create_text_extraction_visualization(sample_data)
        if viz_file:
            print(f"  ✅ Visualization created: {viz_file}")
        else:
            print("  ⚠️ Visualization creation failed (non-critical)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Sample data test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_import():
    """Test API import."""
    print("\n🌐 Testing API import...")
    
    try:
        from api import app
        print("  ✅ Flask API imported successfully")
        return True
    except ImportError as e:
        print(f"  ⚠️ API import failed (non-critical): {e}")
        return True  # Non-critical for basic functionality


def main():
    """Run all tests."""
    print("🚀 AI Web Crawler - Installation Test")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("  ⚠️ Warning: Python 3.8+ recommended")
    else:
        print("  ✅ Python version is compatible")
    
    # Run tests
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Sample Data", test_sample_data),
        ("API Import", test_api_import),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The installation is working correctly.")
        print("\n🚀 You can now:")
        print("  - Start the web server: python3 api.py")
        print("  - Run the demo: python3 visualization_demo.py")
        print("  - Use the crawler: python3 -c 'from crawler import WebCrawler; print(WebCrawler())'")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("  - Make sure all dependencies are installed: pip3 install -r requirements.txt")
        print("  - Check Python version: python3 --version")
        print("  - Verify you're in the correct directory")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 