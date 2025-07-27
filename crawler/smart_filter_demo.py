#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Content Filtering Demo
"""

import json
import time
from smart_filter import SmartContentFilter, ContentFilter, ContentType
from advanced_crawler import AdvancedWebCrawler


def demo_smart_filtering():
    """Demonstrate smart content filtering capabilities."""
    print("🔍 Smart Content Filtering Demo")
    print("=" * 60)
    
    # Initialize smart filter
    smart_filter = SmartContentFilter()
    
    # Create sample pages for demonstration
    sample_pages = [
        {
            'url': 'https://example.com/blog/ai-future',
            'title': 'The Future of Artificial Intelligence',
            'text_content': 'Artificial Intelligence is transforming the way we live and work. Machine learning algorithms are becoming increasingly sophisticated, enabling computers to perform tasks that were once thought impossible. Companies like Google, Microsoft, and OpenAI are leading the charge in developing cutting-edge AI technologies. The future looks bright for AI applications in healthcare, education, and transportation.',
            'word_count': 85,
            'success': True,
            'detailed_text': {
                'headings': {'h1': ['AI Future'], 'h2': ['Technology Trends']},
                'paragraphs': ['AI is amazing...', 'Machine learning is great...'],
                'links': [{'text': 'Learn More', 'href': '/more'}],
                'images': [{'src': '/ai-image.jpg', 'alt': 'AI Technology'}],
                'meta_data': {'description': 'AI technology article', 'date': '2024-01-15'}
            }
        },
        {
            'url': 'https://example.com/product/laptop',
            'title': 'Best Gaming Laptop 2024',
            'text_content': 'Buy the best gaming laptop for 2024. This amazing laptop features the latest graphics card and high-performance processor. Perfect for gaming and professional work. Get it now at a great price!',
            'word_count': 45,
            'success': True,
            'detailed_text': {
                'headings': {'h1': ['Gaming Laptop']},
                'paragraphs': ['Buy now...', 'Great price...'],
                'links': [{'text': 'Buy Now', 'href': '/buy'}],
                'images': [{'src': '/laptop.jpg', 'alt': 'Gaming Laptop'}],
                'meta_data': {'description': 'Gaming laptop product page'}
            }
        },
        {
            'url': 'https://example.com/about-us',
            'title': 'About Our Company',
            'text_content': 'We are a leading technology company dedicated to innovation and excellence. Our team of experts works tirelessly to deliver the best solutions for our customers. Founded in 2010, we have grown to become a trusted partner for businesses worldwide.',
            'word_count': 55,
            'success': True,
            'detailed_text': {
                'headings': {'h1': ['About Us'], 'h2': ['Our Mission']},
                'paragraphs': ['We are a leading company...', 'Our team works tirelessly...'],
                'links': [{'text': 'Contact Us', 'href': '/contact'}],
                'images': [{'src': '/team.jpg', 'alt': 'Our Team'}],
                'meta_data': {'description': 'About our company'}
            }
        },
        {
            'url': 'https://example.com/spam-page',
            'title': 'Click Here for Amazing Deals!',
            'text_content': 'Spam content with clickbait. Buy now! Amazing deals! Don\'t miss out! Limited time offer!',
            'word_count': 15,
            'success': True,
            'detailed_text': {
                'headings': {'h1': ['Amazing Deals']},
                'paragraphs': ['Buy now!', 'Limited time!'],
                'links': [{'text': 'Buy Now', 'href': '/spam'}],
                'images': [],
                'meta_data': {'description': 'Spam content'}
            }
        }
    ]
    
    print(f"📄 Sample pages created: {len(sample_pages)}")
    
    # 1. Content Type Detection
    print("\n1️⃣ Content Type Detection:")
    print("-" * 30)
    for page in sample_pages:
        content_type = smart_filter.detect_content_type(
            page['url'], 
            page['title'], 
            page['text_content'], 
            page['detailed_text'].get('meta_data', {})
        )
        print(f"  {page['title']}: {content_type.value}")
    
    # 2. Content Quality Assessment
    print("\n2️⃣ Content Quality Assessment:")
    print("-" * 30)
    for page in sample_pages:
        quality, score = smart_filter.assess_content_quality(
            page['text_content'], 
            page['detailed_text']
        )
        print(f"  {page['title']}: {quality.value} ({score:.1f}/100)")
    
    # 3. Language Detection
    print("\n3️⃣ Language Detection:")
    print("-" * 30)
    for page in sample_pages:
        language = smart_filter.detect_language(page['text_content'])
        print(f"  {page['title']}: {language}")
    
    # 4. Content Categorization
    print("\n4️⃣ Content Categorization:")
    print("-" * 30)
    categories = smart_filter.categorize_content(sample_pages)
    for content_type, pages in categories.items():
        print(f"  {content_type.value}: {len(pages)} pages")
    
    # 5. Smart Filtering Examples
    print("\n5️⃣ Smart Filtering Examples:")
    print("-" * 30)
    
    # Example 1: Filter for articles and blogs only
    print("\n🔍 Filter 1: Articles and Blogs Only")
    filter1 = ContentFilter(
        content_types=[ContentType.ARTICLE, ContentType.BLOG],
        min_word_count=50
    )
    filtered1 = smart_filter.filter_content(sample_pages, filter1)
    print(f"  Original: {len(sample_pages)} pages")
    print(f"  Filtered: {len(filtered1)} pages")
    for page in filtered1:
        print(f"    - {page['title']}")
    
    # Example 2: Filter for high-quality content
    print("\n🔍 Filter 2: High-Quality Content (Score > 60)")
    filter2 = ContentFilter(
        min_quality_score=60.0,
        exclude_keywords=['spam', 'clickbait']
    )
    filtered2 = smart_filter.filter_content(sample_pages, filter2)
    print(f"  Original: {len(sample_pages)} pages")
    print(f"  Filtered: {len(filtered2)} pages")
    for page in filtered2:
        analysis = page.get('content_analysis', {})
        print(f"    - {page['title']} (Quality: {analysis.get('quality_score', 0):.1f})")
    
    # Example 3: Filter by keywords
    print("\n🔍 Filter 3: Technology-Related Content")
    filter3 = ContentFilter(
        keywords=['technology', 'AI', 'machine learning', 'innovation'],
        min_word_count=30
    )
    filtered3 = smart_filter.filter_content(sample_pages, filter3)
    print(f"  Original: {len(sample_pages)} pages")
    print(f"  Filtered: {len(filtered3)} pages")
    for page in filtered3:
        print(f"    - {page['title']}")
    
    # Example 4: Complex filter
    print("\n🔍 Filter 4: Complex Filter (Articles + High Quality + No Spam)")
    filter4 = ContentFilter(
        content_types=[ContentType.ARTICLE, ContentType.BLOG],
        min_quality_score=50.0,
        exclude_keywords=['spam', 'clickbait'],
        min_word_count=40
    )
    filtered4 = smart_filter.filter_content(sample_pages, filter4)
    print(f"  Original: {len(sample_pages)} pages")
    print(f"  Filtered: {len(filtered4)} pages")
    for page in filtered4:
        analysis = page.get('content_analysis', {})
        print(f"    - {page['title']} (Type: {analysis.get('content_type', 'unknown')}, Quality: {analysis.get('quality_score', 0):.1f})")
    
    # 6. Integration with Advanced Crawler
    print("\n6️⃣ Integration with Advanced Crawler:")
    print("-" * 30)
    
    # Create a filter configuration for crawling
    crawl_filter = ContentFilter(
        content_types=[ContentType.ARTICLE, ContentType.BLOG, ContentType.NEWS],
        min_quality_score=40.0,
        exclude_keywords=['spam', 'clickbait'],
        min_word_count=50
    )
    
    print("✅ Smart filtering can be integrated with the advanced crawler!")
    print("   The crawler will automatically apply filters during crawling.")
    print("   This ensures only relevant, high-quality content is collected.")
    
    # 7. Generate comprehensive report
    print("\n7️⃣ Filtering Report:")
    print("-" * 30)
    
    # Test with a comprehensive filter
    comprehensive_filter = ContentFilter(
        content_types=[ContentType.ARTICLE, ContentType.BLOG, ContentType.ABOUT],
        min_quality_score=30.0,
        exclude_keywords=['spam'],
        min_word_count=20
    )
    
    filtered_comprehensive = smart_filter.filter_content(sample_pages, comprehensive_filter)
    report = smart_filter.generate_filter_report(len(sample_pages), len(filtered_comprehensive), comprehensive_filter)
    
    print(f"📊 Filtering Statistics:")
    print(f"  Original pages: {report['filtering_stats']['original_count']}")
    print(f"  Filtered pages: {report['filtering_stats']['filtered_count']}")
    print(f"  Removed pages: {report['filtering_stats']['removed_count']}")
    print(f"  Retention rate: {report['filtering_stats']['retention_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("🎉 Smart Content Filtering Demo Completed!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Content type detection")
    print("   ✅ Quality assessment")
    print("   ✅ Language detection")
    print("   ✅ Content categorization")
    print("   ✅ Multi-criteria filtering")
    print("   ✅ Duplicate detection")
    print("   ✅ Integration with crawler")
    
    print("\n🚀 Next Steps:")
    print("   - Use: python smart_filter_cli.py crawl_results.json --content-types article,blog")
    print("   - Try: python smart_filter_cli.py crawl_results.json --keywords 'AI,technology' --quality-score 70")
    print("   - Test: python smart_filter_cli.py crawl_results.json --categorize-only")


if __name__ == "__main__":
    demo_smart_filtering() 