# 🚀 Quick Start Guide - Crawler Lane

## ⚡ **Get Started in 5 Minutes**

### **1. Clone the Repository**
```bash
git clone https://github.com/mohmmedwee/Crawler-lane.git
cd Crawler-lane
```

### **2. Set Up Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Start the Server**
```bash
python api.py
```

### **4. Access the Application**
- **Main Interface**: http://localhost:8080
- **Dashboard**: http://localhost:8080/dashboard
- **Health Check**: http://localhost:8080/health

---

## 🎯 **Quick Test**

### **Test Installation**
```bash
python test_installation.py
```

### **Test Web Interface**
```bash
curl http://localhost:8080/health
```

### **Test Basic Crawling**
```bash
curl -X POST http://localhost:8080/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "max_pages": 1}'
```

---

## 🔧 **Troubleshooting**

### **Python Version Issue**
If you get syntax errors, make sure you're using Python 3.6+:
```bash
python --version  # Should be 3.6 or higher
```

### **Virtual Environment**
Always activate the virtual environment:
```bash
source venv/bin/activate  # You should see (venv) in your prompt
```

### **Missing Dependencies**
If you get import errors:
```bash
pip install -r requirements.txt
pip install fake-useragent  # If still missing
```

---

## 📊 **Features to Try**

### **1. Basic Crawling**
- Visit http://localhost:8080
- Go to "Basic Crawler" tab
- Enter a URL and click "Crawl"

### **2. Advanced Crawling**
- Go to "Advanced Crawler" tab
- Use Selenium for JavaScript-heavy sites

### **3. Smart Filtering**
- Go to "Smart Filter" tab
- Set quality thresholds and content types

### **4. Data Visualization**
- Go to "Visualizations" tab
- Generate interactive charts and reports

---

## 🎨 **What You'll See**

### **Main Interface**
- Clean, modern web interface
- Four tabs: Basic, Advanced, Smart Filter, Visualizations
- Real-time results and progress indicators

### **Dashboard**
- Interactive charts and metrics
- Content analysis visualizations
- Performance statistics

### **API Endpoints**
- RESTful API for programmatic access
- JSON responses with detailed data
- Health check endpoint

---

## 🚀 **Next Steps**

1. **Explore the Code**: Check out `crawler.py`, `smart_filter.py`, etc.
2. **Run Demos**: Try `python demos/final_demo.py`
3. **Customize**: Modify filters and settings in the web interface
4. **Extend**: Add your own crawling logic or visualizations

---

**🎯 Ready to start crawling? Run `python api.py` and visit http://localhost:8080!**

**Made with ❤️ by Mohmmed Eloustah in Amman, Jordan** 