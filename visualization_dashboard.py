#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Visualization Dashboard for Web Crawler
AI-Focused Text Extraction Analytics
"""

import json
import time
import base64
from io import BytesIO
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo


class DataVisualizationDashboard:
    def __init__(self):
        """Initialize the data visualization dashboard."""
        # Set style for better-looking charts
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            plt.style.use('seaborn')
        sns.set_palette("husl")
        
        # Color schemes for AI/tech theme
        self.colors = {
            'primary': '#4facfe',
            'secondary': '#00f2fe',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db',
            'ai_blue': '#1e3a8a',
            'ai_purple': '#7c3aed',
            'ai_green': '#059669',
            'ai_orange': '#ea580c',
            'ai_red': '#dc2626',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
        # AI-focused metrics
        self.ai_metrics = {
            'text_quality': 'Text Quality Score',
            'content_diversity': 'Content Diversity',
            'readability': 'Readability Index',
            'sentiment_score': 'Sentiment Analysis',
            'topic_coherence': 'Topic Coherence',
            'ai_relevance': 'AI Relevance Score'
        }
    
    def create_ai_text_analysis_dashboard(self, crawl_data: Dict[str, Any], ai_analysis: Dict[str, Any] = None) -> str:
        """Create a comprehensive AI-focused text analysis dashboard."""
        try:
            # Create interactive Plotly dashboard
            fig = make_subplots(
                rows=3, cols=3,
                subplot_titles=(
                    'Text Quality Distribution', 'Content Type Analysis', 'Word Cloud',
                    'Sentiment Analysis', 'Language Distribution', 'Readability Metrics',
                    'Topic Categories', 'Content Length Analysis', 'AI Relevance Score'
                ),
                specs=[
                    [{"type": "histogram"}, {"type": "pie"}, {"type": "scatter"}],
                    [{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}],
                    [{"type": "bar"}, {"type": "histogram"}, {"type": "gauge"}]
                ]
            )
            
            # 1. Text Quality Distribution
            if crawl_data.get('pages'):
                quality_scores = []
                for page in crawl_data['pages']:
                    if page.get('content_analysis', {}).get('quality_score'):
                        quality_scores.append(page['content_analysis']['quality_score'])
                
                if quality_scores:
                    fig.add_trace(
                        go.Histogram(x=quality_scores, name="Quality Scores", 
                                   marker_color=self.colors['ai_blue']),
                        row=1, col=1
                    )
            
            # 2. Content Type Analysis
            if crawl_data.get('categories'):
                content_types = list(crawl_data['categories'].keys())
                content_counts = [crawl_data['categories'][ct]['count'] for ct in content_types]
                
                fig.add_trace(
                    go.Pie(labels=content_types, values=content_counts, name="Content Types",
                          marker_colors=[self.colors['primary'], self.colors['secondary'], 
                                       self.colors['success'], self.colors['warning']]),
                    row=1, col=2
                )
            
            # 3. Word Cloud (placeholder)
            fig.add_trace(
                go.Scatter(x=[0], y=[0], mode='text', text=['Word Cloud'], 
                          textfont=dict(size=20), showlegend=False),
                row=1, col=3
            )
            
            # 4. Sentiment Analysis
            if ai_analysis and ai_analysis.get('sentiment'):
                sentiment = ai_analysis['sentiment']
                labels = ['Positive', 'Negative', 'Neutral']
                values = [
                    sentiment.get('positive_words', 0),
                    sentiment.get('negative_words', 0),
                    sentiment.get('total_words', 0) - sentiment.get('positive_words', 0) - sentiment.get('negative_words', 0)
                ]
                
                fig.add_trace(
                    go.Bar(x=labels, y=values, name="Sentiment", 
                          marker_color=[self.colors['success'], self.colors['danger'], self.colors['info']]),
                    row=2, col=1
                )
            
            # 5. Language Distribution
            if crawl_data.get('pages'):
                languages = {}
                for page in crawl_data['pages']:
                    if page.get('content_analysis', {}).get('language'):
                        lang = page['content_analysis']['language']
                        languages[lang] = languages.get(lang, 0) + 1
                
                if languages:
                    fig.add_trace(
                        go.Bar(x=list(languages.keys()), y=list(languages.values()), 
                              name="Languages", marker_color=self.colors['ai_purple']),
                        row=2, col=2
                    )
            
            # 6. Readability Metrics
            if ai_analysis and ai_analysis.get('readability'):
                readability = ai_analysis['readability']
                metrics = ['Avg Sentence Length', 'Avg Syllables/Word', 'Flesch Score']
                values = [
                    readability.get('metrics', {}).get('avg_sentence_length', 0),
                    readability.get('metrics', {}).get('avg_syllables_per_word', 0),
                    readability.get('score', 0)
                ]
                
                fig.add_trace(
                    go.Scatter(x=metrics, y=values, mode='lines+markers', 
                              name="Readability", line=dict(color=self.colors['ai_green'])),
                    row=2, col=3
                )
            
            # 7. Topic Categories
            if ai_analysis and ai_analysis.get('topics'):
                topics = ai_analysis['topics'][:10]  # Top 10 topics
                topic_names = [t['topic'] for t in topics]
                topic_confidences = [t['confidence'] for t in topics]
                
                fig.add_trace(
                    go.Bar(x=topic_names, y=topic_confidences, name="Topics", 
                          marker_color=self.colors['ai_orange']),
                    row=3, col=1
                )
            
            # 8. Content Length Analysis
            if crawl_data.get('pages'):
                word_counts = [page.get('word_count', 0) for page in crawl_data['pages']]
                
                fig.add_trace(
                    go.Histogram(x=word_counts, name="Word Counts", 
                               marker_color=self.colors['ai_red']),
                    row=3, col=2
                )
            
            # 9. AI Relevance Score (Bar chart instead of gauge)
            ai_relevance = 85  # Example score
            fig.add_trace(
                go.Bar(
                    x=['AI Relevance'],
                    y=[ai_relevance],
                    name="AI Relevance Score",
                    marker_color=self.colors['ai_blue']
                ),
                row=3, col=3
            )
            
            # Update layout
            fig.update_layout(
                title_text="AI Text Extraction Analysis Dashboard",
                title_x=0.5,
                height=1200,
                showlegend=False,
                template="plotly_white"
            )
            
            # Save as HTML
            timestamp = int(time.time())
            html_filename = f"ai_dashboard_{timestamp}.html"
            fig.write_html(html_filename)
            
            return html_filename
            
        except Exception as e:
            print(f"Error creating AI dashboard: {e}")
            return None
    
    def create_text_extraction_visualization(self, crawl_data: Dict[str, Any]) -> str:
        """Create visualization focused on text extraction metrics."""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Text Extraction Success Rate', 'Content Type Distribution',
                    'Text Quality vs Length', 'Extraction Methods Used'
                ),
                specs=[
                    [{"type": "pie"}, {"type": "bar"}],
                    [{"type": "scatter"}, {"type": "bar"}]
                ]
            )
            
            # 1. Text Extraction Success Rate
            if crawl_data.get('pages'):
                successful_extractions = sum(1 for page in crawl_data['pages'] if page.get('text_content'))
                total_pages = len(crawl_data['pages'])
                failed_extractions = total_pages - successful_extractions
                
                fig.add_trace(
                    go.Pie(labels=['Successful', 'Failed'], 
                          values=[successful_extractions, failed_extractions],
                          marker_colors=[self.colors['success'], self.colors['danger']]),
                    row=1, col=1
                )
            
            # 2. Content Type Distribution
            if crawl_data.get('categories'):
                content_types = list(crawl_data['categories'].keys())
                content_counts = [crawl_data['categories'][ct]['count'] for ct in content_types]
                
                fig.add_trace(
                    go.Bar(x=content_types, y=content_counts, 
                          marker_color=self.colors['primary']),
                    row=1, col=2
                )
            
            # 3. Text Quality vs Length
            if crawl_data.get('pages'):
                word_counts = []
                quality_scores = []
                
                for page in crawl_data['pages']:
                    if page.get('word_count') and page.get('content_analysis', {}).get('quality_score'):
                        word_counts.append(page['word_count'])
                        quality_scores.append(page['content_analysis']['quality_score'])
                
                if word_counts and quality_scores:
                    fig.add_trace(
                        go.Scatter(x=word_counts, y=quality_scores, mode='markers',
                                  marker=dict(color=self.colors['ai_blue'], size=8),
                                  name='Quality vs Length'),
                        row=2, col=1
                    )
            
            # 4. Extraction Methods Used
            methods = ['Requests', 'Selenium', 'Custom Selectors']
            method_counts = [65, 25, 10]  # Example data
            
            fig.add_trace(
                go.Bar(x=methods, y=method_counts, 
                      marker_color=[self.colors['info'], self.colors['warning'], self.colors['ai_purple']]),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title_text="Text Extraction Analytics",
                title_x=0.5,
                height=800,
                showlegend=False
            )
            
            # Save as HTML
            timestamp = int(time.time())
            html_filename = f"text_extraction_viz_{timestamp}.html"
            fig.write_html(html_filename)
            
            return html_filename
            
        except Exception as e:
            print(f"Error creating text extraction visualization: {e}")
            return None
    
    def create_ai_content_quality_report(self, crawl_data: Dict[str, Any], ai_analysis: Dict[str, Any]) -> str:
        """Create a comprehensive AI content quality report."""
        try:
            # Create HTML report with embedded visualizations
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Text Extraction Quality Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .content {{
            padding: 40px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #4facfe;
        }}
        .metric-card h3 {{
            color: #4facfe;
            margin: 0 0 10px 0;
        }}
        .metric-card p {{
            font-size: 24px;
            font-weight: bold;
            margin: 0;
            color: #333;
        }}
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        .ai-insights {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        .ai-insights h3 {{
            margin-top: 0;
        }}
        .insight-item {{
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Text Extraction Quality Report</h1>
            <p>Comprehensive analysis of extracted text content for AI applications</p>
        </div>
        
        <div class="content">
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>📊 Total Pages</h3>
                    <p>{crawl_data.get('statistics', {}).get('total_pages', 0):,}</p>
                </div>
                <div class="metric-card">
                    <h3>📝 Total Words</h3>
                    <p>{crawl_data.get('statistics', {}).get('total_words', 0):,}</p>
                </div>
                <div class="metric-card">
                    <h3>🎯 Avg Quality Score</h3>
                    <p>{self._calculate_avg_quality(crawl_data):.1f}</p>
                </div>
                <div class="metric-card">
                    <h3>📈 Success Rate</h3>
                    <p>{self._calculate_success_rate(crawl_data):.1f}%</p>
                </div>
            </div>
            
            <div class="ai-insights">
                <h3>🧠 AI Content Analysis Insights</h3>
                {self._generate_ai_insights(crawl_data, ai_analysis)}
            </div>
            
            <div class="chart-container">
                <h2>📊 Content Quality Distribution</h2>
                <div id="qualityChart"></div>
            </div>
            
            <div class="chart-container">
                <h2>📂 Content Type Analysis</h2>
                <div id="typeChart"></div>
            </div>
            
            <div class="chart-container">
                <h2>📈 Text Extraction Metrics</h2>
                <div id="extractionChart"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Quality distribution chart
        const qualityData = {self._get_quality_data(crawl_data)};
        Plotly.newPlot('qualityChart', qualityData.data, qualityData.layout);
        
        // Content type chart
        const typeData = {self._get_type_data(crawl_data)};
        Plotly.newPlot('typeChart', typeData.data, typeData.layout);
        
        // Extraction metrics chart
        const extractionData = {self._get_extraction_data(crawl_data)};
        Plotly.newPlot('extractionChart', extractionData.data, extractionData.layout);
    </script>
</body>
</html>
            """
            
            # Save HTML report
            timestamp = int(time.time())
            html_filename = f"ai_quality_report_{timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return html_filename
            
        except Exception as e:
            print(f"Error creating AI quality report: {e}")
            return None
    
    def _calculate_avg_quality(self, crawl_data: Dict[str, Any]) -> float:
        """Calculate average quality score."""
        if not crawl_data.get('pages'):
            return 0.0
        
        quality_scores = []
        for page in crawl_data['pages']:
            if page.get('content_analysis', {}).get('quality_score'):
                quality_scores.append(page['content_analysis']['quality_score'])
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    
    def _calculate_success_rate(self, crawl_data: Dict[str, Any]) -> float:
        """Calculate text extraction success rate."""
        if not crawl_data.get('pages'):
            return 0.0
        
        successful = sum(1 for page in crawl_data['pages'] if page.get('text_content'))
        total = len(crawl_data['pages'])
        
        return (successful / total * 100) if total > 0 else 0.0
    
    def _generate_ai_insights(self, crawl_data: Dict[str, Any], ai_analysis: Dict[str, Any]) -> str:
        """Generate AI insights for the report."""
        insights = []
        
        # Quality insights
        avg_quality = self._calculate_avg_quality(crawl_data)
        if avg_quality > 70:
            insights.append("✅ High-quality content detected - suitable for AI training")
        elif avg_quality > 50:
            insights.append("⚠️ Moderate quality content - may need preprocessing")
        else:
            insights.append("❌ Low-quality content detected - consider filtering")
        
        # Content diversity
        if crawl_data.get('pages'):
            unique_words = set()
            total_words = 0
            for page in crawl_data['pages']:
                if page.get('text_content'):
                    words = page['text_content'].lower().split()
                    unique_words.update(words)
                    total_words += len(words)
            
            diversity = len(unique_words) / total_words if total_words > 0 else 0
            if diversity > 0.6:
                insights.append("🎯 High content diversity - excellent for AI training")
            elif diversity > 0.4:
                insights.append("📊 Good content diversity - suitable for AI applications")
            else:
                insights.append("⚠️ Low content diversity - may need more varied sources")
        
        # Sentiment insights
        if ai_analysis and ai_analysis.get('sentiment'):
            sentiment = ai_analysis['sentiment']
            if sentiment.get('label') == 'positive':
                insights.append("😊 Positive sentiment detected - good for positive AI training")
            elif sentiment.get('label') == 'negative':
                insights.append("😔 Negative sentiment detected - balanced dataset needed")
            else:
                insights.append("😐 Neutral sentiment - balanced content for AI")
        
        # Language insights
        if crawl_data.get('pages'):
            languages = {}
            for page in crawl_data['pages']:
                if page.get('content_analysis', {}).get('language'):
                    lang = page['content_analysis']['language']
                    languages[lang] = languages.get(lang, 0) + 1
            
            if len(languages) > 1:
                insights.append("🌍 Multi-language content detected - international AI training")
            else:
                insights.append("🇺🇸 Single language content - focused AI training")
        
        # Generate HTML
        html_insights = ""
        for insight in insights:
            html_insights += f'<div class="insight-item">{insight}</div>'
        
        return html_insights
    
    def _get_quality_data(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get quality distribution data for Plotly."""
        if not crawl_data.get('pages'):
            return {"data": [], "layout": {}}
        
        quality_scores = []
        for page in crawl_data['pages']:
            if page.get('content_analysis', {}).get('quality_score'):
                quality_scores.append(page['content_analysis']['quality_score'])
        
        if not quality_scores:
            return {"data": [], "layout": {}}
        
        return {
            "data": [{
                "x": quality_scores,
                "type": "histogram",
                "name": "Quality Scores",
                "marker": {"color": self.colors['ai_blue']}
            }],
            "layout": {
                "title": "Content Quality Distribution",
                "xaxis": {"title": "Quality Score"},
                "yaxis": {"title": "Number of Pages"}
            }
        }
    
    def _get_type_data(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get content type data for Plotly."""
        if not crawl_data.get('categories'):
            return {"data": [], "layout": {}}
        
        content_types = list(crawl_data['categories'].keys())
        content_counts = [crawl_data['categories'][ct]['count'] for ct in content_types]
        
        return {
            "data": [{
                "labels": content_types,
                "values": content_counts,
                "type": "pie",
                "name": "Content Types",
                "marker": {"colors": [self.colors['primary'], self.colors['secondary'], 
                                    self.colors['success'], self.colors['warning']]}
            }],
            "layout": {
                "title": "Content Type Distribution"
            }
        }
    
    def _get_extraction_data(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get extraction metrics data for Plotly."""
        if not crawl_data.get('pages'):
            return {"data": [], "layout": {}}
        
        word_counts = []
        quality_scores = []
        
        for page in crawl_data['pages']:
            if page.get('word_count') and page.get('content_analysis', {}).get('quality_score'):
                word_counts.append(page['word_count'])
                quality_scores.append(page['content_analysis']['quality_score'])
        
        return {
            "data": [{
                "x": word_counts,
                "y": quality_scores,
                "mode": "markers",
                "type": "scatter",
                "name": "Quality vs Length",
                "marker": {"color": self.colors['ai_green'], "size": 8}
            }],
            "layout": {
                "title": "Text Quality vs Content Length",
                "xaxis": {"title": "Word Count"},
                "yaxis": {"title": "Quality Score"}
            }
        }


# Example usage
if __name__ == "__main__":
    # Load sample data
    with open('advanced_crawl_httpbin.org_20250727_072852.json', 'r') as f:
        crawl_data = json.load(f)
    
    # Initialize dashboard
    dashboard = DataVisualizationDashboard()
    
    # Create visualizations
    ai_dashboard = dashboard.create_ai_text_analysis_dashboard(crawl_data)
    text_viz = dashboard.create_text_extraction_visualization(crawl_data)
    quality_report = dashboard.create_ai_content_quality_report(crawl_data, {})
    
    print("📊 Data Visualization Results:")
    print(f"  AI Dashboard: {ai_dashboard}")
    print(f"  Text Extraction Viz: {text_viz}")
    print(f"  Quality Report: {quality_report}") 