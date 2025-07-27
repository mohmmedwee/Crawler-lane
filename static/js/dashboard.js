// Dashboard JavaScript for AI Web Crawler

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

// Sample data for demonstration
const sampleData = {
    quality_scores: [85, 78, 92, 65, 88, 75, 82, 90, 68, 85, 79, 91, 73, 87, 81],
    content_types: ['Article', 'Blog', 'Product', 'News', 'Review'],
    type_counts: [8, 6, 5, 4, 2],
    languages: ['English', 'Spanish', 'French', 'German', 'Italian'],
    language_counts: [12, 3, 2, 1, 1],
    sentiments: ['Positive', 'Neutral', 'Negative'],
    sentiment_counts: [8, 5, 2],
    word_counts: [150, 200, 300, 120, 450, 180, 250, 320, 90, 280],
    relevance_scores: [85, 92, 78, 88, 95, 82, 90, 87, 75, 89]
};

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadSampleData();
    createCharts();
});

// Initialize dashboard
function initializeDashboard() {
    console.log('🤖 AI Web Crawler Dashboard initialized');
    
    // Update metrics with sample data
    updateMetrics();
    
    // Set up real-time updates (simulated)
    setInterval(updateMetrics, 30000); // Update every 30 seconds
}

// Update dashboard metrics
function updateMetrics() {
    const totalPages = sampleData.quality_scores.length;
    const totalWords = sampleData.word_counts.reduce((a, b) => a + b, 0);
    const avgQuality = (sampleData.quality_scores.reduce((a, b) => a + b, 0) / totalPages).toFixed(1);
    const successRate = '90%';
    
    document.getElementById('totalPages').textContent = totalPages;
    document.getElementById('totalWords').textContent = totalWords.toLocaleString();
    document.getElementById('avgQuality').textContent = avgQuality;
    document.getElementById('successRate').textContent = successRate;
    
    // Update crawling stats
    document.getElementById('lastCrawl').textContent = new Date().toLocaleString();
    document.getElementById('pagesCrawled').textContent = totalPages;
    document.getElementById('avgSpeed').textContent = '2.5 pages/min';
}

// Create all charts
function createCharts() {
    createQualityChart();
    createTypeChart();
    createLanguageChart();
    createSentimentChart();
    createWordCountChart();
    createRelevanceChart();
}

// Create quality distribution chart
function createQualityChart() {
    const trace = {
        x: sampleData.quality_scores,
        type: 'histogram',
        name: 'Quality Scores',
        marker: {
            color: '#4facfe',
            line: {
                color: '#fff',
                width: 1
            }
        },
        nbinsx: 10
    };
    
    const layout = {
        title: {
            text: 'Content Quality Distribution',
            font: { size: 18, color: '#4facfe' }
        },
        xaxis: {
            title: 'Quality Score',
            range: [60, 100]
        },
        yaxis: {
            title: 'Number of Pages'
        },
        margin: { t: 50, b: 50, l: 50, r: 50 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('qualityChart', [trace], layout, {responsive: true});
}

// Create content type chart
function createTypeChart() {
    const trace = {
        labels: sampleData.content_types,
        values: sampleData.type_counts,
        type: 'pie',
        name: 'Content Types',
        marker: {
            colors: ['#4facfe', '#00f2fe', '#27ae60', '#f39c12', '#e74c3c']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    };
    
    const layout = {
        title: {
            text: 'Content Type Distribution',
            font: { size: 18, color: '#4facfe' }
        },
        margin: { t: 50, b: 50, l: 50, r: 50 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('typeChart', [trace], layout, {responsive: true});
}

// Create language distribution chart
function createLanguageChart() {
    const trace = {
        labels: sampleData.languages,
        values: sampleData.language_counts,
        type: 'pie',
        name: 'Languages',
        marker: {
            colors: ['#4facfe', '#00f2fe', '#27ae60', '#f39c12', '#e74c3c']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    };
    
    const layout = {
        title: {
            text: 'Language Distribution',
            font: { size: 16, color: '#4facfe' }
        },
        margin: { t: 40, b: 40, l: 40, r: 40 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('languageChart', [trace], layout, {responsive: true});
}

// Create sentiment analysis chart
function createSentimentChart() {
    const trace = {
        labels: sampleData.sentiments,
        values: sampleData.sentiment_counts,
        type: 'pie',
        name: 'Sentiments',
        marker: {
            colors: ['#27ae60', '#f39c12', '#e74c3c']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    };
    
    const layout = {
        title: {
            text: 'Sentiment Analysis',
            font: { size: 16, color: '#4facfe' }
        },
        margin: { t: 40, b: 40, l: 40, r: 40 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('sentimentChart', [trace], layout, {responsive: true});
}

// Create word count distribution chart
function createWordCountChart() {
    const trace = {
        x: sampleData.word_counts,
        type: 'histogram',
        name: 'Word Counts',
        marker: {
            color: '#27ae60',
            line: {
                color: '#fff',
                width: 1
            }
        },
        nbinsx: 8
    };
    
    const layout = {
        title: {
            text: 'Word Count Distribution',
            font: { size: 16, color: '#4facfe' }
        },
        xaxis: {
            title: 'Word Count'
        },
        yaxis: {
            title: 'Number of Pages'
        },
        margin: { t: 40, b: 50, l: 50, r: 20 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('wordCountChart', [trace], layout, {responsive: true});
}

// Create AI relevance score chart
function createRelevanceChart() {
    const trace = {
        x: ['Page 1', 'Page 2', 'Page 3', 'Page 4', 'Page 5', 'Page 6', 'Page 7', 'Page 8', 'Page 9', 'Page 10'],
        y: sampleData.relevance_scores,
        type: 'bar',
        name: 'AI Relevance Score',
        marker: {
            color: sampleData.relevance_scores.map(score => {
                if (score >= 90) return '#27ae60';
                if (score >= 80) return '#f39c12';
                return '#e74c3c';
            })
        }
    };
    
    const layout = {
        title: {
            text: 'AI Relevance Score by Page',
            font: { size: 16, color: '#4facfe' }
        },
        xaxis: {
            title: 'Pages'
        },
        yaxis: {
            title: 'Relevance Score',
            range: [70, 100]
        },
        margin: { t: 40, b: 50, l: 50, r: 20 },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('relevanceChart', [trace], layout, {responsive: true});
}

// Load sample data function
function loadSampleData() {
    console.log('📊 Loading sample data...');
    showMessage('Sample data loaded successfully!', 'success');
}

// Generate new visualizations function
function generateNewVisualizations() {
    console.log('🔄 Generating new visualizations...');
    
    // Simulate loading
    const container = document.getElementById('visualizationContainer');
    container.innerHTML = '<div class="message info">🔄 Generating new visualizations...</div>';
    
    setTimeout(() => {
        // Refresh charts with new data
        createCharts();
        container.innerHTML = `
            <div class="message success">✅ New visualizations generated!</div>
            <div class="visualization-grid">
                <div class="viz-card">
                    <h3>📈 Word Count Distribution</h3>
                    <div id="wordCountChart"></div>
                </div>
                <div class="viz-card">
                    <h3>🎯 AI Relevance Score</h3>
                    <div id="relevanceChart"></div>
                </div>
            </div>
        `;
        showMessage('New visualizations ready!', 'success');
    }, 2000);
}

// Show message utility
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    messageDiv.style.minWidth = '300px';
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Export data function
function exportData() {
    const data = {
        metrics: {
            totalPages: sampleData.quality_scores.length,
            totalWords: sampleData.word_counts.reduce((a, b) => a + b, 0),
            avgQuality: (sampleData.quality_scores.reduce((a, b) => a + b, 0) / sampleData.quality_scores.length).toFixed(1)
        },
        charts: {
            quality_scores: sampleData.quality_scores,
            content_types: sampleData.content_types,
            type_counts: sampleData.type_counts,
            languages: sampleData.languages,
            language_counts: sampleData.language_counts,
            sentiments: sampleData.sentiments,
            sentiment_counts: sampleData.sentiment_counts,
            word_counts: sampleData.word_counts,
            relevance_scores: sampleData.relevance_scores
        }
    };
    
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'dashboard_data.json';
    link.click();
    
    URL.revokeObjectURL(url);
    showMessage('Data exported successfully!', 'success');
}

// Real-time data update simulation
function simulateRealTimeUpdate() {
    // Add a new data point
    sampleData.quality_scores.push(Math.floor(Math.random() * 30) + 70);
    sampleData.word_counts.push(Math.floor(Math.random() * 400) + 100);
    sampleData.relevance_scores.push(Math.floor(Math.random() * 20) + 80);
    
    // Update charts
    createCharts();
    updateMetrics();
    
    showMessage('Real-time data updated!', 'info');
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case '1':
                e.preventDefault();
                switchTab('overview');
                break;
            case '2':
                e.preventDefault();
                switchTab('crawling');
                break;
            case '3':
                e.preventDefault();
                switchTab('analysis');
                break;
            case '4':
                e.preventDefault();
                switchTab('visualizations');
                break;
            case 'e':
                e.preventDefault();
                exportData();
                break;
            case 'r':
                e.preventDefault();
                generateNewVisualizations();
                break;
        }
    }
});

console.log('🎯 Dashboard JavaScript loaded successfully!'); 