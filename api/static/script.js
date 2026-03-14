document.addEventListener('DOMContentLoaded', () => {
    const tickerInput = document.getElementById('tickerInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const predictBtn = document.getElementById('predictBtn');
    const analysisSection = document.getElementById('analysisSection');
    const analysisContent = document.getElementById('analysisContent');
    const predictionSection = document.getElementById('predictionSection');
    const predictionGrid = document.getElementById('predictionGrid');
    const loading = document.getElementById('loading');

    analyzeBtn.addEventListener('click', async () => {
        const tickers = tickerInput.value.split(',').map(t => t.trim().toUpperCase()).filter(t => t);
        if (tickers.length === 0) {
            alert('Please enter at least one ticker');
            return;
        }

        // Reset UI
        analysisSection.style.display = 'none';
        predictionSection.style.display = 'none';
        loading.style.display = 'block';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/stock_market/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tickers })
            });

            const data = await response.json();
            
            if (response.ok) {
                // Formatting the analysis (handling potential JSON string or raw text)
                let content = data.analysis;
                try {
                    const parsed = JSON.parse(content);
                    if (parsed.suggestions) {
                        content = `<strong>Overall Suggestion:</strong><br>${parsed.suggestions}<br><br>`;
                        for (const [ticker, info] of Object.entries(parsed.stocks)) {
                            content += `<strong>${ticker}:</strong> ${info.reason}<br><br>`;
                        }
                    }
                } catch (e) {
                    // Fallback to raw text if not JSON
                }

                analysisContent.innerHTML = content;
                analysisSection.style.display = 'block';
            } else {
                alert(`Error: ${data.detail || 'Failed to fetch analysis'}`);
            }
        } catch (error) {
            console.error(error);
            alert('Connection failed');
        } finally {
            loading.style.display = 'none';
            analyzeBtn.disabled = false;
        }
    });

    predictBtn.addEventListener('click', async () => {
        const tickers = tickerInput.value.split(',').map(t => t.trim().toUpperCase()).filter(t => t);
        
        // Reset UI
        predictionSection.style.display = 'none';
        loading.style.display = 'block';
        predictBtn.disabled = true;

        try {
            const response = await fetch('/rnn/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tickers })
            });

            const data = await response.json();
            
            if (response.ok) {
                predictionGrid.innerHTML = '';
                data.predictions.forEach(res => {
                    const card = document.createElement('div');
                    card.className = 'prediction-card';
                    card.innerHTML = `
                        <h3>${res.ticker}</h3>
                        <div class="price-box">$${res.predicted_price.toFixed(2)}</div>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">Next Predicted Close</p>
                        <div class="graph-container">
                            <img src="${res.graph_url}?t=${new Date().getTime()}" alt="${res.ticker} Forecast">
                        </div>
                    `;
                    predictionGrid.appendChild(card);
                });
                predictionSection.style.display = 'block';
                // Scroll to predictions
                predictionSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert(`Error: ${data.detail || 'Prediction failed'}`);
            }
        } catch (error) {
            console.error(error);
            alert('Prediction failed');
        } finally {
            loading.style.display = 'none';
            predictBtn.disabled = false;
        }
    });

    // Modal Logic
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    const captionText = document.getElementById('caption');
    const closeModal = document.querySelector('.close-modal');

    // Use event delegation on the prediction grid for clicks on images
    predictionGrid.addEventListener('click', (e) => {
        if (e.target.tagName === 'IMG') {
            modal.style.display = 'block';
            modalImg.src = e.target.src;
            captionText.innerHTML = e.target.alt;
        }
    });

    closeModal.onclick = () => {
        modal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});
