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
from typing import Dict, Any, Optional


class WebCrawler:
    def __init__(self):
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
        
    def setup_selenium_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with appropriate options for web scraping."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
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
    
    def crawl_with_requests(self, url: str) -> Dict[str, Any]:
        """Crawl website using requests library for static content."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else "No title found"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content') if meta_desc else "No description found"
            
            # Extract links
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            
            # Extract images
            images = [img.get('src') for img in soup.find_all('img', src=True)]
            
            return {
                'success': True,
                'url': url,
                'title': title_text,
                'description': description,
                'text_content': text_content[:5000],  # Limit text content
                'links': links[:50],  # Limit links
                'images': images[:20],  # Limit images
                'status_code': response.status_code,
                'method': 'requests'
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'method': 'requests'
            }
    
    def crawl_with_selenium(self, url: str, wait_time: int = 10) -> Dict[str, Any]:
        """Crawl website using Selenium for JavaScript-heavy sites."""
        driver = None
        try:
            driver = self.setup_selenium_driver()
            driver.get(url)
            
            # Wait for page to load
            time.sleep(wait_time)
            
            # Wait for body to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source after JavaScript execution
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else "No title found"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content') if meta_desc else "No description found"
            
            # Extract links
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            
            # Extract images
            images = [img.get('src') for img in soup.find_all('img', src=True)]
            
            # Get current URL (in case of redirects)
            current_url = driver.current_url
            
            return {
                'success': True,
                'url': url,
                'current_url': current_url,
                'title': title_text,
                'description': description,
                'text_content': text_content[:5000],  # Limit text content
                'links': links[:50],  # Limit links
                'images': images[:20],  # Limit images
                'method': 'selenium'
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'method': 'selenium'
            }
        finally:
            if driver:
                driver.quit()
    
    def crawl_website(self, url: str, use_selenium: bool = False) -> Dict[str, Any]:
        """Main method to crawl a website."""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Try requests first for static sites
        if not use_selenium:
            result = self.crawl_with_requests(url)
            if result['success']:
                return result
        
        # Use Selenium for JavaScript-heavy sites or if requests failed
        return self.crawl_with_selenium(url)
    
    def extract_specific_content(self, url: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract specific content using CSS selectors."""
        driver = None
        try:
            driver = self.setup_selenium_driver()
            driver.get(url)
            time.sleep(5)
            
            extracted_data = {}
            for key, selector in selectors.items():
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        extracted_data[key] = [elem.text for elem in elements]
                    else:
                        extracted_data[key] = []
                except Exception as e:
                    extracted_data[key] = f"Error extracting {key}: {str(e)}"
            
            return {
                'success': True,
                'url': url,
                'extracted_data': extracted_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
        finally:
            if driver:
                driver.quit()


# Example usage and testing
if __name__ == "__main__":
    crawler = WebCrawler()
    
    # Test with Perplexity.ai
    print("Crawling Perplexity.ai...")
    result = crawler.crawl_website("https://www.perplexity.ai/", use_selenium=True)
    
    print(json.dumps(result, indent=2, ensure_ascii=False)) 