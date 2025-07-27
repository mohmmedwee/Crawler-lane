#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Visualization Module for Web Crawler
"""

import json
import time
from typing import Dict, List, Any
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd


class DataVisualizer:
    def __init__(self):
        """Initialize the data visualizer."""
        # Set style for better-looking charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Color schemes
        self.colors = {
            'primary': '#4facfe',
            'secondary': '#00f2fe',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
    
    def create_word_cloud(self, text_data: str, output_path: str = None) -> str:
        """Generate a word cloud from text data."""
        try:
            # Create word cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='viridis',
                max_words=100,
                contour_width=3,
                contour_color='steelblue'
            ).generate(text_data)
            
            # Create figure
            plt.figure(figsize=(12, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Word Cloud - Most Frequent Terms', fontsize=16, pad=20)
            
            # Save or show
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                timestamp = int(time.time())
                output_path = f"wordcloud_{timestamp}.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
                
        except Exception as e:
            print(f"Error creating word cloud: {e}")
            return None
    
    def create_content_distribution_chart(self, crawl_data: Dict[str, Any], output_path: str = None) -> str:
        """Create a chart showing content type distribution."""
        try:
            content_types = crawl_data.get('content_summary', {}).get('content_types', {})
            
            if not content_types:
                return None
            
            # Prepare data
            labels = list(content_types.keys())
            values = list(content_types.values())
            
            # Create figure
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
            
            # Pie chart
            colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
            wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax1.set_title('Content Type Distribution', fontsize=14, pad=20)
            
            # Bar chart
            bars = ax2.bar(labels, values, color=self.colors['primary'], alpha=0.7)
            ax2.set_title('Content Type Counts', fontsize=14, pad=20)
            ax2.set_xlabel('Content Types')
            ax2.set_ylabel('Count')
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(value), ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save or show
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                timestamp = int(time.time())
                output_path = f"content_distribution_{timestamp}.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
                
        except Exception as e:
            print(f"Error creating content distribution chart: {e}")
            return None
    
    def create_crawl_statistics_chart(self, crawl_data: Dict[str, Any], output_path: str = None) -> str:
        """Create a comprehensive statistics dashboard."""
        try:
            stats = crawl_data.get('statistics', {})
            metadata = crawl_data.get('metadata', {})
            
            # Create figure with subplots
            fig = plt.figure(figsize=(16, 12))
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
            
            # Main statistics
            ax1 = fig.add_subplot(gs[0, :2])
            metrics = ['Pages', 'Words', 'Links', 'Images']
            values = [
                stats.get('total_pages', 0),
                stats.get('total_words', 0),
                stats.get('total_links', 0),
                stats.get('total_images', 0)
            ]
            
            bars = ax1.bar(metrics, values, color=[self.colors['primary'], self.colors['success'], 
                                                  self.colors['info'], self.colors['warning']], alpha=0.8)
            ax1.set_title('Crawl Statistics Overview', fontsize=16, pad=20)
            ax1.set_ylabel('Count')
            
            # Add value labels
            for bar, value in zip(bars, values):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{value:,}', ha='center', va='bottom', fontweight='bold')
            
            # Crawl metadata
            ax2 = fig.add_subplot(gs[0, 2])
            ax2.axis('off')
            metadata_text = f"""
Crawl Information:
• Domain: {metadata.get('domain', 'N/A')}
• Date: {metadata.get('crawl_date', 'N/A')}
• Max Pages: {metadata.get('max_pages', 'N/A')}
• Max Depth: {metadata.get('max_depth', 'N/A')}
• Delay: {metadata.get('delay', 'N/A')}s
• URLs Crawled: {metadata.get('crawled_urls_count', 'N/A')}
            """
            ax2.text(0.1, 0.9, metadata_text, transform=ax2.transAxes, fontsize=10,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
            
            # Content quality distribution
            ax3 = fig.add_subplot(gs[1, :])
            if crawl_data.get('pages'):
                word_counts = [page.get('word_count', 0) for page in crawl_data['pages']]
                ax3.hist(word_counts, bins=20, color=self.colors['secondary'], alpha=0.7, edgecolor='black')
                ax3.set_title('Word Count Distribution per Page', fontsize=14, pad=20)
                ax3.set_xlabel('Word Count')
                ax3.set_ylabel('Number of Pages')
                ax3.axvline(np.mean(word_counts), color='red', linestyle='--', 
                           label=f'Mean: {np.mean(word_counts):.1f}')
                ax3.legend()
            
            # Top headings
            ax4 = fig.add_subplot(gs[2, :])
            headings = crawl_data.get('content_summary', {}).get('most_common_headings', {})
            if headings:
                top_headings = dict(list(headings.items())[:10])
                bars = ax4.barh(list(top_headings.keys()), list(top_headings.values()), 
                               color=self.colors['info'], alpha=0.7)
                ax4.set_title('Most Common Headings', fontsize=14, pad=20)
                ax4.set_xlabel('Frequency')
                
                # Add value labels
                for bar, value in zip(bars, top_headings.values()):
                    ax4.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                            str(value), ha='left', va='center')
            
            plt.suptitle('Web Crawler Analysis Dashboard', fontsize=18, y=0.98)
            
            # Save or show
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                timestamp = int(time.time())
                output_path = f"crawl_statistics_{timestamp}.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
                
        except Exception as e:
            print(f"Error creating crawl statistics chart: {e}")
            return None
    
    def create_site_structure_visualization(self, crawl_data: Dict[str, Any], output_path: str = None) -> str:
        """Create a visual representation of the site structure."""
        try:
            site_structure = crawl_data.get('site_structure', {})
            
            if not site_structure:
                return None
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Recursive function to draw structure
            def draw_structure(structure, x, y, level=0, max_width=8):
                if not structure:
                    return
                
                # Calculate positions
                items = list(structure.keys())
                if not items:
                    return
                
                item_width = max_width / len(items)
                
                for i, item in enumerate(items):
                    item_x = x + i * item_width + item_width / 2
                    item_y = y - level * 1.5
                    
                    # Draw box
                    box = FancyBboxPatch((item_x - 0.4, item_y - 0.2), 0.8, 0.4,
                                       boxstyle="round,pad=0.1", 
                                       facecolor=self.colors['primary'], 
                                       edgecolor='black', alpha=0.7)
                    ax.add_patch(box)
                    
                    # Add text
                    ax.text(item_x, item_y, item if item else 'root', 
                           ha='center', va='center', fontsize=8, fontweight='bold')
                    
                    # Draw connection line
                    if level > 0:
                        ax.plot([x, item_x], [y + 0.2, item_y + 0.2], 'k-', alpha=0.5, linewidth=1)
                    
                    # Recursively draw children
                    if structure[item]:
                        draw_structure(structure[item], item_x - 0.3, item_y, level + 1, 0.6)
            
            # Start drawing from root
            draw_structure(site_structure, 1, 9, 0, 8)
            
            ax.set_title('Site Structure Visualization', fontsize=16, pad=20)
            
            # Save or show
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                timestamp = int(time.time())
                output_path = f"site_structure_{timestamp}.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
                
        except Exception as e:
            print(f"Error creating site structure visualization: {e}")
            return None
    
    def create_sentiment_analysis_chart(self, ai_analysis: Dict[str, Any], output_path: str = None) -> str:
        """Create sentiment analysis visualization."""
        try:
            sentiment = ai_analysis.get('sentiment', {})
            
            if not sentiment:
                return None
            
            # Create figure
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Sentiment score gauge
            ax1.set_xlim(-1, 1)
            ax1.set_ylim(0, 1)
            ax1.axis('off')
            
            score = sentiment.get('score', 0)
            label = sentiment.get('label', 'neutral')
            
            # Draw gauge
            theta = np.linspace(0, np.pi, 100)
            ax1.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=3)
            
            # Color based on sentiment
            if label == 'positive':
                color = self.colors['success']
            elif label == 'negative':
                color = self.colors['danger']
            else:
                color = self.colors['info']
            
            # Draw score indicator
            angle = (score + 1) * np.pi / 2
            ax1.plot([0, np.cos(angle)], [0, np.sin(angle)], color=color, linewidth=4)
            ax1.text(0, -0.3, f'Sentiment: {label.title()}\nScore: {score:.3f}', 
                    ha='center', va='center', fontsize=12, fontweight='bold')
            
            # Word counts
            labels = ['Positive', 'Negative', 'Total']
            values = [
                sentiment.get('positive_words', 0),
                sentiment.get('negative_words', 0),
                sentiment.get('total_words', 0)
            ]
            colors = [self.colors['success'], self.colors['danger'], self.colors['info']]
            
            bars = ax2.bar(labels, values, color=colors, alpha=0.7)
            ax2.set_title('Sentiment Word Distribution', fontsize=14, pad=20)
            ax2.set_ylabel('Word Count')
            
            # Add value labels
            for bar, value in zip(bars, values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        str(value), ha='center', va='bottom')
            
            # Top keywords
            keywords = ai_analysis.get('keywords', [])
            if keywords:
                top_keywords = keywords[:10]
                keyword_names = [kw['keyword'] for kw in top_keywords]
                keyword_importance = [kw['importance'] for kw in top_keywords]
                
                bars = ax3.barh(keyword_names, keyword_importance, color=self.colors['primary'], alpha=0.7)
                ax3.set_title('Top Keywords by Importance', fontsize=14, pad=20)
                ax3.set_xlabel('Importance Score')
                
                # Add value labels
                for bar, value in zip(bars, keyword_importance):
                    ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                            f'{value:.1f}', ha='left', va='center')
            
            # Content quality
            quality = ai_analysis.get('content_quality', {})
            if quality:
                metrics = ['Length', 'Structure', 'Readability', 'Diversity']
                scores = [
                    quality.get('length_score', 0),
                    quality.get('structure_score', 0),
                    quality.get('readability_score', 0) / 100,  # Normalize to 0-1
                    quality.get('diversity_score', 0)
                ]
                
                bars = ax4.bar(metrics, scores, color=self.colors['secondary'], alpha=0.7)
                ax4.set_title('Content Quality Metrics', fontsize=14, pad=20)
                ax4.set_ylabel('Score (0-1)')
                ax4.set_ylim(0, 1)
                
                # Add value labels
                for bar, value in zip(bars, scores):
                    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                            f'{value:.2f}', ha='center', va='bottom')
            
            plt.suptitle('AI Content Analysis Dashboard', fontsize=18, y=0.98)
            plt.tight_layout()
            
            # Save or show
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
            else:
                timestamp = int(time.time())
                output_path = f"sentiment_analysis_{timestamp}.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
                
        except Exception as e:
            print(f"Error creating sentiment analysis chart: {e}")
            return None
    
    def generate_comprehensive_report(self, crawl_data: Dict[str, Any], ai_analysis: Dict[str, Any] = None) -> str:
        """Generate a comprehensive visual report with all charts."""
        try:
            timestamp = int(time.time())
            report_dir = f"crawl_report_{timestamp}"
            
            # Create all visualizations
            charts = {}
            
            # Word cloud
            if crawl_data.get('pages'):
                all_text = ' '.join([page.get('text_content', '') for page in crawl_data['pages']])
                charts['wordcloud'] = self.create_word_cloud(all_text, f"{report_dir}_wordcloud.png")
            
            # Content distribution
            charts['content_dist'] = self.create_content_distribution_chart(crawl_data, f"{report_dir}_content_dist.png")
            
            # Crawl statistics
            charts['statistics'] = self.create_crawl_statistics_chart(crawl_data, f"{report_dir}_statistics.png")
            
            # Site structure
            charts['structure'] = self.create_site_structure_visualization(crawl_data, f"{report_dir}_structure.png")
            
            # AI analysis (if available)
            if ai_analysis:
                charts['sentiment'] = self.create_sentiment_analysis_chart(ai_analysis, f"{report_dir}_sentiment.png")
            
            # Create HTML report
            html_report = self.create_html_report(crawl_data, ai_analysis, charts, report_dir)
            
            return html_report
            
        except Exception as e:
            print(f"Error generating comprehensive report: {e}")
            return None
    
    def create_html_report(self, crawl_data: Dict[str, Any], ai_analysis: Dict[str, Any], 
                          charts: Dict[str, str], report_dir: str) -> str:
        """Create an HTML report with all visualizations."""
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Crawler Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
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
        .chart-section {{
            margin-bottom: 40px;
        }}
        .chart-section h2 {{
            color: #333;
            border-bottom: 2px solid #4facfe;
            padding-bottom: 10px;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #4facfe;
        }}
        .stat-card h3 {{
            color: #4facfe;
            margin: 0 0 10px 0;
        }}
        .stat-card p {{
            font-size: 24px;
            font-weight: bold;
            margin: 0;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Web Crawler Analysis Report</h1>
            <p>Comprehensive analysis of crawled website content</p>
        </div>
        
        <div class="content">
            <div class="chart-section">
                <h2>📊 Crawl Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Pages Crawled</h3>
                        <p>{crawl_data.get('statistics', {}).get('total_pages', 0):,}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Words</h3>
                        <p>{crawl_data.get('statistics', {}).get('total_words', 0):,}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Links</h3>
                        <p>{crawl_data.get('statistics', {}).get('total_links', 0):,}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Images</h3>
                        <p>{crawl_data.get('statistics', {}).get('total_images', 0):,}</p>
                    </div>
                </div>
            </div>
            
            {f'''
            <div class="chart-section">
                <h2>📈 Crawl Statistics Dashboard</h2>
                <div class="chart-container">
                    <img src="{charts.get('statistics', '')}" alt="Crawl Statistics">
                </div>
            </div>
            ''' if charts.get('statistics') else ''}
            
            {f'''
            <div class="chart-section">
                <h2>📊 Content Distribution</h2>
                <div class="chart-container">
                    <img src="{charts.get('content_dist', '')}" alt="Content Distribution">
                </div>
            </div>
            ''' if charts.get('content_dist') else ''}
            
            {f'''
            <div class="chart-section">
                <h2>☁️ Word Cloud</h2>
                <div class="chart-container">
                    <img src="{charts.get('wordcloud', '')}" alt="Word Cloud">
                </div>
            </div>
            ''' if charts.get('wordcloud') else ''}
            
            {f'''
            <div class="chart-section">
                <h2>🏗️ Site Structure</h2>
                <div class="chart-container">
                    <img src="{charts.get('structure', '')}" alt="Site Structure">
                </div>
            </div>
            ''' if charts.get('structure') else ''}
            
            {f'''
            <div class="chart-section">
                <h2>🤖 AI Content Analysis</h2>
                <div class="chart-container">
                    <img src="{charts.get('sentiment', '')}" alt="Sentiment Analysis">
                </div>
            </div>
            ''' if charts.get('sentiment') else ''}
        </div>
    </div>
</body>
</html>
            """
            
            # Save HTML report
            html_filename = f"{report_dir}_report.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return html_filename
            
        except Exception as e:
            print(f"Error creating HTML report: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Load sample data
    with open('advanced_crawl_httpbin.org_20250727_072852.json', 'r') as f:
        crawl_data = json.load(f)
    
    # Initialize visualizer
    visualizer = DataVisualizer()
    
    # Generate comprehensive report
    report_path = visualizer.generate_comprehensive_report(crawl_data)
    
    if report_path:
        print(f"📊 Comprehensive report generated: {report_path}")
    else:
        print("❌ Failed to generate report") 