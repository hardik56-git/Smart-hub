import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    CART_SESSION_KEY = 'cart'
    MAX_BUDGET_ITEMS = 50