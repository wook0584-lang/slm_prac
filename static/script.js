// Stock Analysis App - Frontend JavaScript

// Load trending stocks on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadTrendingStocks();

    // Enter key support
    document.getElementById('tickerInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeStock();
        }
    });
});

// Load trending stocks as chips
async function loadTrendingStocks() {
    try {
        const response = await fetch('/api/trending');
        const data = await response.json();

        const chipsContainer = document.getElementById('trendingChips');
        chipsContainer.innerHTML = '';

        data.trending.forEach(ticker => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.textContent = ticker;
            chip.onclick = () => {
                document.getElementById('tickerInput').value = ticker;
                analyzeStock();
            };
            chipsContainer.appendChild(chip);
        });
    } catch (error) {
        console.error('Error loading trending stocks:', error);
    }
}

// Main analysis function
async function analyzeStock() {
    const tickerInput = document.getElementById('tickerInput');
    const ticker = tickerInput.value.trim().toUpperCase();

    if (!ticker) {
        showError('Please enter a ticker symbol');
        return;
    }

    // Hide previous results and errors
    hideElements(['results', 'error']);
    showElement('loading');

    // Disable button
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker: ticker })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        showError(error.message || 'Failed to analyze stock. Please try again.');
        console.error('Analysis error:', error);
    } finally {
        hideElement('loading');
        analyzeBtn.disabled = false;
    }
}

// Display analysis results
function displayResults(data) {
    // Stock Info
    document.getElementById('stockName').textContent = `${data.ticker}`;
    document.getElementById('stockPrice').textContent = `$${data.current_price?.toFixed(2) || 'N/A'}`;

    const changeElement = document.getElementById('stockChange');
    const change = data.change_percent || 0;
    changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
    changeElement.className = `change ${change >= 0 ? 'positive' : 'negative'}`;

    // AI Analysis
    const sentimentBadge = document.getElementById('sentimentBadge');
    sentimentBadge.textContent = data.sentiment;
    sentimentBadge.className = `sentiment-badge ${data.sentiment}`;

    document.getElementById('aiSummary').textContent = data.summary;

    // News
    displayNews(data.news);

    // Show results
    showElement('results');

    // Smooth scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display news items
function displayNews(news) {
    const newsList = document.getElementById('newsList');
    newsList.innerHTML = '';

    if (!news || news.length === 0) {
        newsList.innerHTML = '<p style="color: #999;">No recent news available</p>';
        return;
    }

    news.forEach(item => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';

        const link = document.createElement('a');
        link.href = item.link;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';

        const title = document.createElement('div');
        title.className = 'news-title';
        title.textContent = item.title;

        const meta = document.createElement('div');
        meta.className = 'news-meta';
        meta.innerHTML = `
            <span class="news-source">${item.source}</span> •
            <span>${item.published}</span>
        `;

        link.appendChild(title);
        link.appendChild(meta);
        newsItem.appendChild(link);
        newsList.appendChild(newsItem);
    });
}

// Utility functions
function showError(message) {
    const errorElement = document.getElementById('error');
    errorElement.textContent = message;
    showElement('error');

    // Auto-hide after 5 seconds
    setTimeout(() => hideElement('error'), 5000);
}

function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

function hideElements(ids) {
    ids.forEach(id => hideElement(id));
}

// ===== PDF Analysis Functions =====

let selectedFile = null;

// Tab switching
function switchTab(tab) {
    // Hide all tabs
    hideElement('stockTab');
    hideElement('pdfTab');
    hideElement('results');
    hideElement('pdfResults');
    hideElement('error');

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    if (tab === 'stock') {
        showElement('stockTab');
        event.target.classList.add('active');
    } else if (tab === 'pdf') {
        showElement('pdfTab');
        event.target.classList.add('active');
    }
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {  // 10MB limit
        showError('File too large. Maximum size is 10MB');
        return;
    }

    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('analyzePdfBtn').disabled = false;
}

// Toggle stock context input
function toggleStockContext() {
    const checkbox = document.getElementById('useStockContext');
    const tickerInput = document.getElementById('contextTicker');

    if (checkbox.checked) {
        tickerInput.style.display = 'block';
    } else {
        tickerInput.style.display = 'none';
    }
}

// Analyze PDF with AI
async function analyzePDF() {
    if (!selectedFile) {
        showError('Please select a PDF file first');
        return;
    }

    // Hide previous results
    hideElements(['pdfResults', 'error']);
    showElement('loading');

    const analyzeBtn = document.getElementById('analyzePdfBtn');
    analyzeBtn.disabled = true;

    try {
        const useStockContext = document.getElementById('useStockContext').checked;
        const formData = new FormData();
        formData.append('file', selectedFile);

        let endpoint = '/api/analyze-pdf';
        let url = endpoint;

        if (useStockContext) {
            const ticker = document.getElementById('contextTicker').value.trim().toUpperCase();
            if (!ticker) {
                throw new Error('Please enter a ticker symbol for stock context');
            }
            endpoint = '/api/analyze-pdf-with-stock';
            formData.append('ticker', ticker);
            url = endpoint;
        } else {
            const analysisType = document.getElementById('analysisType').value;
            formData.append('analysis_type', analysisType);
        }

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'PDF analysis failed');
        }

        const data = await response.json();
        displayPDFResults(data);

    } catch (error) {
        showError(error.message || 'Failed to analyze PDF. Please try again.');
        console.error('PDF analysis error:', error);
    } finally {
        hideElement('loading');
        analyzeBtn.disabled = false;
    }
}

// Display PDF analysis results
function displayPDFResults(data) {
    document.getElementById('pdfFileName').textContent = `📄 ${data.filename}`;

    if (data.pages) {
        document.getElementById('pdfPages').textContent = `📑 ${data.pages} pages`;
    } else {
        document.getElementById('pdfPages').textContent = '';
    }

    if (data.ticker) {
        document.getElementById('pdfPages').textContent += ` | 📈 ${data.ticker}`;
    }

    document.getElementById('pdfAnalysisContent').textContent = data.analysis;

    // Show results
    showElement('pdfResults');

    // Smooth scroll to results
    document.getElementById('pdfResults').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
