#!/usr/bin/env python3
"""
Test Templates Script
Verifies that the new template structure is working correctly
"""

import requests
import time

def test_main_interface():
    """Test the main interface template."""
    print("🌐 Testing Main Interface...")
    
    try:
        response = requests.get('http://localhost:8080/')
        if response.status_code == 200:
            content = response.text
            
            # Check for template indicators
            if 'Advanced Web Crawler' in content and 'AI-Powered Text Extraction' in content:
                print("✅ Main interface template loaded correctly")
                
                # Check for external CSS
                if 'href="/static/css/style.css"' in content:
                    print("✅ External CSS link found")
                else:
                    print("⚠️ External CSS link not found")
                
                # Check for JavaScript
                if 'src="/static/js/script.js"' in content:
                    print("✅ External JavaScript link found")
                else:
                    print("⚠️ External JavaScript link not found")
                
                return True
            else:
                print("❌ Main interface template content not found")
                return False
        else:
            print(f"❌ Main interface returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_dashboard():
    """Test the dashboard template."""
    print("\n📊 Testing Dashboard...")
    
    try:
        response = requests.get('http://localhost:8080/dashboard')
        if response.status_code == 200:
            content = response.text
            
            # Check for template indicators
            if 'AI Web Crawler Dashboard' in content and 'Advanced text extraction' in content:
                print("✅ Dashboard template loaded correctly")
                
                # Check for external CSS
                if 'href="/static/css/dashboard.css"' in content:
                    print("✅ Dashboard CSS link found")
                else:
                    print("⚠️ Dashboard CSS link not found")
                
                # Check for JavaScript
                if 'src="/static/js/dashboard.js"' in content:
                    print("✅ Dashboard JavaScript link found")
                else:
                    print("⚠️ Dashboard JavaScript link not found")
                
                # Check for Plotly
                if 'plotly-latest.min.js' in content:
                    print("✅ Plotly.js loaded")
                else:
                    print("⚠️ Plotly.js not found")
                
                return True
            else:
                print("❌ Dashboard template content not found")
                return False
        else:
            print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_static_files():
    """Test static file serving."""
    print("\n📁 Testing Static Files...")
    
    static_files = [
        ('/static/css/style.css', 'Main CSS'),
        ('/static/css/dashboard.css', 'Dashboard CSS'),
        ('/static/js/script.js', 'Main JavaScript'),
        ('/static/js/dashboard.js', 'Dashboard JavaScript')
    ]
    
    all_working = True
    
    for path, name in static_files:
        try:
            response = requests.get(f'http://localhost:8080{path}')
            if response.status_code == 200:
                print(f"✅ {name} served correctly")
            else:
                print(f"❌ {name} returned status code: {response.status_code}")
                all_working = False
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to server for {name}")
            all_working = False
    
    return all_working

def test_api_endpoints():
    """Test API endpoints."""
    print("\n🔌 Testing API Endpoints...")
    
    endpoints = [
        ('/health', 'Health Check'),
        ('/crawl', 'Crawl Endpoint (POST)'),
        ('/advanced-crawl', 'Advanced Crawl Endpoint (POST)'),
        ('/smart-filter-crawl', 'Smart Filter Endpoint (POST)'),
        ('/visualize', 'Visualize Endpoint (POST)')
    ]
    
    all_working = True
    
    # Test health endpoint
    try:
        response = requests.get('http://localhost:8080/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint returned status code: {response.status_code}")
            all_working = False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server for health check")
        all_working = False
    
    # Test POST endpoints with sample data
    sample_data = {
        'url': 'https://example.com',
        'max_pages': 1
    }
    
    for path, name in endpoints[1:]:  # Skip health endpoint
        try:
            response = requests.post(f'http://localhost:8080{path}', json=sample_data)
            if response.status_code in [200, 400]:  # 400 is expected for invalid data
                print(f"✅ {name} responding")
            else:
                print(f"❌ {name} returned unexpected status code: {response.status_code}")
                all_working = False
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to server for {name}")
            all_working = False
    
    return all_working

def main():
    """Main test function."""
    print("🧪 AI Web Crawler - Template Structure Test")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Run all tests
    tests = [
        test_main_interface,
        test_dashboard,
        test_static_files,
        test_api_endpoints
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 30)
    
    test_names = [
        "Main Interface Template",
        "Dashboard Template", 
        "Static Files",
        "API Endpoints"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Template structure is working correctly.")
        print("\n🌐 You can now access:")
        print("   - Main Interface: http://localhost:8080")
        print("   - Dashboard: http://localhost:8080/dashboard")
    else:
        print("⚠️ Some tests failed. Check the server logs for issues.")
    
    return passed == total

if __name__ == "__main__":
    main() 