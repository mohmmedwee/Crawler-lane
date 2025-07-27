#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Content Filtering CLI Tool
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from smart_filter import SmartContentFilter, ContentFilter, ContentType, ContentQuality


def main():
    parser = argparse.ArgumentParser(
        description="Smart Content Filtering - Filter and categorize crawled content intelligently",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python smart_filter_cli.py crawl_results.json --content-types article,blog --min-words 200
  python smart_filter_cli.py crawl_results.json --keywords "AI,technology" --quality-score 70
  python smart_filter_cli.py crawl_results.json --exclude-keywords "spam,clickbait" --output filtered.json
  python smart_filter_cli.py crawl_results.json --language english --sentiment positive
  python smart_filter_cli.py crawl_results.json --categorize-only --output categories.json
        """
    )
    
    parser.add_argument('input_file', help='Input JSON file with crawled data')
    parser.add_argument('--output', '-o', help='Output file for filtered results (JSON format)')
    parser.add_argument('--content-types', help='Comma-separated content types to include (article,blog,news,product,review,about,contact,faq,documentation)')
    parser.add_argument('--min-words', type=int, default=0, help='Minimum word count (default: 0)')
    parser.add_argument('--max-words', type=int, help='Maximum word count')
    parser.add_argument('--quality-score', type=float, default=0.0, help='Minimum quality score (0-100, default: 0)')
    parser.add_argument('--keywords', help='Comma-separated keywords that must be present')
    parser.add_argument('--exclude-keywords', help='Comma-separated keywords to exclude')
    parser.add_argument('--url-patterns', help='Comma-separated URL patterns to include (regex)')
    parser.add_argument('--exclude-url-patterns', help='Comma-separated URL patterns to exclude (regex)')
    parser.add_argument('--min-links', type=int, default=0, help='Minimum number of links (default: 0)')
    parser.add_argument('--max-links', type=int, help='Maximum number of links')
    parser.add_argument('--min-images', type=int, default=0, help='Minimum number of images (default: 0)')
    parser.add_argument('--max-images', type=int, help='Maximum number of images')
    parser.add_argument('--language', help='Filter by language (english, spanish, french)')
    parser.add_argument('--sentiment', choices=['positive', 'negative', 'neutral'], help='Filter by sentiment')
    parser.add_argument('--duplicate-threshold', type=float, default=0.8, help='Duplicate detection threshold (0-1, default: 0.8)')
    parser.add_argument('--date-from', help='Filter content from this date (YYYY-MM-DD)')
    parser.add_argument('--date-to', help='Filter content to this date (YYYY-MM-DD)')
    parser.add_argument('--categorize-only', action='store_true', help='Only categorize content without filtering')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--pretty', action='store_true', help='Pretty print the output')
    parser.add_argument('--summary-only', action='store_true', help='Show only filtering summary')
    
    args = parser.parse_args()
    
    print("🔍 Smart Content Filtering")
    print("=" * 50)
    
    # Load input data
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading input file: {e}")
        sys.exit(1)
    
    # Extract pages from data
    if 'pages' in data:
        pages = data['pages']
    else:
        pages = data if isinstance(data, list) else []
    
    if not pages:
        print("❌ No pages found in input data")
        sys.exit(1)
    
    print(f"📄 Loaded {len(pages)} pages from {args.input_file}")
    
    # Initialize smart filter
    smart_filter = SmartContentFilter()
    
    if args.categorize_only:
        # Only categorize content
        print("\n📂 Categorizing content...")
        categories = smart_filter.categorize_content(pages)
        
        # Prepare output
        output_data = {
            'categorization': {
                'total_pages': len(pages),
                'categories': {}
            }
        }
        
        for content_type, category_pages in categories.items():
            output_data['categorization']['categories'][content_type.value] = {
                'count': len(category_pages),
                'percentage': (len(category_pages) / len(pages)) * 100,
                'pages': category_pages
            }
        
        # Display results
        print("\n📊 Content Categories:")
        print("-" * 30)
        for content_type, category_data in output_data['categorization']['categories'].items():
            print(f"  {content_type}: {category_data['count']} pages ({category_data['percentage']:.1f}%)")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Categorization results saved to: {args.output}")
        
        return
    
    # Parse content types
    content_types = None
    if args.content_types:
        content_types = []
        for ct_str in args.content_types.split(','):
            ct_str = ct_str.strip().upper()
            try:
                content_types.append(ContentType[ct_str])
            except KeyError:
                print(f"⚠️ Warning: Unknown content type '{ct_str}', skipping")
    
    # Parse keywords
    keywords = args.keywords.split(',') if args.keywords else None
    exclude_keywords = args.exclude_keywords.split(',') if args.exclude_keywords else None
    
    # Parse URL patterns
    url_patterns = args.url_patterns.split(',') if args.url_patterns else None
    exclude_url_patterns = args.exclude_url_patterns.split(',') if args.exclude_url_patterns else None
    
    # Parse date range
    date_range = None
    if args.date_from or args.date_to:
        try:
            start_date = datetime.strptime(args.date_from, '%Y-%m-%d') if args.date_from else datetime.min
            end_date = datetime.strptime(args.date_to, '%Y-%m-%d') if args.date_to else datetime.max
            date_range = (start_date, end_date)
        except ValueError as e:
            print(f"❌ Error parsing date: {e}")
            sys.exit(1)
    
    # Create filter configuration
    filter_config = ContentFilter(
        content_types=content_types,
        min_word_count=args.min_words,
        max_word_count=args.max_words,
        min_quality_score=args.quality_score,
        date_range=date_range,
        keywords=keywords,
        exclude_keywords=exclude_keywords,
        url_patterns=url_patterns,
        exclude_url_patterns=exclude_url_patterns,
        min_links=args.min_links,
        max_links=args.max_links,
        min_images=args.min_images,
        max_images=args.max_images,
        language=args.language,
        sentiment=args.sentiment,
        duplicate_threshold=args.duplicate_threshold
    )
    
    # Display filter configuration
    print("\n⚙️ Filter Configuration:")
    print("-" * 30)
    if content_types:
        print(f"  Content Types: {[ct.value for ct in content_types]}")
    if args.min_words > 0 or args.max_words:
        word_range = f"{args.min_words}"
        if args.max_words:
            word_range += f" - {args.max_words}"
        print(f"  Word Count: {word_range}")
    if args.quality_score > 0:
        print(f"  Min Quality Score: {args.quality_score}")
    if keywords:
        print(f"  Keywords: {keywords}")
    if exclude_keywords:
        print(f"  Exclude Keywords: {exclude_keywords}")
    if args.language:
        print(f"  Language: {args.language}")
    if args.sentiment:
        print(f"  Sentiment: {args.sentiment}")
    if date_range:
        print(f"  Date Range: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}")
    
    # Apply filtering
    print("\n🔍 Applying filters...")
    start_time = time.time()
    
    filtered_pages = smart_filter.filter_content(pages, filter_config)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Generate report
    report = smart_filter.generate_filter_report(len(pages), len(filtered_pages), filter_config)
    
    # Display results
    print("\n📊 Filtering Results:")
    print("=" * 50)
    print(f"✅ Original pages: {len(pages)}")
    print(f"✅ Filtered pages: {len(filtered_pages)}")
    print(f"❌ Removed pages: {len(pages) - len(filtered_pages)}")
    print(f"📈 Retention rate: {report['filtering_stats']['retention_rate']:.1f}%")
    print(f"⏱️ Processing time: {duration:.2f} seconds")
    
    # Show content analysis if verbose
    if args.verbose and filtered_pages:
        print("\n📋 Content Analysis (Sample):")
        print("-" * 30)
        for i, page in enumerate(filtered_pages[:5]):  # Show first 5 pages
            analysis = page.get('content_analysis', {})
            print(f"  {i+1}. {page.get('title', 'No title')}")
            print(f"     Type: {analysis.get('content_type', 'unknown')}")
            print(f"     Quality: {analysis.get('quality', 'unknown')} ({analysis.get('quality_score', 0):.1f})")
            print(f"     Language: {analysis.get('language', 'unknown')}")
            print(f"     Words: {page.get('word_count', 0)}")
            print()
    
    # Categorize filtered content
    if filtered_pages:
        print("📂 Content Categories (Filtered):")
        print("-" * 40)
        categories = smart_filter.categorize_content(filtered_pages)
        for content_type, category_pages in categories.items():
            percentage = (len(category_pages) / len(filtered_pages)) * 100
            print(f"  {content_type.value}: {len(category_pages)} pages ({percentage:.1f}%)")
    
    # Prepare output data
    output_data = {
        'filtering_report': report,
        'filtered_pages': filtered_pages,
        'categories': {}
    }
    
    if filtered_pages:
        categories = smart_filter.categorize_content(filtered_pages)
        for content_type, category_pages in categories.items():
            output_data['categories'][content_type.value] = {
                'count': len(category_pages),
                'percentage': (len(category_pages) / len(filtered_pages)) * 100,
                'pages': category_pages
            }
    
    # Save results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Filtered results saved to: {args.output}")
    
    # Show summary only if requested
    if args.summary_only:
        print("\n📋 Summary:")
        print(f"  Input: {len(pages)} pages")
        print(f"  Output: {len(filtered_pages)} pages")
        print(f"  Filtered: {len(pages) - len(filtered_pages)} pages")
        print(f"  Retention: {report['filtering_stats']['retention_rate']:.1f}%")
    
    # Pretty print if requested
    if args.pretty and not args.summary_only:
        print("\n" + "=" * 50)
        print("📄 Sample Filtered Content")
        print("=" * 50)
        if filtered_pages:
            sample_page = filtered_pages[0]
            print(json.dumps({
                'url': sample_page.get('url'),
                'title': sample_page.get('title'),
                'word_count': sample_page.get('word_count'),
                'content_analysis': sample_page.get('content_analysis', {}),
                'text_preview': sample_page.get('text_content', '')[:200] + "..."
            }, indent=2, ensure_ascii=False))
    
    print(f"\n🎉 Smart filtering completed successfully!")


if __name__ == '__main__':
    main() 