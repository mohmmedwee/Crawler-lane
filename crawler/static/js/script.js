// Main JavaScript for AI Web Crawler Interface

// Tab switching functionality
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Basic crawler form
    const basicForm = document.getElementById('basicForm');
    if (basicForm) {
        basicForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleBasicCrawl();
        });
    }
    
    // Advanced crawler form
    const advancedForm = document.getElementById('advancedForm');
    if (advancedForm) {
        advancedForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleAdvancedCrawl();
        });
    }
    
    // Smart filter form
    const smartForm = document.getElementById('smartForm');
    if (smartForm) {
        smartForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleSmartFilter();
        });
    }
});

// Basic crawler handler
async function handleBasicCrawl() {
    const form = document.getElementById('basicForm');
    const resultDiv = document.getElementById('basicResult');
    const outputDiv = document.getElementById('basicOutput');
    
    // Show loading state
    form.classList.add('loading');
    resultDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="message info">⏳ Crawling in progress...</div>';
    
    try {
        const formData = new FormData(form);
        const data = {
            url: formData.get('url'),
            max_pages: parseInt(formData.get('max_pages'))
        };
        
        const response = await fetch('/crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.innerHTML = `
                <div class="message success">✅ Crawling completed successfully!</div>
                <div class="crawl-results">
                    <h4>📊 Crawl Summary</h4>
                    <p><strong>Pages Crawled:</strong> ${result.pages.length}</p>
                    <p><strong>Total Words:</strong> ${result.total_words}</p>
                    <p><strong>Average Quality Score:</strong> ${result.avg_quality_score.toFixed(2)}</p>
                </div>
                <div class="crawl-details">
                    <h4>📄 Page Details</h4>
                    <div class="page-list">
                        ${result.pages.map(page => `
                            <div class="page-item">
                                <h5>${page.title || 'No Title'}</h5>
                                <p><strong>URL:</strong> <a href="${page.url}" target="_blank">${page.url}</a></p>
                                <p><strong>Word Count:</strong> ${page.word_count}</p>
                                <p><strong>Quality Score:</strong> ${page.quality_score}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `<div class="message error">❌ Error: ${result.error}</div>`;
        }
    } catch (error) {
        outputDiv.innerHTML = `<div class="message error">❌ Network error: ${error.message}</div>`;
    } finally {
        form.classList.remove('loading');
    }
}

// Advanced crawler handler
async function handleAdvancedCrawl() {
    const form = document.getElementById('advancedForm');
    const resultDiv = document.getElementById('advancedResult');
    const outputDiv = document.getElementById('advancedOutput');
    
    // Show loading state
    form.classList.add('loading');
    resultDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="message info">⏳ Advanced crawling in progress...</div>';
    
    try {
        const formData = new FormData(form);
        const data = {
            url: formData.get('url'),
            max_pages: parseInt(formData.get('max_pages')),
            wait_time: parseInt(formData.get('wait_time')),
            headless: formData.get('headless') === 'on'
        };
        
        const response = await fetch('/advanced-crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.innerHTML = `
                <div class="message success">✅ Advanced crawling completed successfully!</div>
                <div class="crawl-results">
                    <h4>📊 Crawl Summary</h4>
                    <p><strong>Pages Crawled:</strong> ${result.pages.length}</p>
                    <p><strong>Total Words:</strong> ${result.total_words}</p>
                    <p><strong>Average Quality Score:</strong> ${result.avg_quality_score.toFixed(2)}</p>
                    <p><strong>Execution Time:</strong> ${result.execution_time}s</p>
                </div>
                <div class="crawl-details">
                    <h4>📄 Page Details</h4>
                    <div class="page-list">
                        ${result.pages.map(page => `
                            <div class="page-item">
                                <h5>${page.title || 'No Title'}</h5>
                                <p><strong>URL:</strong> <a href="${page.url}" target="_blank">${page.url}</a></p>
                                <p><strong>Word Count:</strong> ${page.word_count}</p>
                                <p><strong>Quality Score:</strong> ${page.quality_score}</p>
                                <p><strong>Load Time:</strong> ${page.load_time}ms</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `<div class="message error">❌ Error: ${result.error}</div>`;
        }
    } catch (error) {
        outputDiv.innerHTML = `<div class="message error">❌ Network error: ${error.message}</div>`;
    } finally {
        form.classList.remove('loading');
    }
}

// Smart filter handler
async function handleSmartFilter() {
    const form = document.getElementById('smartForm');
    const resultDiv = document.getElementById('smartResult');
    const outputDiv = document.getElementById('smartOutput');
    
    // Show loading state
    form.classList.add('loading');
    resultDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="message info">🧠 Smart filtering in progress...</div>';
    
    try {
        const formData = new FormData(form);
        const data = {
            url: formData.get('url'),
            max_pages: parseInt(formData.get('max_pages')),
            min_quality: parseInt(formData.get('min_quality')),
            content_types: Array.from(form.querySelectorAll('select[name="content_types"] option:checked')).map(opt => opt.value),
            languages: Array.from(form.querySelectorAll('select[name="languages"] option:checked')).map(opt => opt.value)
        };
        
        const response = await fetch('/smart-filter-crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.innerHTML = `
                <div class="message success">✅ Smart filtering completed successfully!</div>
                <div class="crawl-results">
                    <h4>🧠 Smart Filter Summary</h4>
                    <p><strong>Pages Crawled:</strong> ${result.pages.length}</p>
                    <p><strong>Pages Filtered:</strong> ${result.filtered_pages}</p>
                    <p><strong>Total Words:</strong> ${result.total_words}</p>
                    <p><strong>Average Quality Score:</strong> ${result.avg_quality_score.toFixed(2)}</p>
                    <p><strong>Content Types Found:</strong> ${result.content_types.join(', ')}</p>
                    <p><strong>Languages Detected:</strong> ${result.languages.join(', ')}</p>
                </div>
                <div class="crawl-details">
                    <h4>📄 Filtered Page Details</h4>
                    <div class="page-list">
                        ${result.pages.map(page => `
                            <div class="page-item">
                                <h5>${page.title || 'No Title'}</h5>
                                <p><strong>URL:</strong> <a href="${page.url}" target="_blank">${page.url}</a></p>
                                <p><strong>Content Type:</strong> ${page.content_type}</p>
                                <p><strong>Language:</strong> ${page.language}</p>
                                <p><strong>Quality Score:</strong> ${page.quality_score}</p>
                                <p><strong>Sentiment:</strong> ${page.sentiment}</p>
                                <p><strong>Word Count:</strong> ${page.word_count}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `<div class="message error">❌ Error: ${result.error}</div>`;
        }
    } catch (error) {
        outputDiv.innerHTML = `<div class="message error">❌ Network error: ${error.message}</div>`;
    } finally {
        form.classList.remove('loading');
    }
}

// Visualization generator
async function generateVisualizations() {
    const dataTextarea = document.getElementById('visualizationData');
    const resultDiv = document.getElementById('visualizationResult');
    const outputDiv = document.getElementById('visualizationOutput');
    
    if (!dataTextarea.value.trim()) {
        alert('Please enter crawl data in JSON format');
        return;
    }
    
    try {
        const crawlData = JSON.parse(dataTextarea.value);
        
        // Show loading state
        resultDiv.style.display = 'block';
        outputDiv.innerHTML = '<div class="message info">📊 Generating visualizations...</div>';
        
        const response = await fetch('/visualize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ crawl_data: crawlData })
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.innerHTML = `
                <div class="message success">✅ Visualizations generated successfully!</div>
                <div class="visualization-files">
                    <h4>📁 Generated Files</h4>
                    <ul>
                        ${Object.entries(result.visualizations).map(([key, filename]) => `
                            <li><strong>${key}:</strong> <a href="/examples/${filename}" target="_blank">${filename}</a></li>
                        `).join('')}
                    </ul>
                </div>
                <div class="visualization-preview">
                    <h4>📊 Preview</h4>
                    <p>Click on the links above to view the generated visualizations in your browser.</p>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `<div class="message error">❌ Error: ${result.error}</div>`;
        }
    } catch (error) {
        if (error instanceof SyntaxError) {
            outputDiv.innerHTML = `<div class="message error">❌ Invalid JSON format. Please check your data.</div>`;
        } else {
            outputDiv.innerHTML = `<div class="message error">❌ Network error: ${error.message}</div>`;
        }
    }
}

// Utility functions
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Add some sample data for testing
function loadSampleData() {
    const sampleData = {
        "urls": ["https://example.com"],
        "pages": [
            {
                "url": "https://example.com/article1",
                "title": "Sample Article 1",
                "content": "This is a sample article about AI and machine learning.",
                "word_count": 150,
                "quality_score": 85,
                "content_type": "Article",
                "language": "en",
                "sentiment": "positive"
            },
            {
                "url": "https://example.com/article2",
                "title": "Sample Article 2",
                "content": "Another sample article about web crawling and data extraction.",
                "word_count": 200,
                "quality_score": 78,
                "content_type": "Article",
                "language": "en",
                "sentiment": "neutral"
            }
        ]
    };
    
    const textarea = document.getElementById('visualizationData');
    if (textarea) {
        textarea.value = JSON.stringify(sampleData, null, 2);
        showMessage('Sample data loaded!', 'success');
    }
} 