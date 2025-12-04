// Configuration and state
let isProcessing = false;
let currentWebsiteUrl = 'https://example.com';

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const sendText = document.getElementById('sendText');
const loadingSpinner = document.getElementById('loadingSpinner');
const statusBar = document.getElementById('statusBar');
const statusText = document.getElementById('statusText');
const progressIndicator = document.getElementById('progressIndicator');
const progressText = document.getElementById('progressText');
const websiteUrlInput = document.getElementById('websiteUrl');

// Initialize the application
function init() {
    loadConfig();
    updateStatus('Ready to help! Set a website URL and ask me anything.');
    questionInput.focus();
}

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/config');
        const config = await response.json();
        currentWebsiteUrl = config.default_website_url || 'https://example.com';
        websiteUrlInput.value = currentWebsiteUrl;
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

// Configure website URL
async function configureWebsite() {
    const url = websiteUrlInput.value.trim();
    
    if (!url) {
        showError('Please enter a valid website URL');
        return;
    }

    try {
        const response = await fetch('/configure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                website_url: url
            })
        });

        if (response.ok) {
            const result = await response.json();
            currentWebsiteUrl = result.default_website_url;
            showSuccess(`Website configured: ${currentWebsiteUrl}`);
            updateStatus('Ready to answer questions about the configured website');
        } else {
            showError('Failed to configure website');
        }
    } catch (error) {
        console.error('Configuration error:', error);
        showError('Error configuring website');
    }
}

// Send message
async function sendMessage() {
    const question = questionInput.value.trim();
    
    if (!question || isProcessing) {
        return;
    }

    // Add user message to chat
    addMessage(question, 'user');
    questionInput.value = '';
    
    // Start processing
    startProcessing();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                website_url: currentWebsiteUrl
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            // Add bot response
            addMessage(result.answer, 'bot');
            
            // Update status with exploration info
            const explorationInfo = `Explored ${result.pages_visited} page(s)`;
            updateStatus(explorationInfo);
            
            // Show explored URLs if any
            if (result.urls_explored && result.urls_explored.length > 0) {
                const urlsList = result.urls_explored.map(url => `• ${url.title} (${url.url})`).join('\n');
                addMessage(`📋 Pages I explored:\n${urlsList}`, 'bot', true);
            }
        } else {
            addMessage(`❌ Error: ${result.detail}`, 'bot');
            updateStatus('Error occurred');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessage('❌ Sorry, I encountered an error while processing your question. Please try again.', 'bot');
        updateStatus('Error occurred');
    } finally {
        stopProcessing();
    }
}

// Add message to chat
function addMessage(content, type, isInfo = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (isInfo) {
        contentDiv.style.fontSize = '0.9em';
        contentDiv.style.opacity = '0.8';
        contentDiv.style.fontFamily = 'monospace';
        contentDiv.style.whiteSpace = 'pre-line';
        // For info messages, use plain text
        contentDiv.textContent = content;
    } else if (type === 'bot') {
        // For bot messages, render markdown as HTML
        try {
            contentDiv.innerHTML = marked.parse(content);
        } catch (error) {
            console.error('Markdown parsing error:', error);
            contentDiv.textContent = content; // Fallback to plain text
        }
    } else {
        // For user messages, use plain text
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Start processing state
function startProcessing() {
    isProcessing = true;
    sendBtn.disabled = true;
    sendText.style.display = 'none';
    loadingSpinner.classList.remove('hidden');
    questionInput.disabled = true;
    
    updateStatus('Processing your question...');
    showProgress('Analyzing question and starting website exploration...');
}

// Stop processing state
function stopProcessing() {
    isProcessing = false;
    sendBtn.disabled = false;
    sendText.style.display = 'block';
    loadingSpinner.classList.add('hidden');
    questionInput.disabled = false;
    questionInput.focus();
    
    hideProgress();
}

// Update status
function updateStatus(message) {
    statusText.textContent = message;
}

// Show progress indicator
function showProgress(message) {
    progressText.textContent = message;
    progressIndicator.classList.remove('progress-hidden');
    progressIndicator.classList.add('progress-visible');
}

// Hide progress indicator
function hideProgress() {
    progressIndicator.classList.remove('progress-visible');
    progressIndicator.classList.add('progress-hidden');
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.config-panel');
    container.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    const container = document.querySelector('.config-panel');
    container.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !isProcessing) {
        sendMessage();
    }
}

// Example questions for demonstration
const exampleQuestions = [
    "What are your return policies?",
    "How do I contact customer support?", 
    "What payment methods do you accept?",
    "Do you offer international shipping?",
    "What are your business hours?"
];

// Add example question functionality
function addExampleQuestions() {
    const examplesDiv = document.createElement('div');
    examplesDiv.className = 'example-questions';
    examplesDiv.innerHTML = `
        <h4>Try asking:</h4>
        ${exampleQuestions.map(q => 
            `<button class="example-btn" onclick="askExample('${q}')">${q}</button>`
        ).join('')}
    `;
    
    chatMessages.appendChild(examplesDiv);
}

// Ask example question
function askExample(question) {
    questionInput.value = question;
    sendMessage();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);