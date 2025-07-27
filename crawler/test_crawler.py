#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Web Crawler
"""

import sys
import json
from crawler import WebCrawler


def test_basic_crawling():
    """Test basic crawling functionality."""
    print("Testing basic crawling...")
    
    crawler = WebCrawler()
    
    # Test with a simple static site
    result = crawler.crawl_website("https://httpbin.org/html")
    
    assert result['success'] == True, "Basic crawling failed: {}".format(result.get('error', 'Unknown error'))
    assert 'title' in result, "Title not found in result"
    assert 'text_content' in result, "Text content not found in result"
    
    print("✅ Basic crawling test passed")


def test_selenium_crawling():
    """Test Selenium crawling functionality."""
    print("Testing Selenium crawling...")
    
    crawler = WebCrawler()
    
    # Test with a simple site using Selenium
    result = crawler.crawl_website("https://httpbin.org/html", use_selenium=True)
    
    assert result['success'] == True, "Selenium crawling failed: {}".format(result.get('error', 'Unknown error'))
    assert result['method'] == 'selenium', "Method should be selenium"
    
    print("✅ Selenium crawling test passed")


def test_custom_selectors():
    """Test custom CSS selector functionality."""
    print("Testing custom selectors...")
    
    crawler = WebCrawler()
    
    selectors = {
        "headings": "h1, h2, h3",
        "paragraphs": "p"
    }
    
    result = crawler.extract_specific_content("https://httpbin.org/html", selectors)
    
    assert result['success'] == True, "Custom selectors failed: {}".format(result.get('error', 'Unknown error'))
    assert 'extracted_data' in result, "Extracted data not found in result"
    
    print("✅ Custom selectors test passed")


def test_error_handling():
    """Test error handling for invalid URLs."""
    print("Testing error handling...")
    
    crawler = WebCrawler()
    
    # Test with invalid URL
    result = crawler.crawl_website("https://invalid-domain-that-does-not-exist-12345.com")
    
    assert result['success'] == False, "Should fail for invalid URL"
    assert 'error' in result, "Error message should be present"
    
    print("✅ Error handling test passed")


def main():
    """Run all tests."""
    print("🧪 Running Web Crawler Tests")
    print("=" * 50)
    
    try:
        test_basic_crawling()
        test_selenium_crawling()
        test_custom_selectors()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("The crawler is working correctly.")
        
    except Exception as e:
        print("\n❌ Test failed: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 