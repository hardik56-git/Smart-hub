from flask import Flask, jsonify, request
from config import Config
from database.db import init_db
from routes import main, products, cart, budget, auth


def create_app(config_class=Config):
    """Application factory pattern for Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(budget)
    app.register_blueprint(auth)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    # API endpoint for assistant
    @app.route('/api/assistant', methods=['POST'])
    def assistant():
        from services.assistant_engine import get_response
        data = request.get_json()
        message = data.get('message', '')
        response = get_response(message)
        return jsonify({'response': response})
    
    return app


# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)