# 🤖 Crawler Lane

**Advanced AI-Powered Web Crawler for Text Extraction and Content Analysis**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/mohmmedwee/Crawler-lane?style=social)](https://github.com/mohmmedwee/Crawler-lane)

---

## 👨‍💻 **About the Developer**

**Mohmmed Eloustah** - FullStack Developer from Amman, Jordan

I'm a passionate FullStack Developer working in Web development. I enjoy turning complex problems into simple, beautiful and intuitive designs. This project represents my commitment to creating powerful, user-friendly tools that make web scraping and content analysis accessible to everyone.

---

## 🚀 **Quick Start**

### **1. Clone the Repository**
```bash
git clone https://github.com/mohmmedwee/Crawler-lane.git
cd Crawler-lane/crawler
```

### **2. Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Start the Server**
```bash
python api.py
```

### **5. Access the Application**
- **Main Interface**: http://localhost:8080
- **Dashboard**: http://localhost:8080/dashboard
- **Health Check**: http://localhost:8080/health

---

## 🎯 **Features**

### **🌐 Web Crawling**
- **Basic Crawler** - Simple HTTP requests for quick text extraction
- **Advanced Crawler** - Selenium-based crawling for JavaScript-heavy sites
- **Smart Filter** - AI-powered content filtering and quality analysis

### **🧠 AI-Powered Analysis**
- **Content Quality Assessment** - Automatic quality scoring
- **Language Detection** - Multi-language support
- **Sentiment Analysis** - Content sentiment evaluation
- **Duplicate Detection** - Intelligent content deduplication
- **Topic Modeling** - Automatic content categorization

### **📊 Data Visualization**
- **Interactive Dashboards** - Real-time metrics and charts
- **Content Analysis Reports** - Comprehensive data insights
- **Export Capabilities** - JSON, CSV, and HTML reports
- **Custom Visualizations** - Plotly.js powered charts

### **🎨 Modern Web Interface**
- **Responsive Design** - Works on all devices
- **Real-time Updates** - Live data visualization
- **Professional UI** - Beautiful, intuitive interface
- **Mobile-Friendly** - Touch-optimized experience

---

## 🏗️ **Project Structure**

```
Crawler-lane/
├── crawler/                    # Main application directory
│   ├── templates/              # HTML templates
│   │   ├── index.html         # Main interface
│   │   └── dashboard.html     # Dashboard
│   ├── static/                # Static assets
│   │   ├── css/
│   │   │   ├── style.css      # Main styles
│   │   │   └── dashboard.css  # Dashboard styles
│   │   └── js/
│   │       ├── script.js      # Main JavaScript
│   │       └── dashboard.js   # Dashboard JavaScript
│   ├── examples/              # Sample data and outputs
│   ├── demos/                 # Demo scripts
│   ├── api.py                 # Flask web server
│   ├── crawler.py             # Basic web crawler
│   ├── advanced_crawler.py    # Advanced Selenium crawler
│   ├── smart_filter.py        # AI content filtering
│   ├── visualization_dashboard.py  # Data visualization
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Detailed documentation
├── LICENSE                    # MIT License
└── .gitignore                # Git ignore rules
```

---

## 🔧 **API Endpoints**

### **Web Crawling**
- `POST /crawl` - Basic web crawling
- `POST /advanced-crawl` - Advanced Selenium crawling
- `POST /smart-filter-crawl` - AI-powered content filtering

### **Data Visualization**
- `POST /visualize` - Generate data visualizations
- `GET /dashboard` - Interactive dashboard

### **System**
- `GET /health` - Health check endpoint

---

## 📊 **Usage Examples**

### **Basic Crawling**
```python
import requests

response = requests.post('http://localhost:8080/crawl', json={
    'url': 'https://example.com',
    'max_pages': 10
})

print(response.json())
```

### **Advanced Crawling with Selenium**
```python
response = requests.post('http://localhost:8080/advanced-crawl', json={
    'url': 'https://example.com',
    'max_pages': 20,
    'wait_time': 3,
    'headless': True
})
```

### **Smart Content Filtering**
```python
response = requests.post('http://localhost:8080/smart-filter-crawl', json={
    'url': 'https://example.com',
    'max_pages': 15,
    'min_quality': 70,
    'content_types': ['article', 'blog'],
    'languages': ['en']
})
```

---

## 🎨 **Screenshots**

### **Main Interface**
![Main Interface](https://via.placeholder.com/800x400/4facfe/ffffff?text=Main+Interface)

### **Dashboard**
![Dashboard](https://via.placeholder.com/800x400/00f2fe/ffffff?text=Interactive+Dashboard)

### **Visualizations**
![Visualizations](https://via.placeholder.com/800x400/27ae60/ffffff?text=Data+Visualizations)

---

## 🛠️ **Installation**

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package installer)
- Git

### **Step-by-Step Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mohmmedwee/Crawler-lane.git
   cd Crawler-lane/crawler
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python test_installation.py
   ```

5. **Start the Server**
   ```bash
   python api.py
   ```

---

## 🧪 **Testing**

### **Run All Tests**
```bash
python test_installation.py
python test_templates.py
python demos/final_demo.py
```

### **Test Individual Components**
```bash
# Test basic functionality
python -c "from crawler import WebCrawler; print('✅ Basic crawler working')"

# Test advanced crawler
python -c "from advanced_crawler import AdvancedWebCrawler; print('✅ Advanced crawler working')"

# Test smart filter
python -c "from smart_filter import SmartContentFilter; print('✅ Smart filter working')"
```

---

## 📈 **Performance**

### **Crawling Speed**
- **Basic Crawler**: ~50-100 pages/minute
- **Advanced Crawler**: ~20-50 pages/minute (with Selenium)
- **Smart Filter**: ~30-70 pages/minute (with AI analysis)

### **Memory Usage**
- **Light Mode**: ~100-200 MB RAM
- **Heavy Mode**: ~500-1000 MB RAM (with large datasets)

### **Supported Formats**
- **Input**: URLs, HTML files, JSON data
- **Output**: JSON, CSV, HTML reports, interactive charts

---

## 🤝 **Contributing**

We welcome contributions! Please feel free to submit a Pull Request.

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

### **Code Style**
- Follow PEP 8 Python style guide
- Add docstrings to all functions
- Include type hints where possible
- Write comprehensive tests

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Flask** - Web framework
- **Selenium** - Web automation
- **BeautifulSoup** - HTML parsing
- **Plotly** - Data visualization
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

---

## 📞 **Contact**

**Mohmmed Eloustah**
- **Location**: Amman, Jordan
- **GitHub**: [@mohmmedwee](https://github.com/mohmmedwee)
- **Project**: [Crawler Lane](https://github.com/mohmmedwee/Crawler-lane)

---

## ⭐ **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=mohmmedwee/Crawler-lane&type=Date)](https://star-history.com/#mohmmedwee/Crawler-lane&Date)

---

**Made with ❤️ by Mohmmed Eloustah in Amman, Jordan** 