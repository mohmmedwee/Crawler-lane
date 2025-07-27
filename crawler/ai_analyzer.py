#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Powered Content Analyzer for Web Crawler
"""

import re
from collections import Counter
from typing import Dict, List, Any, Tuple
import json
import time


class AIContentAnalyzer:
    def __init__(self):
        """Initialize AI content analyzer with basic NLP capabilities."""
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'
        }
        
        # Common positive and negative words for sentiment analysis
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'perfect',
            'love', 'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'best', 'top', 'outstanding',
            'brilliant', 'superb', 'magnificent', 'terrific', 'fabulous', 'incredible', 'remarkable'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'disappointing', 'poor', 'unfortunate',
            'hate', 'dislike', 'angry', 'sad', 'upset', 'frustrated', 'annoyed', 'disgusted',
            'terrible', 'dreadful', 'atrocious', 'abysmal', 'appalling', 'deplorable', 'miserable'
        }
    
    def analyze_content(self, text_content: str, detailed_text: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis on crawled content.
        
        Args:
            text_content: Raw text content
            detailed_text: Structured text data
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'sentiment': self.analyze_sentiment(text_content),
            'topics': self.extract_topics(text_content, detailed_text),
            'keywords': self.extract_keywords(text_content),
            'summary': self.generate_summary(text_content),
            'language': self.detect_language(text_content),
            'entities': self.extract_entities(text_content),
            'content_quality': self.assess_content_quality(text_content, detailed_text),
            'readability': self.calculate_readability(text_content),
            'word_statistics': self.get_word_statistics(text_content)
        }
        
        return analysis
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the content."""
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0, 'label': 'neutral', 'confidence': 0}
        
        # Calculate sentiment score (-1 to 1)
        sentiment_score = (positive_count - negative_count) / total_words
        
        # Determine sentiment label
        if sentiment_score > 0.05:
            label = 'positive'
        elif sentiment_score < -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        # Calculate confidence based on word count
        confidence = min(0.95, (positive_count + negative_count) / total_words * 10)
        
        return {
            'score': round(sentiment_score, 3),
            'label': label,
            'confidence': round(confidence, 3),
            'positive_words': positive_count,
            'negative_words': negative_count,
            'total_words': total_words
        }
    
    def extract_topics(self, text: str, detailed_text: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract main topics from the content."""
        topics = []
        
        # Extract topics from headings
        headings = detailed_text.get('headings', {})
        for heading_type, heading_list in headings.items():
            for heading in heading_list:
                if len(heading.strip()) > 3:  # Filter out very short headings
                    topics.append({
                        'topic': heading.strip(),
                        'type': 'heading',
                        'level': heading_type,
                        'confidence': 0.9
                    })
        
        # Extract topics from frequent words (excluding stop words)
        words = [word.lower() for word in re.findall(r'\b\w+\b', text) 
                if word.lower() not in self.stop_words and len(word) > 3]
        
        word_freq = Counter(words)
        common_words = word_freq.most_common(10)
        
        for word, count in common_words:
            if count > 2:  # Only include words that appear multiple times
                topics.append({
                    'topic': word.title(),
                    'type': 'keyword',
                    'frequency': count,
                    'confidence': min(0.8, count / len(words) * 10)
                })
        
        return topics[:15]  # Return top 15 topics
    
    def extract_keywords(self, text: str) -> List[Dict[str, Any]]:
        """Extract important keywords from the content."""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out stop words and short words
        filtered_words = [word for word in words 
                         if word not in self.stop_words and len(word) > 3]
        
        # Count word frequency
        word_freq = Counter(filtered_words)
        
        # Calculate TF-IDF like score (simplified)
        total_words = len(filtered_words)
        keywords = []
        
        for word, count in word_freq.most_common(20):
            if count > 1:  # Only include words that appear multiple times
                # Simple importance score
                importance = (count / total_words) * 100
                keywords.append({
                    'keyword': word.title(),
                    'frequency': count,
                    'importance': round(importance, 2),
                    'density': round((count / total_words) * 100, 2)
                })
        
        return keywords
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate a summary of the content."""
        # Simple extractive summarization
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return "No content available for summarization."
        
        # Score sentences based on word frequency
        word_freq = Counter(re.findall(r'\b\w+\b', text.lower()))
        
        sentence_scores = []
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words)
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        summary_sentences = []
        current_length = 0
        
        for sentence, score in sentence_scores:
            if current_length + len(sentence) <= max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        if summary_sentences:
            return ' '.join(summary_sentences) + '.'
        else:
            return text[:max_length] + '...' if len(text) > max_length else text
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the content."""
        # Simple language detection based on common words
        text_lower = text.lower()
        
        # English indicators
        english_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        english_count = sum(1 for word in english_words if word in text_lower)
        
        # Spanish indicators
        spanish_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le'}
        spanish_count = sum(1 for word in spanish_words if word in text_lower)
        
        # French indicators
        french_words = {'le', 'la', 'de', 'et', 'à', 'en', 'un', 'une', 'est', 'que', 'pour', 'dans'}
        french_count = sum(1 for word in french_words if word in text_lower)
        
        # German indicators
        german_words = {'der', 'die', 'das', 'und', 'in', 'den', 'von', 'zu', 'mit', 'sich', 'auf', 'für'}
        german_count = sum(1 for word in german_words if word in text_lower)
        
        languages = {
            'english': english_count,
            'spanish': spanish_count,
            'french': french_count,
            'german': german_count
        }
        
        detected_language = max(languages, key=languages.get)
        confidence = languages[detected_language] / max(1, sum(languages.values()))
        
        return {
            'language': detected_language,
            'confidence': round(confidence, 3),
            'scores': languages
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from the content."""
        entities = {
            'people': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'urls': []
        }
        
        # Extract URLs
        url_pattern = r'https?://[^\s]+'
        entities['urls'] = re.findall(url_pattern, text)
        
        # Extract dates (simple patterns)
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        ]
        
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text))
        
        # Extract potential organizations (words with common org suffixes)
        org_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|LLC|Ltd|Company|Organization|Foundation|Institute|University|College)\b'
        entities['organizations'] = re.findall(org_pattern, text)
        
        # Extract potential people names (simple pattern)
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        potential_names = re.findall(name_pattern, text)
        entities['people'] = [name for name in potential_names if name not in entities['organizations']]
        
        # Extract potential locations (words ending with common location suffixes)
        location_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:City|State|Country|Street|Avenue|Road|Boulevard|Park|Square)\b'
        entities['locations'] = re.findall(location_pattern, text)
        
        return entities
    
    def assess_content_quality(self, text: str, detailed_text: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of the content."""
        quality_metrics = {}
        
        # Content length
        quality_metrics['length_score'] = min(1.0, len(text) / 1000)  # Normalize to 1000 chars
        
        # Structure score (headings, paragraphs, lists)
        headings_count = sum(len(headings) for headings in detailed_text.get('headings', {}).values())
        paragraphs_count = len(detailed_text.get('paragraphs', []))
        lists_count = len(detailed_text.get('lists', []))
        
        structure_score = min(1.0, (headings_count * 0.3 + paragraphs_count * 0.1 + lists_count * 0.2) / 10)
        quality_metrics['structure_score'] = round(structure_score, 3)
        
        # Readability score
        readability = self.calculate_readability(text)
        quality_metrics['readability_score'] = readability['score']
        
        # Content diversity (unique words ratio)
        words = text.lower().split()
        unique_words = set(words)
        diversity_score = len(unique_words) / max(1, len(words))
        quality_metrics['diversity_score'] = round(diversity_score, 3)
        
        # Overall quality score
        overall_score = (
            quality_metrics['length_score'] * 0.2 +
            quality_metrics['structure_score'] * 0.3 +
            quality_metrics['readability_score'] * 0.3 +
            quality_metrics['diversity_score'] * 0.2
        )
        quality_metrics['overall_score'] = round(overall_score, 3)
        
        # Quality label
        if overall_score >= 0.8:
            quality_metrics['label'] = 'excellent'
        elif overall_score >= 0.6:
            quality_metrics['label'] = 'good'
        elif overall_score >= 0.4:
            quality_metrics['label'] = 'fair'
        else:
            quality_metrics['label'] = 'poor'
        
        return quality_metrics
    
    def calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = text.split()
        syllables = self.count_syllables(text)
        
        if not sentences or not words:
            return {'score': 0, 'level': 'unknown', 'metrics': {}}
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Flesch Reading Ease
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))
        
        # Determine reading level
        if flesch_score >= 90:
            level = 'very easy'
        elif flesch_score >= 80:
            level = 'easy'
        elif flesch_score >= 70:
            level = 'fairly easy'
        elif flesch_score >= 60:
            level = 'standard'
        elif flesch_score >= 50:
            level = 'fairly difficult'
        elif flesch_score >= 30:
            level = 'difficult'
        else:
            level = 'very difficult'
        
        return {
            'score': round(flesch_score, 1),
            'level': level,
            'metrics': {
                'avg_sentence_length': round(avg_sentence_length, 1),
                'avg_syllables_per_word': round(avg_syllables_per_word, 2),
                'total_sentences': len(sentences),
                'total_words': len(words),
                'total_syllables': syllables
            }
        }
    
    def count_syllables(self, text: str) -> int:
        """Count syllables in text (simplified method)."""
        text = text.lower()
        count = 0
        vowels = 'aeiouy'
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return max(1, count)
    
    def get_word_statistics(self, text: str) -> Dict[str, Any]:
        """Get comprehensive word statistics."""
        words = text.split()
        unique_words = set(words)
        
        # Word length distribution
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        # Character statistics
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', ''))
        
        return {
            'total_words': len(words),
            'unique_words': len(unique_words),
            'avg_word_length': round(avg_word_length, 2),
            'total_characters': chars,
            'characters_no_spaces': chars_no_spaces,
            'word_diversity': round(len(unique_words) / len(words), 3) if words else 0,
            'avg_words_per_sentence': round(len(words) / max(1, len(text.split('.'))), 1)
        }


# Example usage
if __name__ == "__main__":
    analyzer = AIContentAnalyzer()
    
    # Sample text for testing
    sample_text = """
    Artificial Intelligence is transforming the way we live and work. 
    Machine learning algorithms are becoming increasingly sophisticated, 
    enabling computers to perform tasks that were once thought impossible. 
    Companies like Google, Microsoft, and OpenAI are leading the charge 
    in developing cutting-edge AI technologies. The future looks bright 
    for AI applications in healthcare, education, and transportation.
    """
    
    sample_detailed_text = {
        'headings': {
            'h1': ['Artificial Intelligence Revolution'],
            'h2': ['Machine Learning Advances', 'Future Applications']
        },
        'paragraphs': [sample_text],
        'lists': [],
        'links': [],
        'images': []
    }
    
    # Analyze the content
    analysis = analyzer.analyze_content(sample_text, sample_detailed_text)
    
    print("🤖 AI Content Analysis Results:")
    print("=" * 50)
    print(json.dumps(analysis, indent=2, ensure_ascii=False)) 