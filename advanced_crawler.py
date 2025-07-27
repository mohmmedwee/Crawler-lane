#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Web Crawler with Multi-Page Support and Comprehensive Text Extraction
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
import json
import re
import urllib.parse
from typing import Dict, Any, List, Set, Optional
from collections import defaultdict
import logging
from urllib.robotparser import RobotFileParser
import hashlib
from smart_filter import SmartContentFilter, ContentFilter, ContentType


class AdvancedWebCrawler:
    def __init__(self, max_pages: int = 100, max_depth: int = 3, delay: float = 1.0):
        """
        Initialize advanced crawler
        
        Args:
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum depth of crawling (how many links deep)
            delay: Delay between requests in seconds
        """
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Crawling state
        self.crawled_urls = set()
        self.url_queue = []
        self.domain = None
        self.robot_parser = None
        
        # Data storage
        self.pages_data = []
        self.site_map = defaultdict(list)
        self.text_data = {
            'total_pages': 0,
            'total_words': 0,
            'total_links': 0,
            'total_images': 0,
            'pages': [],
            'site_structure': {},
            'content_summary': {},
            'metadata': {}
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize smart filter
        self.smart_filter = SmartContentFilter()
        
    def setup_selenium_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with appropriate options for web scraping."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def check_robots_txt(self, base_url: str) -> bool:
        """Check robots.txt to see if crawling is allowed."""
        try:
            parsed_url = urllib.parse.urlparse(base_url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            self.robot_parser = RobotFileParser()
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            
            return self.robot_parser.can_fetch("*", base_url)
        except Exception as e:
            self.logger.warning(f"Could not check robots.txt: {e}")
            return True
    
    def normalize_url(self, url: str, base_url: str) -> str:
        """Normalize URL to avoid duplicates."""
        try:
            # Parse URLs
            parsed_base = urllib.parse.urlparse(base_url)
            parsed_url = urllib.parse.urlparse(url)
            
            # Handle relative URLs
            if not parsed_url.netloc:
                url = urllib.parse.urljoin(base_url, url)
                parsed_url = urllib.parse.urlparse(url)
            
            # Only crawl same domain
            if parsed_url.netloc != parsed_base.netloc:
                return None
            
            # Remove fragments and normalize
            normalized = urllib.parse.urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                parsed_url.query,
                ''  # Remove fragment
            ))
            
            return normalized
        except Exception as e:
            self.logger.warning(f"Error normalizing URL {url}: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract comprehensive text content from page."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract different types of text content
        text_data = {
            'headings': {},
            'paragraphs': [],
            'lists': [],
            'tables': [],
            'links': [],
            'images': [],
            'forms': [],
            'buttons': [],
            'meta_data': {},
            'structured_data': {}
        }
        
        # Extract headings
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            text_data['headings'][f'h{i}'] = [h.get_text(strip=True) for h in headings if h.get_text(strip=True)]
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        text_data['paragraphs'] = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        
        # Extract lists
        lists = soup.find_all(['ul', 'ol'])
        for lst in lists:
            items = [li.get_text(strip=True) for li in lst.find_all('li') if li.get_text(strip=True)]
            if items:
                text_data['lists'].append({
                    'type': lst.name,
                    'items': items
                })
        
        # Extract tables
        tables = soup.find_all('table')
        for table in tables:
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th']) if cell.get_text(strip=True)]
                if cells:
                    table_data.append(cells)
            if table_data:
                text_data['tables'].append(table_data)
        
        # Extract links
        links = soup.find_all('a', href=True)
        for link in links:
            text_data['links'].append({
                'text': link.get_text(strip=True),
                'href': link.get('href'),
                'title': link.get('title', '')
            })
        
        # Extract images
        images = soup.find_all('img')
        for img in images:
            text_data['images'].append({
                'src': img.get('src'),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        # Extract forms
        forms = soup.find_all('form')
        for form in forms:
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', ''),
                'inputs': []
            }
            inputs = form.find_all('input')
            for inp in inputs:
                form_data['inputs'].append({
                    'type': inp.get('type', ''),
                    'name': inp.get('name', ''),
                    'placeholder': inp.get('placeholder', '')
                })
            text_data['forms'].append(form_data)
        
        # Extract buttons
        buttons = soup.find_all('button')
        text_data['buttons'] = [btn.get_text(strip=True) for btn in buttons if btn.get_text(strip=True)]
        
        # Extract meta data
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                text_data['meta_data'][name] = content
        
        # Extract structured data (JSON-LD)
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                structured_data = json.loads(script.string)
                text_data['structured_data'] = structured_data
            except:
                pass
        
        return text_data
    
    def crawl_page(self, url: str, use_selenium: bool = False) -> Dict[str, Any]:
        """Crawl a single page and extract comprehensive data."""
        if url in self.crawled_urls:
            return None
        
        self.crawled_urls.add(url)
        self.logger.info(f"Crawling: {url}")
        
        try:
            if use_selenium:
                return self._crawl_with_selenium(url)
            else:
                return self._crawl_with_requests(url)
        except Exception as e:
            self.logger.error(f"Error crawling {url}: {e}")
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }
    
    def _crawl_with_requests(self, url: str) -> Dict[str, Any]:
        """Crawl page using requests."""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract comprehensive text data
        text_data = self.extract_text_content(soup)
        
        # Get all text content
        all_text = soup.get_text(separator=' ', strip=True)
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text() if title else "No title found"
        
        # Count words
        word_count = len(all_text.split())
        
        # Find new links
        new_links = []
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            normalized_url = self.normalize_url(href, url)
            if normalized_url and normalized_url not in self.crawled_urls:
                new_links.append(normalized_url)
        
        return {
            'url': url,
            'success': True,
            'title': title_text,
            'word_count': word_count,
            'text_content': all_text[:5000],  # First 5000 chars
            'detailed_text': text_data,
            'new_links': new_links,
            'status_code': response.status_code,
            'method': 'requests'
        }
    
    def _crawl_with_selenium(self, url: str) -> Dict[str, Any]:
        """Crawl page using Selenium."""
        driver = None
        try:
            driver = self.setup_selenium_driver()
            driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Wait for body to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract comprehensive text data
            text_data = self.extract_text_content(soup)
            
            # Get all text content
            all_text = soup.get_text(separator=' ', strip=True)
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else "No title found"
            
            # Count words
            word_count = len(all_text.split())
            
            # Find new links
            new_links = []
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                normalized_url = self.normalize_url(href, url)
                if normalized_url and normalized_url not in self.crawled_urls:
                    new_links.append(normalized_url)
            
            return {
                'url': url,
                'success': True,
                'title': title_text,
                'word_count': word_count,
                'text_content': all_text[:5000],  # First 5000 chars
                'detailed_text': text_data,
                'new_links': new_links,
                'method': 'selenium'
            }
            
        except Exception as e:
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }
        finally:
            if driver:
                driver.quit()
    
    def crawl_website(self, start_url: str, use_selenium: bool = False, filter_config: ContentFilter = None) -> Dict[str, Any]:
        """Crawl entire website starting from given URL."""
        self.logger.info(f"Starting advanced crawl of: {start_url}")
        
        # Setup
        self.domain = urllib.parse.urlparse(start_url).netloc
        self.url_queue = [start_url]
        
        # Store filter configuration
        self.filter_config = filter_config
        
        # Check robots.txt
        if not self.check_robots_txt(start_url):
            self.logger.warning("Crawling not allowed by robots.txt")
            return {'error': 'Crawling not allowed by robots.txt'}
        
        page_count = 0
        
        while self.url_queue and page_count < self.max_pages:
            url = self.url_queue.pop(0)
            
            # Crawl the page
            page_data = self.crawl_page(url, use_selenium)
            
            if page_data and page_data.get('success'):
                self.pages_data.append(page_data)
                
                # Add new links to queue
                new_links = page_data.get('new_links', [])
                for link in new_links:
                    if link not in self.crawled_urls and link not in self.url_queue:
                        self.url_queue.append(link)
                
                page_count += 1
                self.logger.info(f"Successfully crawled page {page_count}: {url}")
                
                # Add delay between requests
                time.sleep(self.delay)
            else:
                self.logger.warning(f"Failed to crawl: {url}")
        
        # Generate comprehensive report
        # Apply smart filtering if configured
        if hasattr(self, 'filter_config') and self.filter_config:
            self.logger.info("Applying smart content filtering...")
            self.pages_data = self.smart_filter.filter_content(self.pages_data, self.filter_config)
            self.logger.info(f"Filtered to {len(self.pages_data)} pages")
        
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive crawling report."""
        if not self.pages_data:
            return {'error': 'No pages were successfully crawled'}
        
        # Calculate statistics
        total_words = sum(page.get('word_count', 0) for page in self.pages_data)
        total_links = sum(len(page.get('new_links', [])) for page in self.pages_data)
        total_images = sum(len(page.get('detailed_text', {}).get('images', [])) for page in self.pages_data)
        
        # Build site structure
        site_structure = {}
        for page in self.pages_data:
            url = page['url']
            path_parts = urllib.parse.urlparse(url).path.strip('/').split('/')
            
            current_level = site_structure
            for part in path_parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        # Content summary
        content_summary = {
            'total_pages': len(self.pages_data),
            'total_words': total_words,
            'total_links': total_links,
            'total_images': total_images,
            'average_words_per_page': total_words / len(self.pages_data) if self.pages_data else 0,
            'most_common_headings': self._get_most_common_headings(),
            'content_types': self._analyze_content_types()
        }
        
        # Metadata
        metadata = {
            'crawl_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'domain': self.domain,
            'max_pages': self.max_pages,
            'max_depth': self.max_depth,
            'delay': self.delay,
            'crawled_urls_count': len(self.crawled_urls)
        }
        
        return {
            'success': True,
            'metadata': metadata,
            'content_summary': content_summary,
            'site_structure': site_structure,
            'pages': self.pages_data,
            'statistics': {
                'total_pages': len(self.pages_data),
                'total_words': total_words,
                'total_links': total_links,
                'total_images': total_images
            }
        }
    
    def _get_most_common_headings(self) -> Dict[str, int]:
        """Get most common headings across all pages."""
        heading_counts = defaultdict(int)
        for page in self.pages_data:
            detailed_text = page.get('detailed_text', {})
            headings = detailed_text.get('headings', {})
            for heading_type, heading_list in headings.items():
                for heading in heading_list:
                    heading_counts[heading] += 1
        
        return dict(sorted(heading_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _analyze_content_types(self) -> Dict[str, int]:
        """Analyze content types across all pages."""
        content_types = defaultdict(int)
        for page in self.pages_data:
            detailed_text = page.get('detailed_text', {})
            for content_type, content_list in detailed_text.items():
                if isinstance(content_list, list):
                    content_types[content_type] += len(content_list)
                elif isinstance(content_list, dict):
                    content_types[content_type] += len(content_list)
        
        return dict(content_types)
    
    def save_to_json(self, filename: str = None) -> str:
        """Save crawling results to JSON file."""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"advanced_crawl_{self.domain}_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {filename}")
        return filename


# Example usage
if __name__ == "__main__":
    # Initialize advanced crawler
    crawler = AdvancedWebCrawler(max_pages=10, max_depth=2, delay=1.0)
    
    # Crawl a website
    result = crawler.crawl_website("https://httpbin.org/", use_selenium=False)
    
    # Save results
    filename = crawler.save_to_json()
    
    print(f"Crawling completed! Results saved to: {filename}")
    print(f"Pages crawled: {result['statistics']['total_pages']}")
    print(f"Total words: {result['statistics']['total_words']}") 