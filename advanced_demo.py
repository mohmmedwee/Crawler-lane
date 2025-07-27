#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Demo for the Advanced Web Crawler
"""

import json
import time
from advanced_crawler import AdvancedWebCrawler


def demo_advanced_crawler():
    """Demonstrate the advanced crawler functionality."""
    print("🌐 Advanced Web Crawler Demo")
    print("=" * 60)
    
    # Initialize advanced crawler with conservative settings
    crawler = AdvancedWebCrawler(max_pages=5, max_depth=2, delay=1.0)
    
    print("\n1️⃣ Testing comprehensive website crawling...")
    print("   Crawling httpbin.org (test site with multiple pages)")
    
    start_time = time.time()
    result = crawler.crawl_website("https://httpbin.org/", use_selenium=False)
    end_time = time.time()
    
    if result.get('success'):
        stats = result['statistics']
        duration = end_time - start_time
        
        print("✅ Success!")
        print(f"   📊 Pages crawled: {stats['total_pages']}")
        print(f"   📝 Total words: {stats['total_words']:,}")
        print(f"   🔗 Total links: {stats['total_links']}")
        print(f"   🖼️ Total images: {stats['total_images']}")
        print(f"   ⏱️ Time taken: {duration:.2f} seconds")
        
        # Show detailed content analysis
        content_summary = result['content_summary']
        print(f"\n2️⃣ Content Analysis:")
        print(f"   📈 Average words per page: {content_summary['average_words_per_page']:.1f}")
        
        if content_summary.get('content_types'):
            print(f"   📄 Content types found:")
            for content_type, count in content_summary['content_types'].items():
                print(f"      • {content_type}: {count}")
        
        # Show sample page data
        if result['pages']:
            sample_page = result['pages'][0]
            print(f"\n3️⃣ Sample Page Analysis:")
            print(f"   🌐 URL: {sample_page['url']}")
            print(f"   📄 Title: {sample_page['title']}")
            print(f"   📝 Word count: {sample_page['word_count']}")
            
            detailed_text = sample_page['detailed_text']
            print(f"   📋 Headings found: {sum(len(headings) for headings in detailed_text['headings'].values())}")
            print(f"   📝 Paragraphs: {len(detailed_text['paragraphs'])}")
            print(f"   📋 Lists: {len(detailed_text['lists'])}")
            print(f"   🖼️ Images: {len(detailed_text['images'])}")
            print(f"   🔗 Links: {len(detailed_text['links'])}")
            print(f"   📊 Tables: {len(detailed_text['tables'])}")
            print(f"   📝 Forms: {len(detailed_text['forms'])}")
            print(f"   🔘 Buttons: {len(detailed_text['buttons'])}")
        
        # Show site structure
        print(f"\n4️⃣ Site Structure:")
        site_structure = result['site_structure']
        print(f"   📁 Directory structure: {len(site_structure)} top-level paths")
        
        # Save comprehensive results
        filename = crawler.save_to_json()
        print(f"\n5️⃣ Results saved to: {filename}")
        
        # Show JSON structure
        print(f"\n6️⃣ JSON Output Structure:")
        print("   📄 The JSON file contains:")
        print("      • metadata: Crawl information and settings")
        print("      • content_summary: Statistical analysis")
        print("      • site_structure: Website directory structure")
        print("      • pages: Detailed data for each crawled page")
        print("      • statistics: Overall crawling statistics")
        
        # Show sample JSON structure
        print(f"\n7️⃣ Sample JSON Structure:")
        sample_structure = {
            "success": True,
            "metadata": {
                "crawl_date": "2024-01-01 12:00:00",
                "domain": "httpbin.org",
                "max_pages": 5,
                "max_depth": 2
            },
            "statistics": {
                "total_pages": stats['total_pages'],
                "total_words": stats['total_words'],
                "total_links": stats['total_links'],
                "total_images": stats['total_images']
            },
            "pages": [
                {
                    "url": "https://httpbin.org/",
                    "title": "Sample Page",
                    "word_count": 150,
                    "text_content": "Sample text content...",
                    "detailed_text": {
                        "headings": {"h1": ["Main Title"], "h2": ["Subtitle"]},
                        "paragraphs": ["Paragraph 1", "Paragraph 2"],
                        "lists": [{"type": "ul", "items": ["Item 1", "Item 2"]}],
                        "links": [{"text": "Link", "href": "/link"}],
                        "images": [{"src": "/image.jpg", "alt": "Image"}],
                        "meta_data": {"description": "Page description"}
                    }
                }
            ]
        }
        
        print(json.dumps(sample_structure, indent=2, ensure_ascii=False))
        
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("🎉 Advanced Demo completed!")
    print("\n💡 Next steps:")
    print("   - Try: python advanced_cli.py https://example.com --max-pages 20")
    print("   - Use: python advanced_cli.py https://example.com --extract-only-text")
    print("   - For large sites: python advanced_cli.py https://example.com --max-pages 100 --delay 2.0")


def demo_text_extraction():
    """Demonstrate text-only extraction."""
    print("\n" + "=" * 60)
    print("📝 Text-Only Extraction Demo")
    print("=" * 60)
    
    # Initialize crawler for text extraction
    crawler = AdvancedWebCrawler(max_pages=3, max_depth=1, delay=1.0)
    
    print("\n🔍 Extracting only text content from httpbin.org...")
    
    result = crawler.crawl_website("https://httpbin.org/", use_selenium=False)
    
    if result.get('success') and result['pages']:
        # Create text-only version
        text_only_data = {
            'metadata': result['metadata'],
            'statistics': result['statistics'],
            'text_content': {}
        }
        
        for page in result['pages']:
            url = page['url']
            text_only_data['text_content'][url] = {
                'title': page['title'],
                'word_count': page['word_count'],
                'full_text': page['text_content'],
                'headings': page['detailed_text']['headings'],
                'paragraphs': page['detailed_text']['paragraphs'],
                'lists': page['detailed_text']['lists']
            }
        
        # Save text-only results
        filename = f"text_only_extraction_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(text_only_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Text extraction completed!")
        print(f"   📄 Pages processed: {len(text_only_data['text_content'])}")
        print(f"   📝 Total words: {result['statistics']['total_words']}")
        print(f"   💾 Saved to: {filename}")
        
        # Show sample text content
        if text_only_data['text_content']:
            first_url = list(text_only_data['text_content'].keys())[0]
            first_page = text_only_data['text_content'][first_url]
            print(f"\n📄 Sample Text Content:")
            print(f"   🌐 URL: {first_url}")
            print(f"   📄 Title: {first_page['title']}")
            print(f"   📝 Word count: {first_page['word_count']}")
            print(f"   📋 Headings: {sum(len(headings) for headings in first_page['headings'].values())}")
            print(f"   📝 Paragraphs: {len(first_page['paragraphs'])}")
            print(f"   📋 Lists: {len(first_page['lists'])}")
            print(f"   📄 Text preview: {first_page['full_text'][:200]}...")


if __name__ == "__main__":
    demo_advanced_crawler()
    demo_text_extraction() 