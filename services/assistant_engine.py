"""
AI Assistant Engine - Rule-based Keyword Parser
Smiling bot that responds to user queries with helpful information
"""

class AssistantEngine:
    """Rule-based assistant that parses user messages and provides relevant responses."""
    
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! 😊 How can I help you today?",
                "Hi there! 🌟 What can I assist you with?",
                "Hey! ✨ I'm here to help you find what you need!"
            ],
            'help': [
                "I can help you with:\n• Finding products\n• Checking prices\n• Budget optimization\n• Cart management\n• Product recommendations",
                "Need assistance? I can help you navigate our shop, find products, or optimize your budget! 😊"
            ],
            'budget': [
                "Use our Budget Optimizer to get the best products within your budget! Just go to the budget page and enter your spending limit.",
                "Want smart shopping? Try our budget optimizer to find the best products that fit your wallet! 💰"
            ],
            'cart': [
                "You can add products to your cart from any product page. View your cart anytime from the navigation menu.",
                "To manage your cart, simply click 'Add to Cart' on any product, then visit the cart page to review or remove items."
            ],
            'products': [
                "Browse our Products page to see all available items. You can filter by category or search for specific products.",
                "We have a wide variety of products! Check out the Products page to explore our collection."
            ],
            'categories': [
                "We have categories like Electronics, Clothing, Home & Kitchen, Books, Sports, and more!",
                "You can shop by category: Electronics, Clothing, Home, Books, Sports Equipment, and more!"
            ],
            'shipping': [
                "Standard shipping takes 5-7 business days. Express shipping is available for faster delivery!",
                "Free shipping on orders over $50! 🚚 Standard delivery within 5-7 days."
            ],
            'return': [
                "We offer a 30-day return policy for all products. Contact support for assistance.",
                "Not satisfied? We have a hassle-free 30-day return policy! 😊"
            ],
            'contact': [
                "You can reach us at support@shop.com or call 1-800-SHOP.",
                "Need more help? Email us at support@shop.com!"
            ],
            'thanks': [
                "You're welcome! 😊 Happy shopping!",
                "No problem! Let me know if you need anything else! 🌟",
                "Glad I could help! Feel free to ask more questions!"
            ],
            'bye': [
                "Goodbye! 👋 Come back soon!",
                "Take care! 😊 Shop with us again soon!",
                "Bye for now! See you next time! ✨"
            ],
            'default': [
                "I'm not sure about that, but I'm here to help! 😊 Try asking about products, budget, cart, or shipping!",
                "Hmm, I didn't catch that. Ask me about shopping, products, or how I can help! 🌟"
            ]
        }
        
        # Keyword mappings
        self.keywords = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
            'help': ['help', 'assist', 'support', 'what can you do', 'how can you help'],
            'budget': ['budget', 'price', 'cheap', 'affordable', 'money', 'cost', 'expensive', 'deal', 'discount', 'save'],
            'cart': ['cart', 'add to cart', 'remove', 'buy', 'purchase', 'order', 'checkout'],
            'products': ['product', 'items', 'shop', 'shopping', 'buy', 'purchase'],
            'categories': ['category', 'type', 'kind', 'electronics', 'clothing', 'home', 'books', 'sports'],
            'shipping': ['shipping', 'delivery', 'deliver', 'ship', 'arrival', 'time'],
            'return': ['return', 'refund', 'exchange', 'warranty', 'guarantee'],
            'contact': ['contact', 'email', 'phone', 'reach', 'support'],
            'thanks': ['thank', 'thanks', 'appreciate', 'grateful'],
            'bye': ['bye', 'goodbye', 'see you', 'later', 'farewell']
        }
    
    def process_message(self, user_message):
        """
        Process user message and return appropriate response.
        
        Args:
            user_message: String input from user
        
        Returns:
            String response from the assistant
        """
        if not user_message or not user_message.strip():
            return "Hi! 👋 How can I help you today?"
        
        # Normalize message
        message = user_message.lower().strip()
        
        # Check for keyword matches
        matched_category = self._match_keywords(message)
        
        # Get response from matched category or default
        responses = self.responses.get(matched_category, self.responses['default'])
        
        # Return first response in list (could be randomized)
        return responses[0]
    
    def _match_keywords(self, message):
        """Match message keywords to response categories."""
        scores = {}
        
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > 0:
                scores[category] = score
        
        if not scores:
            return 'default'
        
        # Return category with highest score
        return max(scores, key=scores.get)


# Singleton instance
assistant = AssistantEngine()


def get_response(user_message):
    """Quick access function to get assistant response."""
    return assistant.process_message(user_message)