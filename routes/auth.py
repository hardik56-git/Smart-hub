from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.product import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        
        if user and User.check_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        existing = User.get_by_username(username)
        if existing:
            flash('Username already exists', 'error')
            return render_template('signup.html')
        
        # Create new user (simple hash for demo)
        user_id = User.create(username, email, password)
        
        if user_id:
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Error creating account', 'error')
    
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    """Logout route."""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.index'))


@auth.route('/profile')
def profile():
    """User profile page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(session['user_id'])
    return render_template('profile.html', user=user)