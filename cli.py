#!/usr/bin/env python3
"""
Command-line interface for the Web Crawler
"""

import argparse
import json
import sys
from crawler import WebCrawler


def main():
    parser = argparse.ArgumentParser(
        description="Web Crawler - Extract content from websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py https://www.perplexity.ai/
  python cli.py https://www.perplexity.ai/ --selenium
  python cli.py https://www.perplexity.ai/ --output result.json
  python cli.py https://www.perplexity.ai/ --selectors '{"title": "h1", "content": ".main-content"}'
        """
    )
    
    parser.add_argument('url', help='URL of the website to crawl')
    parser.add_argument('--selenium', action='store_true', 
                       help='Use Selenium for JavaScript-heavy sites')
    parser.add_argument('--output', '-o', 
                       help='Output file to save results (JSON format)')
    parser.add_argument('--selectors', '-s', 
                       help='Custom CSS selectors in JSON format')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty print the output')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize crawler
    crawler = WebCrawler()
    
    if args.verbose:
        print(f"Crawling: {args.url}")
        print(f"Using Selenium: {args.selenium}")
        if args.selectors:
            print(f"Custom selectors: {args.selectors}")
        print("-" * 50)
    
    try:
        # Parse custom selectors if provided
        selectors = None
        if args.selectors:
            try:
                selectors = json.loads(args.selectors)
            except json.JSONDecodeError as e:
                print(f"Error parsing selectors: {e}")
                sys.exit(1)
        
        # Crawl the website
        if selectors:
            result = crawler.extract_specific_content(args.url, selectors)
        else:
            result = crawler.crawl_website(args.url, use_selenium=args.selenium)
        
        # Format output
        if args.pretty:
            output_json = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output_json = json.dumps(result, ensure_ascii=False)
        
        # Save to file or print to stdout
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"Results saved to: {args.output}")
        else:
            print(output_json)
        
        # Exit with error code if crawling failed
        if not result.get('success', False):
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 