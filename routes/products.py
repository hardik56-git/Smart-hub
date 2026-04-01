from flask import Blueprint, render_template, request, jsonify, abort
from models.product import Product

products = Blueprint('products', __name__)


@products.route('/products')
def product_list():
    """Product listing page with search and filter."""
    search_query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    all_products = Product.get_all(search_query=search_query if search_query else None, 
                                    category=category if category else None)
    
    # Get all categories for filter
    categories = Product.get_categories()
    
    return render_template('products.html', 
                         products=all_products, 
                         categories=categories,
                         search_query=search_query,
                         selected_category=category)


@products.route('/product/<int:product_id>')
def product_detail(product_id):
    """Single product detail page."""
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)


@products.route('/api/products')
def api_products():
    """API endpoint for products JSON."""
    search_query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    products_list = Product.get_all(search_query=search_query if search_query else None,
                                     category=category if category else None)
    return jsonify(products_list)


@products.route('/api/product/<int:product_id>')
def api_product(product_id):
    """API endpoint for single product JSON."""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)