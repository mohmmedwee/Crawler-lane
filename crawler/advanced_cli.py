#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced CLI for the Advanced Web Crawler
"""

import argparse
import json
import sys
import time
from advanced_crawler import AdvancedWebCrawler


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Web Crawler - Extract comprehensive content from entire websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_cli.py https://www.perplexity.ai/ --max-pages 50
  python advanced_cli.py https://www.perplexity.ai/ --selenium --output full_site.json
  python advanced_cli.py https://www.perplexity.ai/ --max-pages 100 --delay 2.0 --verbose
  python advanced_cli.py https://www.perplexity.ai/ --extract-only-text --output text_only.json
        """
    )
    
    parser.add_argument('url', help='Starting URL of the website to crawl')
    parser.add_argument('--max-pages', '-m', type=int, default=50,
                       help='Maximum number of pages to crawl (default: 50)')
    parser.add_argument('--max-depth', '-d', type=int, default=3,
                       help='Maximum depth of crawling (default: 3)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--selenium', action='store_true',
                       help='Use Selenium for JavaScript-heavy sites')
    parser.add_argument('--output', '-o',
                       help='Output file to save results (JSON format)')
    parser.add_argument('--extract-only-text', action='store_true',
                       help='Extract only text content (no images, forms, etc.)')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty print the output')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output with detailed logging')
    parser.add_argument('--summary-only', action='store_true',
                       help='Show only summary statistics')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("🌐 Advanced Web Crawler")
    print("=" * 50)
    print(f"Starting URL: {args.url}")
    print(f"Max pages: {args.max_pages}")
    print(f"Max depth: {args.max_depth}")
    print(f"Delay: {args.delay}s")
    print(f"Use Selenium: {args.selenium}")
    print("-" * 50)
    
    # Initialize advanced crawler
    crawler = AdvancedWebCrawler(
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        delay=args.delay
    )
    
    start_time = time.time()
    
    try:
        # Start crawling
        print("🚀 Starting advanced crawl...")
        result = crawler.crawl_website(args.url, use_selenium=args.selenium)
        
        if not result.get('success'):
            print(f"❌ Crawling failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
        
        # Calculate time taken
        end_time = time.time()
        duration = end_time - start_time
        
        # Show summary
        stats = result['statistics']
        print("\n" + "=" * 50)
        print("📊 Crawling Summary")
        print("=" * 50)
        print(f"✅ Successfully crawled: {stats['total_pages']} pages")
        print(f"📝 Total words extracted: {stats['total_words']:,}")
        print(f"🔗 Total links found: {stats['total_links']}")
        print(f"🖼️ Total images found: {stats['total_images']}")
        print(f"⏱️ Time taken: {duration:.2f} seconds")
        print(f"📈 Average words per page: {stats['total_words'] // stats['total_pages'] if stats['total_pages'] > 0 else 0}")
        
        # Show content summary
        content_summary = result['content_summary']
        if content_summary.get('most_common_headings'):
            print(f"\n📋 Most common headings:")
            for heading, count in list(content_summary['most_common_headings'].items())[:5]:
                print(f"   • {heading}: {count} times")
        
        if content_summary.get('content_types'):
            print(f"\n📄 Content types found:")
            for content_type, count in content_summary['content_types'].items():
                print(f"   • {content_type}: {count}")
        
        # Save results
        if args.output:
            filename = args.output
        else:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            domain = result['metadata']['domain']
            filename = f"advanced_crawl_{domain}_{timestamp}.json"
        
        # Filter content if requested
        if args.extract_only_text:
            print("\n🔍 Extracting only text content...")
            filtered_result = {
                'metadata': result['metadata'],
                'statistics': result['statistics'],
                'pages': []
            }
            
            for page in result['pages']:
                filtered_page = {
                    'url': page['url'],
                    'title': page['title'],
                    'word_count': page['word_count'],
                    'text_content': page['text_content'],
                    'detailed_text': {
                        'headings': page['detailed_text']['headings'],
                        'paragraphs': page['detailed_text']['paragraphs'],
                        'lists': page['detailed_text']['lists'],
                        'meta_data': page['detailed_text']['meta_data']
                    }
                }
                filtered_result['pages'].append(filtered_page)
            
            result = filtered_result
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        
        # Show output if requested
        if args.pretty:
            print("\n" + "=" * 50)
            print("📄 Sample Output")
            print("=" * 50)
            if args.summary_only:
                print(json.dumps({
                    'statistics': result['statistics'],
                    'content_summary': result.get('content_summary', {})
                }, indent=2, ensure_ascii=False))
            else:
                # Show first page as sample
                if result['pages']:
                    sample_page = result['pages'][0]
                    print(json.dumps({
                        'url': sample_page['url'],
                        'title': sample_page['title'],
                        'word_count': sample_page['word_count'],
                        'text_preview': sample_page['text_content'][:500] + "..."
                    }, indent=2, ensure_ascii=False))
        
        print(f"\n🎉 Advanced crawling completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Crawling interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during crawling: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 