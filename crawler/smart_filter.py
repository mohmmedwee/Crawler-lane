#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Content Filtering System for Web Crawler
"""

import re
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import hashlib
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    """Content type categories."""
    ARTICLE = "article"
    PRODUCT = "product"
    REVIEW = "review"
    NEWS = "news"
    BLOG = "blog"
    LANDING_PAGE = "landing_page"
    ABOUT = "about"
    CONTACT = "contact"
    FAQ = "faq"
    DOCUMENTATION = "documentation"
    UNKNOWN = "unknown"


class ContentQuality(Enum):
    """Content quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class ContentFilter:
    """Content filter configuration."""
    content_types: List[ContentType] = None
    min_word_count: int = 0
    max_word_count: int = None
    min_quality_score: float = 0.0
    date_range: Tuple[datetime, datetime] = None
    keywords: List[str] = None
    exclude_keywords: List[str] = None
    url_patterns: List[str] = None
    exclude_url_patterns: List[str] = None
    min_links: int = 0
    max_links: int = None
    min_images: int = 0
    max_images: int = None
    language: str = None
    sentiment: str = None  # positive, negative, neutral
    duplicate_threshold: float = 0.8


class SmartContentFilter:
    def __init__(self):
        """Initialize the smart content filter."""
        # Content type detection patterns
        self.content_patterns = {
            ContentType.ARTICLE: {
                'url_patterns': [r'/article/', r'/post/', r'/blog/', r'/news/'],
                'keywords': ['article', 'post', 'blog', 'news', 'story', 'feature'],
                'meta_patterns': ['article', 'post', 'blog']
            },
            ContentType.PRODUCT: {
                'url_patterns': [r'/product/', r'/item/', r'/shop/', r'/store/'],
                'keywords': ['product', 'item', 'buy', 'purchase', 'price', 'shop'],
                'meta_patterns': ['product', 'item', 'ecommerce']
            },
            ContentType.REVIEW: {
                'url_patterns': [r'/review/', r'/rating/', r'/feedback/'],
                'keywords': ['review', 'rating', 'feedback', 'opinion', 'test'],
                'meta_patterns': ['review', 'rating']
            },
            ContentType.NEWS: {
                'url_patterns': [r'/news/', r'/breaking/', r'/latest/'],
                'keywords': ['news', 'breaking', 'latest', 'update', 'announcement'],
                'meta_patterns': ['news', 'breaking']
            },
            ContentType.BLOG: {
                'url_patterns': [r'/blog/', r'/posts/', r'/journal/'],
                'keywords': ['blog', 'post', 'journal', 'diary', 'thoughts'],
                'meta_patterns': ['blog', 'post']
            },
            ContentType.LANDING_PAGE: {
                'url_patterns': [r'/$', r'/home', r'/main'],
                'keywords': ['welcome', 'home', 'main', 'landing'],
                'meta_patterns': ['landing', 'home']
            },
            ContentType.ABOUT: {
                'url_patterns': [r'/about/', r'/about-us/', r'/company/'],
                'keywords': ['about', 'company', 'team', 'mission', 'vision'],
                'meta_patterns': ['about', 'company']
            },
            ContentType.CONTACT: {
                'url_patterns': [r'/contact/', r'/contact-us/'],
                'keywords': ['contact', 'reach', 'get in touch', 'support'],
                'meta_patterns': ['contact', 'support']
            },
            ContentType.FAQ: {
                'url_patterns': [r'/faq/', r'/help/', r'/support/'],
                'keywords': ['faq', 'frequently asked', 'help', 'support', 'question'],
                'meta_patterns': ['faq', 'help']
            },
            ContentType.DOCUMENTATION: {
                'url_patterns': [r'/docs/', r'/documentation/', r'/guide/'],
                'keywords': ['documentation', 'guide', 'manual', 'tutorial', 'docs'],
                'meta_patterns': ['documentation', 'guide']
            }
        }
        
        # Quality indicators
        self.quality_indicators = {
            'positive': [
                'comprehensive', 'detailed', 'thorough', 'complete', 'extensive',
                'well-written', 'informative', 'educational', 'helpful', 'useful',
                'professional', 'expert', 'authoritative', 'reliable', 'accurate'
            ],
            'negative': [
                'incomplete', 'brief', 'short', 'minimal', 'basic',
                'poorly written', 'confusing', 'unclear', 'vague', 'generic',
                'spam', 'clickbait', 'misleading', 'outdated', 'irrelevant'
            ]
        }
        
        # Language detection patterns
        self.language_patterns = {
            'english': {
                'common_words': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'],
                'patterns': [r'\bthe\b', r'\band\b', r'\bor\b']
            },
            'spanish': {
                'common_words': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se'],
                'patterns': [r'\bel\b', r'\bla\b', r'\bde\b']
            },
            'french': {
                'common_words': ['le', 'la', 'de', 'et', 'à', 'en', 'un', 'une', 'est', 'que'],
                'patterns': [r'\ble\b', r'\bla\b', r'\bde\b']
            }
        }
        
        # Duplicate detection cache
        self.content_hashes = set()
        self.similarity_cache = {}
    
    def detect_content_type(self, url: str, title: str, text_content: str, meta_data: Dict[str, Any]) -> ContentType:
        """Detect the type of content based on URL, title, and content."""
        scores = defaultdict(int)
        
        # Check URL patterns
        for content_type, patterns in self.content_patterns.items():
            for url_pattern in patterns['url_patterns']:
                if re.search(url_pattern, url, re.IGNORECASE):
                    scores[content_type] += 3
            
            # Check keywords in title and content
            for keyword in patterns['keywords']:
                if keyword.lower() in title.lower():
                    scores[content_type] += 2
                if keyword.lower() in text_content.lower():
                    scores[content_type] += 1
            
            # Check meta data
            for meta_pattern in patterns['meta_patterns']:
                for meta_key, meta_value in meta_data.items():
                    if meta_pattern.lower() in str(meta_value).lower():
                        scores[content_type] += 2
        
        # Return the content type with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return ContentType.UNKNOWN
    
    def assess_content_quality(self, text_content: str, detailed_text: Dict[str, Any]) -> Tuple[ContentQuality, float]:
        """Assess the quality of content and return quality level and score."""
        score = 0.0
        max_score = 100.0
        
        # Length score (0-20 points)
        word_count = len(text_content.split())
        if word_count >= 1000:
            score += 20
        elif word_count >= 500:
            score += 15
        elif word_count >= 200:
            score += 10
        elif word_count >= 100:
            score += 5
        
        # Structure score (0-25 points)
        headings_count = sum(len(headings) for headings in detailed_text.get('headings', {}).values())
        paragraphs_count = len(detailed_text.get('paragraphs', []))
        lists_count = len(detailed_text.get('lists', []))
        
        structure_score = min(25, (headings_count * 2 + paragraphs_count * 0.5 + lists_count * 1))
        score += structure_score
        
        # Readability score (0-20 points)
        sentences = re.split(r'[.!?]+', text_content)
        avg_sentence_length = word_count / max(1, len(sentences))
        
        if 10 <= avg_sentence_length <= 20:
            score += 20
        elif 5 <= avg_sentence_length <= 25:
            score += 15
        elif 3 <= avg_sentence_length <= 30:
            score += 10
        else:
            score += 5
        
        # Content diversity score (0-15 points)
        words = text_content.lower().split()
        unique_words = set(words)
        diversity_ratio = len(unique_words) / max(1, len(words))
        score += diversity_ratio * 15
        
        # Quality indicators score (0-20 points)
        positive_count = sum(1 for word in self.quality_indicators['positive'] 
                           if word.lower() in text_content.lower())
        negative_count = sum(1 for word in self.quality_indicators['negative'] 
                           if word.lower() in text_content.lower())
        
        quality_indicator_score = max(0, (positive_count - negative_count) * 2)
        score += min(20, quality_indicator_score)
        
        # Normalize score
        final_score = min(100, max(0, score))
        
        # Determine quality level
        if final_score >= 80:
            quality = ContentQuality.EXCELLENT
        elif final_score >= 60:
            quality = ContentQuality.GOOD
        elif final_score >= 40:
            quality = ContentQuality.FAIR
        else:
            quality = ContentQuality.POOR
        
        return quality, final_score
    
    def detect_language(self, text_content: str) -> str:
        """Detect the language of the content."""
        text_lower = text_content.lower()
        language_scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            for word in patterns['common_words']:
                if word in text_lower:
                    score += 1
            language_scores[language] = score
        
        if language_scores:
            return max(language_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'unknown'
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text contents using Jaccard similarity."""
        # Create word sets
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def is_duplicate(self, text_content: str, threshold: float = 0.8) -> bool:
        """Check if content is duplicate based on similarity threshold."""
        content_hash = hashlib.md5(text_content.encode()).hexdigest()
        
        # Check exact hash match
        if content_hash in self.content_hashes:
            return True
        
        # For now, just add the hash and assume no duplicates
        # In a full implementation, you would compare with existing content
        self.content_hashes.add(content_hash)
        return False
        
        # Add to cache
        self.content_hashes.add(content_hash)
        return False
    
    def get_content_by_hash(self, content_hash: str) -> Optional[str]:
        """Get content by hash (placeholder - would need to be implemented with storage)."""
        # This would typically query a database or storage system
        return None
    
    def extract_date(self, text_content: str, meta_data: Dict[str, Any]) -> Optional[datetime]:
        """Extract date from content or meta data."""
        # Check meta data first
        date_meta_keys = ['date', 'published', 'created', 'updated', 'pubdate']
        for key in date_meta_keys:
            if key in meta_data:
                try:
                    return datetime.fromisoformat(meta_data[key].replace('Z', '+00:00'))
                except:
                    pass
        
        # Check content for date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                try:
                    # Try to parse the first match
                    date_str = matches[0]
                    if '/' in date_str:
                        return datetime.strptime(date_str, '%m/%d/%Y')
                    elif '-' in date_str:
                        return datetime.strptime(date_str, '%Y-%m-%d')
                    else:
                        return datetime.strptime(date_str, '%B %d, %Y')
                except:
                    pass
        
        return None
    
    def filter_content(self, pages: List[Dict[str, Any]], filter_config: ContentFilter) -> List[Dict[str, Any]]:
        """Filter content based on the provided configuration."""
        filtered_pages = []
        
        for page in pages:
            # Skip if page doesn't exist or failed
            if not page.get('success', False):
                continue
            
            url = page.get('url', '')
            title = page.get('title', '')
            text_content = page.get('text_content', '')
            detailed_text = page.get('detailed_text', {})
            word_count = page.get('word_count', 0)
            
            # Apply filters
            
            # 1. Content type filter
            if filter_config.content_types:
                detected_type = self.detect_content_type(url, title, text_content, detailed_text.get('meta_data', {}))
                if detected_type not in filter_config.content_types:
                    continue
            
            # 2. Word count filter
            if word_count < filter_config.min_word_count:
                continue
            if filter_config.max_word_count and word_count > filter_config.max_word_count:
                continue
            
            # 3. Quality filter
            quality, quality_score = self.assess_content_quality(text_content, detailed_text)
            if quality_score < filter_config.min_quality_score:
                continue
            
            # 4. Date range filter
            if filter_config.date_range:
                content_date = self.extract_date(text_content, detailed_text.get('meta_data', {}))
                if content_date:
                    start_date, end_date = filter_config.date_range
                    if not (start_date <= content_date <= end_date):
                        continue
            
            # 5. Keyword filter
            if filter_config.keywords:
                text_lower = text_content.lower()
                if not any(keyword.lower() in text_lower for keyword in filter_config.keywords):
                    continue
            
            # 6. Exclude keywords filter
            if filter_config.exclude_keywords:
                text_lower = text_content.lower()
                if any(keyword.lower() in text_lower for keyword in filter_config.exclude_keywords):
                    continue
            
            # 7. URL pattern filter
            if filter_config.url_patterns:
                if not any(re.search(pattern, url, re.IGNORECASE) for pattern in filter_config.url_patterns):
                    continue
            
            # 8. Exclude URL pattern filter
            if filter_config.exclude_url_patterns:
                if any(re.search(pattern, url, re.IGNORECASE) for pattern in filter_config.exclude_url_patterns):
                    continue
            
            # 9. Links filter
            links_count = len(detailed_text.get('links', []))
            if links_count < filter_config.min_links:
                continue
            if filter_config.max_links and links_count > filter_config.max_links:
                continue
            
            # 10. Images filter
            images_count = len(detailed_text.get('images', []))
            if images_count < filter_config.min_images:
                continue
            if filter_config.max_images and images_count > filter_config.max_images:
                continue
            
            # 11. Language filter
            if filter_config.language:
                detected_language = self.detect_language(text_content)
                if detected_language != filter_config.language:
                    continue
            
            # 12. Sentiment filter
            if filter_config.sentiment:
                # Simple sentiment detection
                positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
                negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst']
                
                text_lower = text_content.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    detected_sentiment = 'positive'
                elif negative_count > positive_count:
                    detected_sentiment = 'negative'
                else:
                    detected_sentiment = 'neutral'
                
                if detected_sentiment != filter_config.sentiment:
                    continue
            
            # 13. Duplicate filter
            if filter_config.duplicate_threshold:
                if self.is_duplicate(text_content, filter_config.duplicate_threshold):
                    continue
            
            # Add analysis data to the page
            page['content_analysis'] = {
                'content_type': self.detect_content_type(url, title, text_content, detailed_text.get('meta_data', {})).value,
                'quality': quality.value,
                'quality_score': quality_score,
                'language': self.detect_language(text_content),
                'date_extracted': self.extract_date(text_content, detailed_text.get('meta_data', {})),
                'is_duplicate': self.is_duplicate(text_content, filter_config.duplicate_threshold)
            }
            
            filtered_pages.append(page)
        
        return filtered_pages
    
    def categorize_content(self, pages: List[Dict[str, Any]]) -> Dict[ContentType, List[Dict[str, Any]]]:
        """Categorize content by type."""
        categories = defaultdict(list)
        
        for page in pages:
            if not page.get('success', False):
                continue
            
            url = page.get('url', '')
            title = page.get('title', '')
            text_content = page.get('text_content', '')
            detailed_text = page.get('detailed_text', {})
            
            content_type = self.detect_content_type(url, title, text_content, detailed_text.get('meta_data', {}))
            categories[content_type].append(page)
        
        return dict(categories)
    
    def generate_filter_report(self, original_count: int, filtered_count: int, 
                             filter_config: ContentFilter) -> Dict[str, Any]:
        """Generate a report about the filtering process."""
        return {
            'filter_config': {
                'content_types': [ct.value for ct in filter_config.content_types] if filter_config.content_types else None,
                'min_word_count': filter_config.min_word_count,
                'max_word_count': filter_config.max_word_count,
                'min_quality_score': filter_config.min_quality_score,
                'keywords': filter_config.keywords,
                'exclude_keywords': filter_config.exclude_keywords,
                'language': filter_config.language,
                'sentiment': filter_config.sentiment
            },
            'filtering_stats': {
                'original_count': original_count,
                'filtered_count': filtered_count,
                'removed_count': original_count - filtered_count,
                'retention_rate': (filtered_count / original_count * 100) if original_count > 0 else 0
            },
            'timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    # Initialize smart filter
    smart_filter = SmartContentFilter()
    
    # Create filter configuration
    filter_config = ContentFilter(
        content_types=[ContentType.ARTICLE, ContentType.BLOG, ContentType.NEWS],
        min_word_count=100,
        min_quality_score=50.0,
        keywords=['technology', 'AI', 'machine learning'],
        exclude_keywords=['spam', 'clickbait'],
        language='english',
        sentiment='positive',
        duplicate_threshold=0.8
    )
    
    # Sample pages (would come from crawler)
    sample_pages = [
        {
            'url': 'https://example.com/article/ai-future',
            'title': 'The Future of Artificial Intelligence',
            'text_content': 'Artificial Intelligence is transforming the way we live and work...',
            'word_count': 500,
            'success': True,
            'detailed_text': {
                'headings': {'h1': ['AI Future'], 'h2': ['Technology Trends']},
                'paragraphs': ['AI is amazing...', 'Machine learning is great...'],
                'meta_data': {'description': 'AI technology article'}
            }
        }
    ]
    
    # Apply filtering
    filtered_pages = smart_filter.filter_content(sample_pages, filter_config)
    
    # Generate report
    report = smart_filter.generate_filter_report(len(sample_pages), len(filtered_pages), filter_config)
    
    print("🔍 Smart Content Filtering Results:")
    print("=" * 50)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Categorize content
    categories = smart_filter.categorize_content(sample_pages)
    print(f"\n📂 Content Categories:")
    for content_type, pages in categories.items():
        print(f"  {content_type.value}: {len(pages)} pages") 