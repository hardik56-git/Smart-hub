/**
 * AI Chat Widget - Smiling Bot
 * Rule-based AI logic for customer assistance
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize chat widget
    initChatWidget();
});

function initChatWidget() {
    const chatWidget = document.querySelector('.chat-widget');
    if (!chatWidget) return;
    
    const chatToggle = chatWidget.querySelector('.chat-toggle');
    const chatWindow = chatWidget.querySelector('.chat-window');
    const chatClose = chatWidget.querySelector('.chat-close');
    const chatInput = chatWidget.querySelector('.chat-input');
    const chatSendBtn = chatWidget.querySelector('.chat-send-btn');
    const chatMessages = chatWidget.querySelector('.chat-messages');
    
    // Toggle chat window
    chatToggle.addEventListener('click', () => {
        chatToggle.classList.toggle('active');
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            chatInput.focus();
        }
    });
    
    // Close chat
    chatClose.addEventListener('click', () => {
        chatToggle.classList.remove('active');
        chatWindow.classList.remove('active');
    });
    
    // Send message on button click
    chatSendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Quick question handlers
    const quickQuestions = chatWidget.querySelectorAll('.quick-question');
    quickQuestions.forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.textContent;
            addUserMessage(message);
            processMessage(message);
        });
    });
    
    // Show welcome message
    showWelcomeMessage();
}

function showWelcomeMessage() {
    const chatMessages = document.querySelector('.chat-messages');
    if (!chatMessages) return;
    
    const welcomeHTML = `
        <div class="welcome-message">
            <h4>👋 Hi there! I'm your shopping assistant</h4>
            <p>Ask me anything about products, cart, budget, or shipping!</p>
        </div>
    `;
    
    chatMessages.innerHTML = welcomeHTML;
    
    // Add initial bot message
    setTimeout(() => {
        addBotMessage("Hello! 😊 How can I help you today? Feel free to ask about our products, deals, or any questions you have!");
    }, 500);
}

function sendMessage() {
    const chatInput = document.querySelector('.chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    addUserMessage(message);
    chatInput.value = '';
    
    // Process the message
    processMessage(message);
}

function addUserMessage(message) {
    const chatMessages = document.querySelector('.chat-messages');
    const messageHTML = `
        <div class="message user">
            <div class="message-avatar">🧑</div>
            <div class="message-content">${escapeHtml(message)}</div>
        </div>
    `;
    
    chatMessages.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

function addBotMessage(message, showTyping = true) {
    const chatMessages = document.querySelector('.chat-messages');
    
    if (showTyping) {
        // Show typing indicator
        const typingHTML = `
            <div class="typing-indicator" id="typing-indicator">
                <div class="message-avatar">😊</div>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        chatMessages.insertAdjacentHTML('beforeend', typingHTML);
        scrollToBottom();
        
        // Simulate response delay (1-2 seconds)
        const delay = 1000 + Math.random() * 1000;
        
        setTimeout(() => {
            // Remove typing indicator
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            // Add bot message
            const botMessageHTML = `
                <div class="message bot">
                    <div class="message-avatar">😊</div>
                    <div class="message-content">${message}</div>
                </div>
            `;
            
            chatMessages.insertAdjacentHTML('beforeend', botMessageHTML);
            scrollToBottom();
        }, delay);
    } else {
        const botMessageHTML = `
            <div class="message bot">
                <div class="message-avatar">😊</div>
                <div class="message-content">${message}</div>
            </div>
        `;
        
        chatMessages.insertAdjacentHTML('beforeend', botMessageHTML);
        scrollToBottom();
    }
}

function processMessage(message) {
    const lowerMessage = message.toLowerCase();
    
    // Rule-based keyword matching
    let response = getAssistantResponse(lowerMessage);
    
    addBotMessage(response);
}

function getAssistantResponse(message) {
    // Keywords and their responses
    const responses = {
        greeting: [
            "Hello! 😊 How can I help you today?",
            "Hi there! 🌟 What can I assist you with?",
            "Hey! ✨ I'm here to help you find what you need!"
        ],
        help: [
            "I can help you with:\n\n• Finding products\n• Checking prices and deals\n• Budget optimization\n• Cart management\n• Product recommendations\n• Shipping information\n\nJust ask me anything! 😊",
            "Need assistance? I can help you navigate our shop, find products, optimize your budget, or answer any questions! 🌟"
        ],
        budget: [
            "Use our Budget Optimizer to get the best products within your budget! Just go to the budget page and enter your spending limit. Our smart algorithm will find the perfect items for you! 💰",
            "Want smart shopping? Try our budget optimizer at /budget to find the best products that fit your wallet! It uses advanced optimization to maximize value! 💡"
        ],
        cart: [
            "You can add products to your cart from any product page. Visit the cart to review items, update quantities, or remove items. Easy peasy! 🛒",
            "To manage your cart, simply click 'Add to Cart' on any product, then visit the cart page to review or remove items. Happy shopping! 😊"
        ],
        products: [
            "Browse our Products page to see all available items. You can filter by category or search for specific products. We have great deals! 🛍️",
            "We have a wide variety of products! Check out the Products page to explore our collection. From electronics to home goods, we've got you covered! ✨"
        ],
        categories: [
            "We have categories like:\n\n• Electronics & Gadgets\n• Clothing & Fashion\n• Home & Kitchen\n• Books & Media\n• Sports & Outdoors\n\nBrowse and find what you need! 🏷️",
            "You can shop by category: Electronics, Clothing, Home, Books, Sports Equipment, and more! Each category has amazing products waiting for you! 🌟"
        ],
        shipping: [
            "📦 Shipping Information:\n\n• Standard shipping: 5-7 business days\n• Express shipping: 2-3 business days\n• Free shipping on orders over $50!\n\nLet me know if you need more details!",
            "🚚 Delivery Options:\n\n• Standard: 5-7 days (Free over $50)\n• Express: 2-3 days (Extra fee)\n• Same-day delivery in select areas\n\nShop more, pay less! 😊"
        ],
        return: [
            "🔄 Return Policy:\n\n• 30-day return window\n• Items must be unused\n• Full refund or exchange\n\nWe want you happy! 😊",
            "Not satisfied? No worries! We have a hassle-free 30-day return policy. Just contact support and we'll help you out! 🌟"
        ],
        contact: [
            "📞 Contact Us:\n\n• Email: support@shop.com\n• Phone: 1-800-SHOP\n• We're here 24/7!\n\nHow can I help you? 😊",
            "Need more help? Reach us at support@shop.com or call 1-800-SHOP. We're always happy to assist! 🌟"
        ],
        thanks: [
            "You're welcome! 😊 Happy shopping!",
            "No problem! Let me know if you need anything else! 🌟",
            "Glad I could help! Feel free to ask more questions! ✨"
        ],
        bye: [
            "Goodbye! 👋 Come back soon!",
            "Take care! 😊 Shop with us again soon!",
            "Bye for now! See you next time! ✨"
        ],
        search: [
            "You can use the search bar at the top to find specific products. Try searching for items like 'laptop', 'phone', or 'shoes'! 🔍",
            "Looking for something specific? Use our search feature to find products by name, category, or price. Happy hunting! 🔎"
        ],
        price: [
            "Our prices are competitive and we often have deals! Check out our budget optimizer to find the best options within your budget. 💰",
            "Great question! Browse our products to see prices. You can also use our budget tool to optimize your spending! ✨"
        ],
        deal: [
            "We have amazing deals! Check our homepage for current promotions. Our budget optimizer can also help you find the best value! 🎉",
            "Always look out for deals! Subscribe to our newsletter for exclusive offers. The budget optimizer is great for finding deals too! 💫"
        ]
    };
    
    // Keywords mapping
    const keywords = {
        greeting: ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'start'],
        help: ['help', 'assist', 'support', 'what can you do', 'how can you help', ' Capabilities', 'options'],
        budget: ['budget', 'price', 'cheap', 'affordable', 'money', 'cost', 'expensive', 'deal', 'discount', 'save', 'save money', 'best price'],
        cart: ['cart', 'add to cart', 'remove', 'buy', 'purchase', 'order', 'checkout', 'shopping cart'],
        products: ['product', 'items', 'shop', 'shopping', 'buy', 'purchase', 'catalog'],
        categories: ['category', 'type', 'kind', 'electronics', 'clothing', 'home', 'books', 'sports', 'section'],
        shipping: ['shipping', 'delivery', 'deliver', 'ship', 'arrival', 'time', 'arrive', 'send'],
        return: ['return', 'refund', 'exchange', 'warranty', 'guarantee', 'money back'],
        contact: ['contact', 'email', 'phone', 'reach', 'support', 'talk to'],
        thanks: ['thank', 'thanks', 'appreciate', 'grateful', 'thank you', 'thx'],
        bye: ['bye', 'goodbye', 'see you', 'later', 'farewell', 'exit', 'close'],
        search: ['search', 'find', 'look for', 'looking'],
        price: ['price', 'cost', 'how much', 'expensive', 'cheap', 'price?'],
        deal: ['deal', 'offer', 'sale', 'promotion', 'discount', 'coupon']
    };
    
    // Score keywords
    const scores = {};
    
    for (const [category, categoryKeywords] of Object.entries(keywords)) {
        let score = 0;
        for (const keyword of categoryKeywords) {
            if (message.includes(keyword)) {
                score += keyword.length;
            }
        }
        if (score > 0) {
            scores[category] = score;
        }
    }
    
    // Find best match
    let bestMatch = 'default';
    let maxScore = 0;
    
    for (const [category, score] of Object.entries(scores)) {
        if (score > maxScore) {
            maxScore = score;
            bestMatch = category;
        }
    }
    
    // Get response
    const categoryResponses = responses[bestMatch] || responses['default'];
    const randomIndex = Math.floor(Math.random() * categoryResponses.length);
    
    return categoryResponses[randomIndex];
}

function scrollToBottom() {
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export for potential API integration
window.ChatAssistant = {
    sendMessage: sendMessage,
    addBotMessage: addBotMessage
};