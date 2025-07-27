from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from crawler import WebCrawler
from advanced_crawler import AdvancedWebCrawler
from smart_filter import SmartContentFilter, ContentFilter, ContentType
from visualization_dashboard import DataVisualizationDashboard
import json
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize the crawlers
crawler = WebCrawler()
advanced_crawler = None  # Will be initialized when needed
smart_filter = SmartContentFilter()
visualization_dashboard = DataVisualizationDashboard()

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl_website():
    """API endpoint to crawl a single website."""
    try:
        data = request.get_json()
        url = data.get('url')
        max_pages = data.get('max_pages', 10)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Use basic crawler
        result = crawler.crawl_website(url, max_pages=max_pages)
        
        if result.get('success'):
            # Calculate additional metrics
            pages = result.get('pages', [])
            total_words = sum(page.get('word_count', 0) for page in pages)
            avg_quality_score = sum(page.get('quality_score', 0) for page in pages) / len(pages) if pages else 0
            
            result.update({
                'total_words': total_words,
                'avg_quality_score': round(avg_quality_score, 2)
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/advanced-crawl', methods=['POST'])
def advanced_crawl_website():
    """API endpoint for advanced multi-page crawling."""
    try:
        data = request.get_json()
        url = data.get('url')
        max_pages = data.get('max_pages', 10)
        wait_time = data.get('wait_time', 3)
        headless = data.get('headless', True)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Initialize advanced crawler
        global advanced_crawler
        advanced_crawler = AdvancedWebCrawler(
            max_pages=max_pages,
            delay=wait_time
        )
        
        # Start crawling
        result = advanced_crawler.crawl_website(url, use_selenium=True)
        
        if result.get('success'):
            # Calculate additional metrics
            pages = result.get('pages', [])
            total_words = sum(page.get('word_count', 0) for page in pages)
            avg_quality_score = sum(page.get('quality_score', 0) for page in pages) / len(pages) if pages else 0
            
            result.update({
                'total_words': total_words,
                'avg_quality_score': round(avg_quality_score, 2),
                'execution_time': result.get('execution_time', 0)
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/smart-filter-crawl', methods=['POST'])
def smart_filter_crawl_website():
    """API endpoint for smart filtering with crawling."""
    try:
        data = request.get_json()
        url = data.get('url')
        max_pages = data.get('max_pages', 10)
        min_quality = data.get('min_quality', 70)
        content_types = data.get('content_types', [])
        languages = data.get('languages', [])
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Create content filter
        content_filter = ContentFilter(
            min_quality_score=min_quality,
            content_types=content_types,
            languages=languages
        )
        
        # Use smart filter crawler
        result = smart_filter.crawl_and_filter(url, content_filter, max_pages=max_pages)
        
        if result.get('success'):
            # Calculate additional metrics
            pages = result.get('pages', [])
            total_words = sum(page.get('word_count', 0) for page in pages)
            avg_quality_score = sum(page.get('quality_score', 0) for page in pages) / len(pages) if pages else 0
            
            # Get unique content types and languages
            content_types_found = list(set(page.get('content_type', 'Unknown') for page in pages))
            languages_found = list(set(page.get('language', 'Unknown') for page in pages))
            
            result.update({
                'total_words': total_words,
                'avg_quality_score': round(avg_quality_score, 2),
                'filtered_pages': result.get('filtered_pages', 0),
                'content_types': content_types_found,
                'languages': languages_found
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/visualize', methods=['POST'])
def create_visualizations():
    """API endpoint to create data visualizations."""
    try:
        data = request.get_json()
        crawl_data = data.get('crawl_data')
        
        if not crawl_data:
            return jsonify({'success': False, 'error': 'Crawl data is required'}), 400
        
        # Create visualizations
        result = visualization_dashboard.create_visualizations(crawl_data)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': f"Created {len(result.get('files', []))} visualization(s)",
                'visualizations': result.get('files', {})
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Failed to create visualizations')}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Serve the main dashboard page with integrated visualizations."""
    return render_template('dashboard.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 