#!/usr/bin/env python3
"""
Simple Flask test for AdvancedWebCrawler
"""

from flask import Flask, request, jsonify
from advanced_crawler import AdvancedWebCrawler
import time

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_crawler():
    try:
        data = request.get_json()
        url = data.get('url', 'https://httpbin.org/html')
        
        print(f"Testing crawler with URL: {url}")
        
        # Create fresh instance
        crawler = AdvancedWebCrawler(max_pages=1, delay=1)
        
        # Bypass robots.txt
        crawler.check_robots_txt = lambda x: True
        
        # Test crawl_website directly
        result = crawler.crawl_website(url, use_selenium=False)
        
        print(f"Result: {result}")
        
        if result.get('success'):
            return jsonify({'success': True, 'message': 'Crawler works!'})
        else:
            return jsonify({'success': False, 'error': result.get('error')})
            
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8080) 