// API Configuration
const API_BASE_URL = 'http://localhost:5000';
const API_PREDICT_ENDPOINT = '/api/predict';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const productNameInput = document.getElementById('productName');
const conditionSelect = document.getElementById('condition');
const usageMonthsInput = document.getElementById('usageMonths');
const warrantySelect = document.getElementById('warranty');
const originalPriceInput = document.getElementById('originalPrice');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

// Event Listeners
analyzeBtn.addEventListener('click', handleAnalyze);
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) handleAnalyze();
});

// Check API Health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('✅ API Health:', data);
        if (!data.api_configured) {
            showMessage('⚠️ Warning: Gemini API key not configured. Please set GEMINI_API_KEY environment variable.', 'bot');
        }
    } catch (error) {
        console.error('❌ API Connection Error:', error);
        showMessage('⚠️ Warning: Cannot connect to backend server. Make sure Flask app is running on port 5000.', 'bot');
    }
}

// Main Analysis Function
async function handleAnalyze() {
    // Validate inputs
    if (!productNameInput.value.trim()) {
        showMessage('❌ Please enter a product name', 'bot');
        return;
    }
    if (!conditionSelect.value) {
        showMessage('❌ Please select a condition', 'bot');
        return;
    }
    if (usageMonthsInput.value === '') {
        showMessage('❌ Please enter usage months', 'bot');
        return;
    }
    if (!warrantySelect.value) {
        showMessage('❌ Please select warranty option', 'bot');
        return;
    }
    if (!originalPriceInput.value) {
        showMessage('❌ Please enter original price', 'bot');
        return;
    }

    // Disable button and show loading
    analyzeBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';

    // Get form data
    const formData = {
        productName: productNameInput.value.trim(),
        condition: conditionSelect.value,
        usageMonths: parseInt(usageMonthsInput.value),
        warranty: warrantySelect.value,
        originalPrice: parseFloat(originalPriceInput.value)
    };

    // Display user input
    showMessage(`Analyzing: ${formData.productName} - Condition: ${formData.condition}, Usage: ${formData.usageMonths} months, Warranty: ${formData.warranty}, Original Price: $${formData.originalPrice.toFixed(2)}`, 'user');

    try {
        // Send data to backend API
        const response = await fetch(`${API_BASE_URL}${API_PREDICT_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            showMessage(`❌ Error: ${error.error || 'Unknown error occurred'}`, 'bot');
            return;
        }

        const result = await response.json();

        if (result.success) {
            displayResults(result.productData, result.prediction, result.aiInsights);
        } else {
            showMessage(`❌ Error: ${result.error || 'Analysis failed'}`, 'bot');
        }

    } catch (error) {
        console.error('Error:', error);
        showMessage(`❌ Connection Error: ${error.message}. Make sure the Flask server is running on port 5000.`, 'bot');
    } finally {
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Display Results
function displayResults(data, prediction, aiInsights) {
    // Create result message with all data
    const resultHTML = `
        <div class="prediction-result">
            <h3 style="color: #00695c; margin-bottom: 15px;">📊 Price Prediction Analysis</h3>
            
            <div class="result-row">
                <span class="result-label">Estimated Market Price:</span>
                <span class="result-value">$${prediction.estimatedMarketPrice.toFixed(2)}</span>
            </div>
            
            <div class="result-row">
                <span class="result-label">Online Market Price:</span>
                <span class="result-value">$${prediction.marketComparison.online.toFixed(2)}</span>
            </div>
            
            <div class="result-row">
                <span class="result-label">Retail Price Range:</span>
                <span class="result-value">$${prediction.marketComparison.retail.toFixed(2)}</span>
            </div>
            
            <div class="result-row">
                <span class="result-label">Wholesale Price:</span>
                <span class="result-value">$${prediction.marketComparison.wholesale.toFixed(2)}</span>
            </div>
            
            <div class="result-row">
                <span class="result-label">Total Depreciation:</span>
                <span class="result-value">${prediction.depreciation.percentageLoss}% ($${prediction.depreciation.priceLoss})</span>
            </div>
            
            <div class="result-row">
                <span class="result-label">Recommendation:</span>
                <span class="result-value">${prediction.recommendation}</span>
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 12px; background: #f5f5f5; border-radius: 6px; font-size: 0.95em; line-height: 1.6; color: #333;">
            <strong style="color: #667eea;">🤖 AI Market Insights (via Gemini):</strong><br/>
            ${aiInsights.split('\n').map(line => line.trim()).filter(line => line).join('<br/>')}
        </div>
    `;

    showMessage(resultHTML, 'bot', true);

    // Clear form
    setTimeout(() => {
        productNameInput.value = '';
        conditionSelect.value = '';
        usageMonthsInput.value = '';
        warrantySelect.value = '';
        originalPriceInput.value = '';
    }, 500);
}

// Show Message in Chat
function showMessage(content, sender, isHTML = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    if (isHTML) {
        messageContent.innerHTML = content;
    } else {
        messageContent.textContent = content;
    }

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    // Auto scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize on page load
window.addEventListener('load', () => {
    console.log('🚀 AI Market Price Predictor Frontend Loaded');
    console.log('📡 Backend URL:', API_BASE_URL);
    checkAPIHealth();
});