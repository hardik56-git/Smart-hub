/**
 * Cart - Add/Remove Cart Items
 * Handles cart operations via AJAX
 */

document.addEventListener('DOMContentLoaded', function() {
    initCart();
});

function initCart() {
    // Add to cart buttons
    initAddToCart();
    
    // Cart quantity controls
    initQuantityControls();
    
    // Remove from cart
    initRemoveButtons();
}

function initAddToCart() {
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn, .btn-add-to-cart');
    
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId || this.getAttribute('data-product-id');
            
            if (productId) {
                addToCart(productId, this);
            }
        });
    });
}

function addToCart(productId, buttonElement) {
    // Show loading state
    const originalText = buttonElement.textContent;
    buttonElement.textContent = 'Adding...';
    buttonElement.disabled = true;
    
    fetch(`/cart/add/${productId}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count in navbar
            updateCartCount();
            
            // Show success message
            showNotification('Product added to cart! 🛒', 'success');
            
            // Change button text temporarily
            buttonElement.textContent = 'Added! ✓';
            setTimeout(() => {
                buttonElement.textContent = originalText;
                buttonElement.disabled = false;
            }, 2000);
        } else {
            showNotification('Failed to add product', 'error');
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        showNotification('An error occurred', 'error');
        buttonElement.textContent = originalText;
        buttonElement.disabled = false;
    });
}

function initQuantityControls() {
    // Decrease quantity
    document.querySelectorAll('.quantity-decrease').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const input = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
            let quantity = parseInt(input.value);
            
            if (quantity > 1) {
                updateCartQuantity(itemId, quantity - 1);
            }
        });
    });
    
    // Increase quantity
    document.querySelectorAll('.quantity-increase').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const input = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
            let quantity = parseInt(input.value);
            
            updateCartQuantity(itemId, quantity + 1);
        });
    });
    
    // Manual quantity input
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            let quantity = parseInt(this.value);
            
            if (quantity < 1) quantity = 1;
            
            updateCartQuantity(itemId, quantity);
        });
    });
}

function updateCartQuantity(itemId, quantity) {
    fetch(`/cart/update/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `quantity=${quantity}`,
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.redirected) {
            window.location.reload();
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.success) {
            // Update UI without reload if possible
            updateCartUI(data);
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
        // Fallback to page reload
        window.location.reload();
    });
}

function updateCartUI(data) {
    // Update totals
    if (data.total) {
        document.querySelectorAll('.cart-total').forEach(el => {
            el.textContent = `$${data.total.toFixed(2)}`;
        });
    }
}

function initRemoveButtons() {
    document.querySelectorAll('.remove-from-cart, .btn-remove-item').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!confirm('Remove this item from cart?')) {
                return;
            }
            
            const itemId = this.dataset.itemId || this.getAttribute('data-item-id');
            
            removeFromCart(itemId);
        });
    });
}

function removeFromCart(itemId) {
    fetch(`/cart/remove/${itemId}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.redirected) {
            window.location.reload();
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.success) {
            showNotification('Item removed from cart', 'info');
            
            // Reload page to update cart
            setTimeout(() => {
                window.location.reload();
            }, 500);
        }
    })
    .catch(error => {
        console.error('Error removing item:', error);
        window.location.reload();
    });
}

function updateCartCount() {
    fetch('/api/cart')
    .then(response => response.json())
    .then(cart => {
        const cartCountElements = document.querySelectorAll('.cart-count');
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        
        cartCountElements.forEach(el => {
            el.textContent = totalItems;
            el.style.display = totalItems > 0 ? 'block' : 'none';
        });
    })
    .catch(error => {
        console.error('Error fetching cart count:', error);
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${getNotificationIcon(type)}</span>
        <span class="notification-message">${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Hide and remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        info: 'ℹ',
        warning: '⚠'
    };
    return icons[type] || 'ℹ';
}

// Add notification styles dynamically
const notificationStyles = `
    .notification {
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 15px 20px;
        background: var(--white);
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid var(--success);
    }
    
    .notification-error {
        border-left: 4px solid var(--error);
    }
    
    .notification-info {
        border-left: 4px solid #2196F3;
    }
    
    .notification-icon {
        font-size: 18px;
    }
    
    .notification-success .notification-icon {
        color: var(--success);
    }
    
    .notification-error .notification-icon {
        color: var(--error);
    }
`;

// Add styles to head
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Export for use
window.CartManager = {
    addToCart,
    removeFromCart,
    updateCartQuantity,
    updateCartCount
};