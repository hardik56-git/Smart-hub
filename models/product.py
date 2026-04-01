import sqlite3
import os
from database.db import get_db_connection

class Product:
    """Product model using SQLite."""
    
    @staticmethod
    def get_all(search_query=None, category=None):
        """Get all products with optional filtering."""
        conn = get_db_connection()
        query = 'SELECT * FROM products WHERE 1=1'
        params = []
        
        if search_query:
            query += ' AND name LIKE ?'
            params.append(f'%{search_query}%')
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        products = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(row) for row in products]
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID."""
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return dict(product) if product else None
    
    @staticmethod
    def get_featured(limit=6):
        """Get featured products (highest rated)."""
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products ORDER BY rating DESC LIMIT ?', (limit,)).fetchall()
        conn.close()
        return [dict(row) for row in products]
    
    @staticmethod
    def get_categories():
        """Get all unique categories."""
        conn = get_db_connection()
        categories = conn.execute('SELECT DISTINCT category FROM products WHERE category IS NOT NULL').fetchall()
        conn.close()
        return [row['category'] for row in categories]
    
    @staticmethod
    def create(name, description, price, category, image_url=None, rating=0.0, reviews=0):
        """Create a new product."""
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO products (name, description, price, category, image_url, rating, reviews) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, description, price, category, image_url, rating, reviews)
        )
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return product_id
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'rating': self.rating,
            'reviews': self.reviews
        }


class User:
    """User model using SQLite."""
    
    @staticmethod
    def get_by_username(username):
        """Get user by username."""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def create(username, email, password_hash):
        """Create a new user."""
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def check_password(stored_hash, password):
        """Check password (simple comparison for demo)."""
        return stored_hash == password


class CartItem:
    """Cart item model using SQLite."""
    
    @staticmethod
    def get_by_session(session_key):
        """Get cart items by session key."""
        conn = get_db_connection()
        items = conn.execute('''
            SELECT cart_items.*, products.name, products.price, products.image_url, products.category
            FROM cart_items 
            JOIN products ON cart_items.product_id = products.id
            WHERE cart_items.session_key = ?
        ''', (session_key,)).fetchall()
        conn.close()
        return [dict(row) for row in items]
    
    @staticmethod
    def add(session_key, product_id, quantity=1):
        """Add item to cart."""
        conn = get_db_connection()
        
        # Check if item already exists
        existing = conn.execute(
            'SELECT * FROM cart_items WHERE session_key = ? AND product_id = ?',
            (session_key, product_id)
        ).fetchone()
        
        if existing:
            conn.execute(
                'UPDATE cart_items SET quantity = quantity + ? WHERE id = ?',
                (quantity, existing['id'])
            )
        else:
            conn.execute(
                'INSERT INTO cart_items (session_key, product_id, quantity) VALUES (?, ?, ?)',
                (session_key, product_id, quantity)
            )
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_quantity(item_id, quantity):
        """Update cart item quantity."""
        conn = get_db_connection()
        if quantity > 0:
            conn.execute('UPDATE cart_items SET quantity = ? WHERE id = ?', (quantity, item_id))
        else:
            conn.execute('DELETE FROM cart_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def remove(item_id):
        """Remove item from cart."""
        conn = get_db_connection()
        conn.execute('DELETE FROM cart_items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()