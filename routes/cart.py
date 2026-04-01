from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from models.product import Product, CartItem
from database.db import init_db
import uuid

cart = Blueprint('cart', __name__)


@cart.route('/cart')
def view_cart():
    """Cart page showing all items."""
    cart_key = session.get('cart_key', 'default')
    cart_items = CartItem.get_by_session(cart_key)
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@cart.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart."""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Get or create cart key
    cart_key = session.get('cart_key')
    if not cart_key:
        cart_key = str(uuid.uuid4())
        session['cart_key'] = cart_key
    
    # Add to cart
    CartItem.add(cart_key, product_id, quantity=1)
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Added to cart!'})
    
    return redirect(url_for('products.product_detail', product_id=product_id))


@cart.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """Remove item from cart."""
    CartItem.remove(item_id)
    return redirect(url_for('cart.view_cart'))


@cart.route('/cart/update/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    """Update cart item quantity."""
    quantity = request.form.get('quantity', type=int)
    
    if quantity and quantity > 0:
        CartItem.update_quantity(item_id, quantity)
    else:
        CartItem.remove(item_id)
    
    return redirect(url_for('cart.view_cart'))


@cart.route('/api/cart')
def api_cart():
    """API endpoint for cart items."""
    cart_key = session.get('cart_key', 'default')
    cart_items = CartItem.get_by_session(cart_key)
    
    return jsonify(cart_items)


@cart.route('/api/cart/add/<int:product_id>', methods=['POST'])
def api_add_to_cart(product_id):
    """API endpoint to add product to cart."""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    cart_key = session.get('cart_key')
    if not cart_key:
        cart_key = str(uuid.uuid4())
        session['cart_key'] = cart_key
    
    CartItem.add(cart_key, product_id, quantity=1)
    
    return jsonify({'success': True, 'product_id': product_id})


@cart.route('/api/cart/remove/<int:item_id>', methods=['POST'])
def api_remove_from_cart(item_id):
    """API endpoint to remove item from cart."""
    CartItem.remove(item_id)
    return jsonify({'success': True})


# Add render_template import
from flask import render_template