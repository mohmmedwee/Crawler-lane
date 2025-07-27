from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from crawler import WebCrawler
from advanced_crawler import AdvancedWebCrawler
from smart_filter import SmartContentFilter, ContentFilter, ContentType
from visualization_dashboard import DataVisualizationDashboard
import json
import os
from datetime import datetime
import time

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize the crawlers
crawler = WebCrawler()
smart_filter = SmartContentFilter()
visualization_dashboard = DataVisualizationDashboard()

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl_website():
    """API endpoint for basic crawling."""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Create a fresh crawler instance
        crawler = WebCrawler()
        result = crawler.crawl_website(url, use_selenium=False)
        
        if result.get('success'):
            # Calculate additional metrics
            total_words = result.get('total_words', 0)
            avg_quality_score = result.get('avg_quality_score', 0)
            
            result.update({
                'total_words': total_words,
                'avg_quality_score': round(avg_quality_score, 2)
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/advanced-crawl', methods=['POST'])
def advanced_crawl_website():
    """API endpoint for advanced crawling."""
    try:
        data = request.get_json()
        url = data.get('url')
        max_pages = data.get('max_pages', 10)
        wait_time = data.get('wait_time', 1)
        headless = data.get('headless', True)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Create a fresh advanced crawler instance
        advanced_crawler = AdvancedWebCrawler(
            max_pages=max_pages,
            delay=wait_time
        )
        
        # Temporarily bypass robots.txt check
        advanced_crawler.check_robots_txt = lambda x: True
        
        start_time = time.time()
        # Use headless=True for requests, headless=False for selenium
        use_selenium = not headless  # headless=True means use requests, headless=False means use Selenium
        
        result = advanced_crawler.crawl_website(url, use_selenium=use_selenium)
        execution_time = round(time.time() - start_time, 2)
        
        if result.get('success'):
            # Calculate additional metrics
            pages = result.get('pages', [])
            total_words = sum(page.get('word_count', 0) for page in pages)
            avg_quality_score = sum(page.get('quality_score', 0) for page in pages) / len(pages) if pages else 0
            
            result.update({
                'total_words': total_words,
                'avg_quality_score': round(avg_quality_score, 2),
                'execution_time': execution_time
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
            language=languages[0] if languages else None
        )
        
        # Create a fresh advanced crawler instance
        advanced_crawler = AdvancedWebCrawler(
            max_pages=max_pages,
            delay=1
        )
        
        # Temporarily bypass robots.txt check
        advanced_crawler.check_robots_txt = lambda x: True
        
        # Use advanced crawler WITHOUT smart filtering first to test
        result = advanced_crawler.crawl_website(url, use_selenium=False, filter_config=None)
        
        # Check if we got a valid result
        if result and isinstance(result, dict):
            # Handle the result structure
            if 'error' in result:
                return jsonify({'success': False, 'error': result['error']}), 400
            
            # If result has pages, process them
            if 'pages' in result and result['pages']:
                pages = result['pages']
                total_words = sum(page.get('word_count', 0) for page in pages)
                avg_quality_score = sum(page.get('quality_score', 0) for page in pages) / len(pages) if pages else 0
                
                # Get unique content types and languages
                content_types_found = list(set(page.get('content_type', 'Unknown') for page in pages))
                languages_found = list(set(page.get('language', 'Unknown') for page in pages))
                
                # Return the full result with additional fields
                result.update({
                    'total_words': total_words,
                    'avg_quality_score': round(avg_quality_score, 2),
                    'filtered_pages': len(pages),
                    'content_types': content_types_found,
                    'languages': languages_found
                })
            else:
                # No pages found
                return jsonify({'success': False, 'error': 'No pages were successfully crawled'}), 400
        else:
            return jsonify({'success': False, 'error': 'No pages were successfully crawled'}), 400
        
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
        
        # Create visualizations using the correct method
        try:
            # Create AI text analysis dashboard
            dashboard_html = visualization_dashboard.create_ai_text_analysis_dashboard(crawl_data)
            
            # Create text extraction visualization
            extraction_html = visualization_dashboard.create_text_extraction_visualization(crawl_data)
            
            # Create AI content quality report (with empty ai_analysis if not provided)
            ai_analysis = crawl_data.get('ai_analysis', {})
            quality_html = visualization_dashboard.create_ai_content_quality_report(crawl_data, ai_analysis)
            
            return jsonify({
                'success': True,
                'message': "Created 3 visualization types successfully",
                'visualizations': {
                    'dashboard': dashboard_html,
                    'extraction': extraction_html,
                    'quality': quality_html
                }
            })
        except Exception as viz_error:
            return jsonify({'success': False, 'error': f'Visualization error: {str(viz_error)}'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Serve the main dashboard page with integrated visualizations."""
    return render_template('dashboard.html')

@app.route('/download-json', methods=['POST'])
def download_json():
    """API endpoint for downloading crawl results as JSON."""
    try:
        data = request.get_json()
        crawl_data = data.get('crawl_data')
        filename = data.get('filename', 'crawl_results.json')
        
        if not crawl_data:
            return jsonify({'success': False, 'error': 'Crawl data is required'}), 400
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Create downloads directory if it doesn't exist
        downloads_dir = 'downloads'
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        filepath = os.path.join(downloads_dir, filename)
        
        # Save the data to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(crawl_data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True, 
            'filename': filename,
            'filepath': filepath,
            'message': f'Results saved to {filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/downloads/<filename>')
def serve_download(filename):
    """Serve downloaded files."""
    try:
        downloads_dir = 'downloads'
        filepath = os.path.join(downloads_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(downloads_dir, filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 