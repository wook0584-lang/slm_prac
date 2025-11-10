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
