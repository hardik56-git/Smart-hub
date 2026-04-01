"""
Seed Data - Sample Products for Database
Run this script to populate the database with sample products
"""

import requests
from database.db import get_db_connection, init_db


def seed_products():
    """Seed the database with sample products."""
    # Initialize database first
    init_db()
    
    # Hardcoded image URLs from fakestoreapi.com
    image_urls = [
        "https://fakestoreapi.com/img/81fPPd8cutL._AC_UY879_.jpg",  # backpack
        "https://fakestoreapi.com/img/81tTSuB5NL._AC_SL1500_.jpg",  # jacket
        "https://fakestoreapi.com/img/61sbMiUnoS._AC_SL1500_.jpg",  # shirt
        "https://fakestoreapi.com/img/51Hor6Z3dL._AC_SL1000_.jpg",  # gold chain
        "https://fakestoreapi.com/img/41CRg1jKvpL._AC_SL1000_.jpg",  # ring
        "https://fakestoreapi.com/img/51H4Ww1ZRpL._AC_SL1000_.jpg",  # bracelet
        "https://fakestoreapi.com/img/61HBxnnUAbL._AC_SL1500_.jpg",  # fan
        "https://fakestoreapi.com/img/51Q2WnTjKL._AC_SL1500_.jpg",  # shirts
        "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg",  # boots
        "https://fakestoreapi.com/img/81hT3F6B8L._AC_SL1500_.jpg",  # shirt
        "https://fakestoreapi.com/img/61gd05N6kKL._AC_SL1500_.jpg",  # jacket
        "https://fakestoreapi.com/img/51b9t-6l0L._AC_SL1500_.jpg",  # jeans
        "https://fakestoreapi.com/img/611yclcoOlL._AC_SL1500_.jpg",  # dress
        "https://fakestoreapi.com/img/71kVx5xk6TL._AC_SL1500_.jpg",  # shoes
        "https://fakestoreapi.com/img/61Y4E+WmKaL._AC_SL1500_.jpg",  # leggings
        "https://fakestoreapi.com/img/61nN5+9FJZL._AC_SL1500_.jpg",  # ring
        "https://fakestoreapi.com/img/71G+N0JgAbL._AC_SL1500_.jpg",  # electronics
        "https://fakestoreapi.com/img/71yxfy2Xx8L._AC_SL1500_.jpg",  # watch
        "https://fakestoreapi.com/img/61p4+V+QBQL._AC_SL1000_.jpg",  # jewelry
        "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg",  # misc
    ]
    
    products_data = [
        # Electronics
        {"name": "Wireless Bluetooth Headphones", "description": "High-quality wireless headphones with noise cancellation and 20-hour battery life.", "price": 79.99, "category": "Electronics", "rating": 4.5, "reviews": 234, "image_url": "https://fakestoreapi.com/img/81fPPd8cutL._AC_UY879_.jpg"},
        {"name": "Smartphone 6.5\" Display", "description": "Latest smartphone with 128GB storage, dual camera, and fast charging.", "price": 699.99, "category": "Electronics", "rating": 4.7, "reviews": 156, "image_url": "https://fakestoreapi.com/img/81tTSuB5NL._AC_SL1500_.jpg"},
        {"name": "Laptop 15.6\" Full HD", "description": "Powerful laptop with 16GB RAM, 512GB SSD, and Intel Core i7 processor.", "price": 1199.99, "category": "Electronics", "rating": 4.6, "reviews": 89, "image_url": "https://fakestoreapi.com/img/61sbMiUnoS._AC_SL1500_.jpg"},
        {"name": "4K Ultra HD Smart TV 55\"", "description": "Stunning 4K TV with smart features, HDR support, and built-in streaming apps.", "price": 549.99, "category": "Electronics", "rating": 4.8, "reviews": 312, "image_url": "https://fakestoreapi.com/img/51Hor6Z3dL._AC_SL1000_.jpg"},
        {"name": "Wireless Gaming Mouse", "description": "Professional gaming mouse with programmable buttons and RGB lighting.", "price": 49.99, "category": "Electronics", "rating": 4.3, "reviews": 178, "image_url": "https://fakestoreapi.com/img/41CRg1jKvpL._AC_SL1000_.jpg"},
        {"name": "Portable Bluetooth Speaker", "description": "Waterproof speaker with 12-hour battery life and premium sound quality.", "price": 89.99, "category": "Electronics", "rating": 4.4, "reviews": 267, "image_url": "https://fakestoreapi.com/img/51H4Ww1ZRpL._AC_SL1000_.jpg"},
        {"name": "Smart Watch Fitness Tracker", "description": "Track your health and fitness with heart rate monitor, GPS, and sleep tracking.", "price": 199.99, "category": "Electronics", "rating": 4.2, "reviews": 145, "image_url": "https://fakestoreapi.com/img/71yxfy2Xx8L._AC_SL1500_.jpg"},
        {"name": "Tablet 10.1\" Display", "description": "Versatile tablet perfect for work and entertainment with 64GB storage.", "price": 299.99, "category": "Electronics", "rating": 4.5, "reviews": 98, "image_url": "https://fakestoreapi.com/img/61p4+V+QBQL._AC_SL1000_.jpg"},
        
        # Clothing
        {"name": "Classic Cotton T-Shirt Pack", "description": "Pack of 3 premium cotton t-shirts in assorted colors. Comfortable and durable.", "price": 29.99, "category": "Clothing", "rating": 4.4, "reviews": 456, "image_url": "https://fakestoreapi.com/img/61Y4E+WmKaL._AC_SL1500_.jpg"},
        {"name": "Men's Slim Fit Jeans", "description": "Stylish slim fit jeans made from premium denim. Perfect for any occasion.", "price": 49.99, "category": "Clothing", "rating": 4.3, "reviews": 234, "image_url": "https://fakestoreapi.com/img/51b9t-6l0L._AC_SL1500_.jpg"},
        {"name": "Winter Jacket Waterproof", "description": "Warm and stylish winter jacket with waterproof exterior and cozy lining.", "price": 129.99, "category": "Clothing", "rating": 4.6, "reviews": 167, "image_url": "https://fakestoreapi.com/img/61gd05N6kKL._AC_SL1500_.jpg"},
        {"name": "Running Shoes Performance", "description": "Lightweight running shoes with superior cushioning and breathable mesh.", "price": 119.99, "category": "Clothing", "rating": 4.7, "reviews": 345, "image_url": "https://fakestoreapi.com/img/71G+N0JgAbL._AC_SL1500_.jpg"},
        {"name": "Casual Summer Dress", "description": "Elegant summer dress perfect for casual outings and beach days.", "price": 39.99, "category": "Clothing", "rating": 4.5, "reviews": 189, "image_url": "https://fakestoreapi.com/img/611yclcoOlL._AC_SL1500_.jpg"},
        {"name": "Wool Blend Sweater", "description": "Cozy wool blend sweater perfect for the colder months. Machine washable.", "price": 59.99, "category": "Clothing", "rating": 4.4, "reviews": 112, "image_url": "https://fakestoreapi.com/img/81hT3F6B8L._AC_SL1500_.jpg"},
        {"name": "Athletic Leggings Workout", "description": "High-waisted workout leggings with stretch fabric and pocket detail.", "price": 34.99, "category": "Clothing", "rating": 4.6, "reviews": 278, "image_url": "https://fakestoreapi.com/img/71kVx5xk6TL._AC_SL1500_.jpg"},
        {"name": "Leather Belt Premium", "description": "Genuine leather belt with classic buckle. Perfect for formal or casual.", "price": 24.99, "category": "Clothing", "rating": 4.2, "reviews": 89, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        
        # Home & Kitchen
        {"name": "Stainless Steel Cookware Set", "description": "10-piece cookware set with pots, pans, and lids. Induction compatible.", "price": 189.99, "category": "Home", "rating": 4.7, "reviews": 234, "image_url": "https://fakestoreapi.com/img/81fPPd8cutL._AC_UY879_.jpg"},
        {"name": "Coffee Maker Programmable", "description": "12-cup programmable coffee maker with auto shut-off and thermal carafe.", "price": 79.99, "category": "Home", "rating": 4.5, "reviews": 345, "image_url": "https://fakestoreapi.com/img/81tTSuB5NL._AC_SL1500_.jpg"},
        {"name": "Stand Mixer 5-Quart", "description": "Professional stand mixer with multiple attachments for baking and cooking.", "price": 299.99, "category": "Home", "rating": 4.8, "reviews": 156, "image_url": "https://fakestoreapi.com/img/61sbMiUnoS._AC_SL1500_.jpg"},
        {"name": "Air Purifier HEPA Filter", "description": "Cleans air in large rooms with True HEPA filter and smart sensors.", "price": 149.99, "category": "Home", "rating": 4.4, "reviews": 189, "image_url": "https://fakestoreapi.com/img/51Hor6Z3dL._AC_SL1000_.jpg"},
        {"name": "Robot Vacuum Cleaner", "description": "Smart robot vacuum with mapping technology and app control.", "price": 349.99, "category": "Home", "rating": 4.6, "reviews": 267, "image_url": "https://fakestoreapi.com/img/41CRg1jKvpL._AC_SL1000_.jpg"},
        {"name": "Memory Foam Pillow Set", "description": "Set of 2 memory foam pillows with cooling gel technology.", "price": 59.99, "category": "Home", "rating": 4.3, "reviews": 312, "image_url": "https://fakestoreapi.com/img/51H4Ww1ZRpL._AC_SL1000_.jpg"},
        {"name": "Blender High Speed", "description": "Professional-grade blender with 1400W motor for smoothies and more.", "price": 129.99, "category": "Home", "rating": 4.5, "reviews": 198, "image_url": "https://fakestoreapi.com/img/61HBxnnUAbL._AC_SL1500_.jpg"},
        {"name": "Knife Set Professional", "description": "15-piece knife set with wooden block and sharpening tool.", "price": 99.99, "category": "Home", "rating": 4.7, "reviews": 234, "image_url": "https://fakestoreapi.com/img/51Q2WnTjKL._AC_SL1500_.jpg"},
        
        # Books
        {"name": "The Great Gatsby", "description": "Classic novel by F. Scott Fitzgerald. A timeless American masterpiece.", "price": 12.99, "category": "Books", "rating": 4.8, "reviews": 1234, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "To Kill a Mockingbird", "description": "Harper Lee's Pulitzer Prize-winning novel about justice and racism.", "price": 14.99, "category": "Books", "rating": 4.9, "reviews": 1567, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "1984 George Orwell", "description": "Dystopian novel about totalitarianism and surveillance.", "price": 11.99, "category": "Books", "rating": 4.7, "reviews": 987, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Pride and Prejudice", "description": "Jane Austen's beloved romantic novel of manners.", "price": 10.99, "category": "Books", "rating": 4.6, "reviews": 876, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "The Catcher in the Rye", "description": "J.D. Salinger's coming-of-age classic.", "price": 9.99, "category": "Books", "rating": 4.4, "reviews": 654, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Steve Jobs Biography", "description": "Walter Isaacson's definitive biography of the Apple founder.", "price": 18.99, "category": "Books", "rating": 4.7, "reviews": 432, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Atomic Habits", "description": "James Clear's guide to building good habits and breaking bad ones.", "price": 16.99, "category": "Books", "rating": 4.8, "reviews": 789, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "The Psychology of Money", "description": "Timeless lessons on wealth and investing by Morgan Housel.", "price": 19.99, "category": "Books", "rating": 4.6, "reviews": 567, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        
        # Sports
        {"name": "Yoga Mat Premium", "description": "Extra thick yoga mat with non-slip surface and carrying strap.", "price": 39.99, "category": "Sports", "rating": 4.5, "reviews": 345, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Adjustable Dumbbells Set", "description": "Space-saving adjustable dumbbells from 5 to 25 lbs each.", "price": 249.99, "category": "Sports", "rating": 4.7, "reviews": 178, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Tennis Racket Pro", "description": "Professional tennis racket with graphite frame and strings.", "price": 89.99, "category": "Sports", "rating": 4.4, "reviews": 123, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Soccer Ball Match Grade", "description": "Official size and weight soccer ball with premium construction.", "price": 29.99, "category": "Sports", "rating": 4.6, "reviews": 234, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Basketball Indoor/Outdoor", "description": "Official size basketball with superior grip and durability.", "price": 24.99, "category": "Sports", "rating": 4.3, "reviews": 189, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Cycling Helmet Safety", "description": "Lightweight helmet with adjustable fit and ventilation.", "price": 49.99, "category": "Sports", "rating": 4.5, "reviews": 156, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Resistance Bands Set", "description": "Set of 5 resistance bands with different tension levels.", "price": 19.99, "category": "Sports", "rating": 4.4, "reviews": 267, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
        {"name": "Running Hydration Belt", "description": "Lightweight hydration belt with two bottle bottles.", "price": 29.99, "category": "Sports", "rating": 4.2, "reviews": 98, "image_url": "https://fakestoreapi.com/img/81XH0R6kSnL._AC_SL1500_.jpg"},
    ]
    
    conn = get_db_connection()
    
    # Check if products already exist
    existing = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()
    if existing['count'] > 0:
        print(f"Database already has {existing['count']} products. Skipping seed.")
        conn.close()
        return
    
    # Add new products
    for product_data in products_data:
        conn.execute('''
            INSERT INTO products (name, description, price, category, image_url, rating, reviews)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product_data['name'], product_data['description'], product_data['price'], 
              product_data['category'], product_data['image_url'], product_data['rating'], product_data['reviews']))
    
    conn.commit()
    conn.close()
    print(f"Seeded {len(products_data)} products successfully!")


if __name__ == '__main__':
    seed_products()