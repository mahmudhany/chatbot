document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        addMessage(message, 'user');
        userInput.value = '';
        
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = 'none';
            
            if (data.status === 'success') {
                addMessage(data.answer, 'bot');
            } else {
                addMessage('حدث خطأ أثناء معالجة سؤالك. يرجى المحاولة مرة أخرى.', 'bot');
            }
        })
        .catch(error => {
            typingIndicator.style.display = 'none';
            addMessage('حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.', 'bot');
            console.error('Error:', error);
        });
    }
    
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'user') {
            messageDiv.innerHTML = `<p>${content}</p>`;
        } else {
            messageDiv.innerHTML = content;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});