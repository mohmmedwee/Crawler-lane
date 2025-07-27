#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for the Web Crawler
"""

import json
from crawler import WebCrawler


def demo_crawler():
    """Demonstrate the crawler functionality."""
    print("🌐 Web Crawler Demo")
    print("=" * 50)
    
    # Initialize crawler
    crawler = WebCrawler()
    
    # Test 1: Simple static site
    print("\n1️⃣ Testing with a simple static site...")
    result1 = crawler.crawl_website("https://httpbin.org/html")
    
    if result1['success']:
        print("✅ Success!")
        print(f"   Title: {result1.get('title', 'N/A')}")
        print(f"   Method: {result1.get('method', 'N/A')}")
        print(f"   Status: {result1.get('status_code', 'N/A')}")
        print(f"   Content preview: {result1.get('text_content', '')[:100]}...")
    else:
        print(f"❌ Failed: {result1.get('error', 'Unknown error')}")
    
    # Test 2: JSON API
    print("\n2️⃣ Testing with JSON API...")
    result2 = crawler.crawl_website("https://httpbin.org/json")
    
    if result2['success']:
        print("✅ Success!")
        print(f"   Title: {result2.get('title', 'N/A')}")
        print(f"   Method: {result2.get('method', 'N/A')}")
        print(f"   Content preview: {result2.get('text_content', '')[:100]}...")
    else:
        print(f"❌ Failed: {result2.get('error', 'Unknown error')}")
    
    # Test 3: Custom selectors
    print("\n3️⃣ Testing custom CSS selectors...")
    selectors = {
        "headings": "h1, h2, h3",
        "paragraphs": "p",
        "links": "a"
    }
    
    result3 = crawler.extract_specific_content("https://httpbin.org/html", selectors)
    
    if result3['success']:
        print("✅ Success!")
        for key, value in result3['extracted_data'].items():
            if isinstance(value, list):
                print(f"   {key}: {len(value)} items found")
            else:
                print(f"   {key}: {value}")
    else:
        print(f"❌ Failed: {result3.get('error', 'Unknown error')}")
    
    # Test 4: Save results
    print("\n4️⃣ Saving results to file...")
    with open('demo_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'static_site': result1,
            'json_api': result2,
            'custom_selectors': result3
        }, f, indent=2, ensure_ascii=False)
    print("✅ Results saved to demo_results.json")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("\n💡 Next steps:")
    print("   - Try the web interface: python start.py")
    print("   - Use command line: python cli.py https://example.com")
    print("   - For JavaScript sites, use: python cli.py https://example.com --selenium")


if __name__ == "__main__":
    demo_crawler() 