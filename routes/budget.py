from flask import Blueprint, render_template, request, jsonify
from models.product import Product
from services.budget_optimizer import get_budget_recommendations
from database.db import init_db

budget = Blueprint('budget', __name__)


@budget.route('/budget')
def budget_page():
    """Budget optimizer page."""
    # Initialize database
    init_db()
    
    # Get all categories for filtering
    categories = Product.get_categories()
    
    return render_template('budget.html', categories=categories)


@budget.route('/budget/optimize', methods=['POST'])
def optimize_budget():
    """API endpoint for budget optimization."""
    data = request.get_json()
    budget_amount = float(data.get('budget', 0))
    selected_categories = data.get('categories', [])
    
    # Get all products within budget
    all_products = Product.get_all()
    all_products = [p for p in all_products if p['price'] <= budget_amount]
    
    if not all_products:
        return jsonify({
            'error': 'No products available within this budget',
            'selected_products': [],
            'total_cost': 0
        })
    
    # Get recommendations
    result = get_budget_recommendations(
        all_products, 
        budget_amount, 
        selected_categories if selected_categories else None
    )
    
    return jsonify(result)


@budget.route('/budget_result')
def budget_result():
    """Budget result page (for form redirect)."""
    budget = request.args.get('budget', type=float, default=0)
    return render_template('budget_result.html', budget=budget)