
document.body.addEventListener('htmx:afterRequest', function(event){
    if (event.detail.successful) {
        try {
            const response = JSON.parse(event.detail.xhr.responseText);
            const shortCode = response.shortCode;
            
            if (shortCode) {
                const baseUrl = 'http://localhost:8000/shorten/';
                const shortUrl = baseUrl + shortCode;
                
                const resultHolder = document.getElementById('result-holder');
                resultHolder.innerHTML = `
                    <div class="result-box">
                        <h2>[ SUCCESS ]</h2>
                        
                        <div class="result-item">
                            <div class="result-label">SHORT_URL:</div>
                            <div class="result-value">
                                <a href="${shortUrl}" target="_blank">${shortUrl}</a>
                            </div>
                            <button class="copy-btn" onclick="copyToClipboard('${shortUrl}')">
                                [ COPY ]
                            </button>
                        </div>
                        
                        <div class="result-item">
                            <div class="result-label">ORIGINAL_URL:</div>
                            <div class="result-value">${response.url}</div>
                        </div>
                        
                        <div class="result-item">
                            <div class="result-label">CREATED_AT:</div>
                            <div class="result-value">${response.createdAt}</div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error parsing response:', error);
            document.getElementById('result-holder').innerHTML = `
                <div class="result-box">
                    <h2>[ ERROR ]</h2>
                    <div class="result-item">
                        <div class="result-value" style="color: #ff4444;">
                            SYSTEM_ERROR: Failed to process response
                        </div>
                    </div>
                </div>
            `;
        }
    } else {
        document.getElementById('result-holder').innerHTML = `
            <div class="result-box">
                <h2>[ ERROR ]</h2>
                <div class="result-item">
                    <div class="result-value" style="color: #ff4444;">
                        CONNECTION_ERROR: Request failed
                    </div>
                </div>
            </div>
        `;
    }
});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('✓ COPIED TO CLIPBOARD');
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}
