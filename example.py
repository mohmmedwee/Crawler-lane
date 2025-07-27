#!/usr/bin/env python3
"""
Example usage of the Web Crawler
"""

import json
from crawler import WebCrawler


def main():
    # Initialize the crawler
    crawler = WebCrawler()
    
    # Example 1: Crawl Perplexity.ai (JavaScript-heavy site)
    print("=" * 60)
    print("Example 1: Crawling Perplexity.ai")
    print("=" * 60)
    
    result = crawler.crawl_website("https://www.perplexity.ai/", use_selenium=True)
    
    if result['success']:
        print(f"✅ Successfully crawled: {result['url']}")
        print(f"📄 Title: {result['title']}")
        print(f"📝 Description: {result['description'][:100]}...")
        print(f"🔗 Method: {result['method']}")
        print(f"📊 Links found: {len(result['links'])}")
        print(f"🖼️ Images found: {len(result['images'])}")
        print(f"📄 Content preview: {result['text_content'][:200]}...")
    else:
        print(f"❌ Failed to crawl: {result['error']}")
    
    print("\n" + "=" * 60)
    print("Example 2: Crawl a simple static site")
    print("=" * 60)
    
    # Example 2: Crawl a simple static site
    result2 = crawler.crawl_website("https://httpbin.org/html")
    
    if result2['success']:
        print(f"✅ Successfully crawled: {result2['url']}")
        print(f"📄 Title: {result2['title']}")
        print(f"🔗 Method: {result2['method']}")
        print(f"📊 Status Code: {result2['status_code']}")
    else:
        print(f"❌ Failed to crawl: {result2['error']}")
    
    print("\n" + "=" * 60)
    print("Example 3: Extract specific content using CSS selectors")
    print("=" * 60)
    
    # Example 3: Extract specific content
    selectors = {
        "headings": "h1, h2, h3",
        "paragraphs": "p",
        "links": "a",
        "buttons": "button"
    }
    
    result3 = crawler.extract_specific_content("https://httpbin.org/html", selectors)
    
    if result3['success']:
        print(f"✅ Successfully extracted content from: {result3['url']}")
        for key, value in result3['extracted_data'].items():
            if isinstance(value, list):
                print(f"📋 {key}: {len(value)} items found")
                if value:
                    print(f"   Sample: {value[0][:100]}...")
            else:
                print(f"📋 {key}: {value}")
    else:
        print(f"❌ Failed to extract content: {result3['error']}")
    
    print("\n" + "=" * 60)
    print("Example 4: Save results to JSON file")
    print("=" * 60)
    
    # Example 4: Save results to file
    result4 = crawler.crawl_website("https://httpbin.org/json")
    
    if result4['success']:
        with open('crawl_results.json', 'w', encoding='utf-8') as f:
            json.dump(result4, f, indent=2, ensure_ascii=False)
        print("✅ Results saved to crawl_results.json")
    else:
        print(f"❌ Failed to crawl: {result4['error']}")


if __name__ == "__main__":
    main() 