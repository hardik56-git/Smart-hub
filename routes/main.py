from flask import Blueprint, render_template
from models.product import Product
from database.db import init_db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Home page route."""
    # Initialize database if needed
    init_db()
    
    # Get featured products (top rated)
    featured_products = Product.get_featured(limit=6)
    return render_template('index.html', featured_products=featured_products)


@main.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@main.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html')