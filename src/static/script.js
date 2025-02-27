document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Process message content
        if (isUser) {
            messageContent.textContent = message;
        } else {
            // Process bot message with formatting
            const formattedMessage = formatBotMessage(message);
            messageContent.innerHTML = formattedMessage;
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to format bot messages with HTML
    function formatBotMessage(message) {
        // Convert URLs to links
        message = message.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank">$1</a>'
        );
        
        // Convert newlines to <br>
        message = message.replace(/\n/g, '<br>');
        
        // Format numbered lists
        message = message.replace(
            /(\d+\.\s+[^\n]+)(?:\n|$)/g,
            '<li>$1</li>'
        );
        
        if (message.includes('<li>')) {
            message = '<ol>' + message + '</ol>';
            // Clean up any extra <ol> tags that might have been added
            message = message.replace(/<\/ol>\s*<ol>/g, '');
        }
        
        return message;
    }
    
    // Function to add a loading indicator
    function addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading-indicator';
        loadingDiv.innerHTML = `
            <div class="message-content">
                <div class="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return loadingDiv;
    }
    
    // Function to send a message to the API
    async function sendMessage(message) {
        try {
            // Add loading indicator
            const loadingIndicator = addLoadingIndicator();
            
            // Send request to API
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: message }),
            });
            
            // Remove loading indicator
            loadingIndicator.remove();
            
            if (!response.ok) {
                throw new Error('API request failed');
            }
            
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error:', error);
            return 'Sorry, I encountered an error while processing your question. Please try again.';
        }
    }
    
    // Function to handle user input
    async function handleUserInput() {
        const message = userInput.value.trim();
        
        if (message) {
            // Clear input
            userInput.value = '';
            
            // Add user message to chat
            addMessage(message, true);
            
            // Get response from API
            const response = await sendMessage(message);
            
            // Add bot response to chat
            addMessage(response);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', handleUserInput);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });
    
    // Focus input on page load
    userInput.focus();
}); 