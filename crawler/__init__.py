#!/usr/bin/env python3
"""
Crawler Lane - Advanced AI-Powered Web Crawler for Text Extraction and Content Analysis

A sophisticated web crawler designed for AI text extraction, content analysis, 
and machine learning data preparation with intelligent filtering and visualization.

Author: Mohmmed Eloustah
GitHub: https://github.com/mohmmedwee/Crawler-lane
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Mohmmed Eloustah"
__email__ = "mohmmed.eloustah@gmail.com"
__description__ = "Advanced AI-Powered Web Crawler for Text Extraction and Content Analysis"
__url__ = "https://github.com/mohmmedwee/Crawler-lane"
__license__ = "MIT"

# Import core classes
from .crawler import WebCrawler
from .advanced_crawler import AdvancedWebCrawler
from .smart_filter import SmartContentFilter, ContentFilter, ContentType, ContentQuality
from .visualization_dashboard import DataVisualizationDashboard

# Import Flask app if available
try:
    from .api import app
except ImportError:
    app = None

# Define what gets imported with "from crawler import *"
__all__ = [
    # Core classes
    'WebCrawler',
    'AdvancedWebCrawler', 
    'SmartContentFilter',
    'ContentFilter',
    'ContentType',
    'ContentQuality',
    'DataVisualizationDashboard',
    
    # Flask app
    'app',
    
    # Metadata
    '__version__',
    '__author__',
    '__email__',
    '__description__',
    '__url__',
    '__license__',
]

# Package initialization message
print(f"🤖 Crawler Lane v{__version__} loaded successfully!")
print(f"👨‍💻 Developed by {__author__} from Amman, Jordan")
print(f"🌐 GitHub: {__url__}")
print(f"📄 License: {__license__}")
print("🚀 Ready for web crawling and content analysis!") 