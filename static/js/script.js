// Tab switching functionality
function switchTab(tabName) {
    // Hide all tab panels
    const tabPanels = document.querySelectorAll('.tab-panel');
    tabPanels.forEach(panel => {
        panel.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab panel
    const selectedPanel = document.getElementById(tabName);
    if (selectedPanel) {
        selectedPanel.classList.add('active');
    }
    
    // Add active class to clicked tab button
    const clickedButton = document.querySelector(`[data-tab="${tabName}"]`);
    if (clickedButton) {
        clickedButton.classList.add('active');
    }
}

// Clear result function
function clearResult(tabName) {
    const resultPanel = document.getElementById(`${tabName}Result`);
    const output = document.getElementById(`${tabName}Output`);
    if (resultPanel && output) {
        resultPanel.style.display = 'none';
        output.innerHTML = '';
    }
}

// Show message function
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = message;
    
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Add new message
    const activePanel = document.querySelector('.tab-panel.active');
    if (activePanel) {
        activePanel.insertBefore(messageDiv, activePanel.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Show/hide loading overlay
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Basic Crawler
document.getElementById('basicForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const url = document.getElementById('basicUrl').value;
    const resultDiv = document.getElementById('basicResult');
    const outputDiv = document.getElementById('basicOutput');
    
    if (!url) {
        showMessage('Please enter a valid URL', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const totalWords = result.total_words || 0;
            const avgQuality = result.avg_quality_score || 0;
            
            outputDiv.innerHTML = `
                <div class="crawl-results">
                    <h4><i class="fas fa-check-circle"></i> Basic Crawl Results</h4>
                    <p><strong>URL:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>
                    <p><strong>Title:</strong> ${result.title || 'No title'}</p>
                    <p><strong>Word Count:</strong> ${totalWords}</p>
                    <p><strong>Quality Score:</strong> ${avgQuality.toFixed(2)}</p>
                    <p><strong>Status Code:</strong> ${result.status_code || 'N/A'}</p>
                    <p><strong>Method:</strong> ${result.method || 'requests'}</p>
                    <div class="download-section">
                        <button onclick="downloadResults(${JSON.stringify(result).replace(/"/g, '&quot;')}, 'basic_crawl')" class="download-btn">
                            <i class="fas fa-download"></i> Download JSON
                        </button>
                    </div>
                </div>
                <div class="page-item">
                    <h5>Content Preview</h5>
                    <p><strong>Text Content:</strong></p>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; max-height: 200px; overflow-y: auto; font-size: 0.9rem; line-height: 1.5;">
                        ${result.text_content ? result.text_content.substring(0, 500) + '...' : 'No content available'}
                    </div>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `
                <div class="message error">
                    <i class="fas fa-exclamation-triangle"></i> Error: ${result.error || 'Unknown error occurred'}
                </div>
            `;
        }
        
        resultDiv.style.display = 'block';
        
    } catch (error) {
        outputDiv.innerHTML = `
            <div class="message error">
                <i class="fas fa-exclamation-triangle"></i> Network error: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        hideLoading();
    }
});

// Advanced Crawler
document.getElementById('advancedForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const url = document.getElementById('advancedUrl').value;
    const maxPages = parseInt(document.getElementById('advancedMaxPages').value) || 5;
    const waitTime = parseInt(document.getElementById('advancedWaitTime').value) || 1;
    const headless = document.getElementById('advancedHeadless').checked;
    const resultDiv = document.getElementById('advancedResult');
    const outputDiv = document.getElementById('advancedOutput');
    
    if (!url) {
        showMessage('Please enter a valid URL', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/advanced-crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                max_pages: maxPages,
                wait_time: waitTime,
                headless: headless
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const pages = result.pages || [result];
            const totalPages = pages.length;
            const totalWords = result.total_words || 0;
            const avgQuality = result.avg_quality_score || 0;
            const totalLinks = pages.reduce((sum, page) => sum + (page.links || []).length, 0);
            const totalImages = pages.reduce((sum, page) => sum + (page.images || []).length, 0);
            
            outputDiv.innerHTML = `
                <div class="crawl-results">
                    <h4><i class="fas fa-chart-line"></i> Advanced Crawl Analytics</h4>
                    <p><strong>Pages Crawled:</strong> ${totalPages}</p>
                    <p><strong>Total Words:</strong> ${totalWords}</p>
                    <p><strong>Average Quality Score:</strong> ${avgQuality.toFixed(2)}</p>
                    <p><strong>Total Links Found:</strong> ${totalLinks}</p>
                    <p><strong>Total Images Found:</strong> ${totalImages}</p>
                    <p><strong>Execution Time:</strong> ${result.execution_time || 'N/A'}s</p>
                    <p><strong>Status Code:</strong> ${result.status_code || 'N/A'}</p>
                    <div class="download-section">
                        <button onclick="downloadResults(${JSON.stringify(result).replace(/"/g, '&quot;')}, 'advanced_crawl')" class="download-btn">
                            <i class="fas fa-download"></i> Download JSON
                        </button>
                    </div>
                </div>
                <div class="crawl-details">
                    <h4><i class="fas fa-list"></i> Pages Details (${totalPages} pages)</h4>
                    ${pages.map((page, index) => `
                        <div class="page-item">
                            <h5>${index + 1}. ${page.title || 'No Title'}</h5>
                            <p><strong>URL:</strong> <a href="${page.url}" target="_blank">${page.url}</a></p>
                            <p><strong>Word Count:</strong> ${page.word_count || page.total_words || 0}</p>
                            <p><strong>Quality Score:</strong> ${page.quality_score || page.avg_quality_score || 0}</p>
                            <p><strong>Description:</strong> ${page.description || 'No description'}</p>
                            <p><strong>Links Found:</strong> ${(page.links || []).length}</p>
                            <p><strong>Images Found:</strong> ${(page.images || []).length}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            outputDiv.innerHTML = `
                <div class="message error">
                    <i class="fas fa-exclamation-triangle"></i> Error: ${result.error || 'Unknown error occurred'}
                </div>
            `;
        }
        
        resultDiv.style.display = 'block';
        
    } catch (error) {
        outputDiv.innerHTML = `
            <div class="message error">
                <i class="fas fa-exclamation-triangle"></i> Network error: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        hideLoading();
    }
});

// Smart Filter Crawler
document.getElementById('smartForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const url = document.getElementById('smartUrl').value;
    const maxPages = parseInt(document.getElementById('smartMaxPages').value) || 5;
    const minQuality = parseInt(document.getElementById('smartMinQuality').value) || 70;
    const contentTypes = Array.from(document.getElementById('smartContentTypes').selectedOptions).map(option => option.value);
    const languages = Array.from(document.getElementById('smartLanguages').selectedOptions).map(option => option.value);
    const resultDiv = document.getElementById('smartResult');
    const outputDiv = document.getElementById('smartOutput');
    
    if (!url) {
        showMessage('Please enter a valid URL', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/smart-filter-crawl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                max_pages: maxPages,
                min_quality: minQuality,
                content_types: contentTypes,
                languages: languages
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const pages = result.pages || [result];
            const totalPages = pages.length;
            const totalWords = result.total_words || 0;
            const avgQuality = result.avg_quality_score || 0;
            const filteredPages = result.filtered_pages || totalPages;
            
            outputDiv.innerHTML = `
                <div class="crawl-results">
                    <h4><i class="fas fa-brain"></i> Smart Filter Results</h4>
                    <p><strong>Total Pages Crawled:</strong> ${totalPages}</p>
                    <p><strong>Pages After Filtering:</strong> ${filteredPages}</p>
                    <p><strong>Total Words:</strong> ${totalWords}</p>
                    <p><strong>Average Quality Score:</strong> ${avgQuality.toFixed(2)}</p>
                    <p><strong>Content Types:</strong> ${result.content_types ? result.content_types.join(', ') : 'All'}</p>
                    <p><strong>Languages:</strong> ${result.languages ? result.languages.join(', ') : 'All'}</p>
                    <p><strong>Minimum Quality Threshold:</strong> ${minQuality}</p>
                    <div class="download-section">
                        <button onclick="downloadResults(${JSON.stringify(result).replace(/"/g, '&quot;')}, 'smart_filter_crawl')" class="download-btn">
                            <i class="fas fa-download"></i> Download JSON
                        </button>
                    </div>
                </div>
                <div class="crawl-details">
                    <h4><i class="fas fa-filter"></i> Filtered Pages (${filteredPages} pages)</h4>
                    ${pages.map((page, index) => `
                        <div class="page-item">
                            <h5>${index + 1}. ${page.title || 'No Title'}</h5>
                            <p><strong>URL:</strong> <a href="${page.url}" target="_blank">${page.url}</a></p>
                            <p><strong>Word Count:</strong> ${page.word_count || page.total_words || 0}</p>
                            <p><strong>Quality Score:</strong> ${page.quality_score || page.avg_quality_score || 0}</p>
                            <p><strong>Content Type:</strong> ${page.content_type || 'Unknown'}</p>
                            <p><strong>Language:</strong> ${page.language || 'Unknown'}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            outputDiv.innerHTML = `
                <div class="message error">
                    <i class="fas fa-exclamation-triangle"></i> Error: ${result.error || 'Unknown error occurred'}
                </div>
            `;
        }
        
        resultDiv.style.display = 'block';
        
    } catch (error) {
        outputDiv.innerHTML = `
            <div class="message error">
                <i class="fas fa-exclamation-triangle"></i> Network error: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        hideLoading();
    }
});

// Visualizations
async function generateVisualizations() {
    const data = document.getElementById('visualizationData').value;
    const resultDiv = document.getElementById('visualizationResult');
    const outputDiv = document.getElementById('visualizationOutput');
    
    if (!data) {
        showMessage('Please enter crawl data for visualization', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/visualize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crawl_data: JSON.parse(data)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputDiv.innerHTML = `
                <div class="crawl-results">
                    <h4><i class="fas fa-chart-bar"></i> Generated Visualizations</h4>
                    <p><strong>Visualizations Created:</strong> ${result.visualizations ? result.visualizations.length : 0}</p>
                    <p><strong>Message:</strong> ${result.message}</p>
                    <div class="download-section">
                        <button onclick="window.open('/dashboard', '_blank')" class="download-btn">
                            <i class="fas fa-external-link-alt"></i> View Dashboard
                        </button>
                    </div>
                </div>
            `;
        } else {
            outputDiv.innerHTML = `
                <div class="message error">
                    <i class="fas fa-exclamation-triangle"></i> Error: ${result.error || 'Unknown error occurred'}
                </div>
            `;
        }
        
        resultDiv.style.display = 'block';
        
    } catch (error) {
        outputDiv.innerHTML = `
            <div class="message error">
                <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    } finally {
        hideLoading();
    }
}

// Download results as JSON file
async function downloadResults(crawlData, crawlType) {
    try {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const filename = `${crawlType}_${timestamp}.json`;
        
        const response = await fetch('/download-json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crawl_data: crawlData,
                filename: filename
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Create a download link for the file
            const blob = new Blob([JSON.stringify(crawlData, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showMessage(`✅ ${result.message}`, 'success');
        } else {
            showMessage(`❌ Download failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showMessage(`❌ Download error: ${error.message}`, 'error');
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set up tab button event listeners
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
    
    // Add some sample data to visualization textarea
    const visualizationData = document.getElementById('visualizationData');
    if (visualizationData && !visualizationData.value) {
        visualizationData.value = JSON.stringify({
            urls: ["https://example.com"],
            pages: [{
                url: "https://example.com",
                title: "Example Page",
                content: "This is sample content for visualization testing.",
                word_count: 100,
                quality_score: 85
            }]
        }, null, 2);
    }
    
    console.log('Crawler Lane initialized successfully!');
}); 