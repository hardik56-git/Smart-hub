/**
 * Budget - Budget Input & Result UI
 * Handles budget optimization form and results display
 */

document.addEventListener('DOMContentLoaded', function() {
    initBudgetOptimizer();
});

function initBudgetOptimizer() {
    // Budget form
    initBudgetForm();
    
    // Category selection
    initCategorySelection();
    
    // Results display
    initResultsDisplay();
}

function initBudgetForm() {
    const budgetForm = document.querySelector('#budget-form');
    
    if (budgetForm) {
        budgetForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitBudgetRequest();
        });
    }
}

function initCategorySelection() {
    const categoryCheckboxes = document.querySelectorAll('.category-checkbox');
    
    categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedCategories();
        });
    });
    
    // Select all / Clear all
    const selectAllBtn = document.querySelector('.select-all-categories');
    const clearAllBtn = document.querySelector('.clear-all-categories');
    
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            categoryCheckboxes.forEach(cb => cb.checked = true);
            updateSelectedCategories();
        });
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            categoryCheckboxes.forEach(cb => cb.checked = false);
            updateSelectedCategories();
        });
    }
}

function updateSelectedCategories() {
    const selected = [];
    document.querySelectorAll('.category-checkbox:checked').forEach(cb => {
        selected.push(cb.value);
    });
    
    const countEl = document.querySelector('.selected-count');
    if (countEl) {
        countEl.textContent = `${selected.length} selected`;
    }
}

function submitBudgetRequest() {
    const budgetInput = document.querySelector('#budget-amount');
    const budget = parseFloat(budgetInput.value);
    
    if (!budget || budget <= 0) {
        showBudgetError('Please enter a valid budget amount');
        return;
    }
    
    // Get selected categories
    const selectedCategories = [];
    document.querySelectorAll('.category-checkbox:checked').forEach(cb => {
        selectedCategories.push(cb.value);
    });
    
    // Show loading state
    showBudgetLoading();
    
    // Submit request
    fetch('/budget/optimize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            budget: budget,
            categories: selectedCategories
        })
    })
    .then(response => response.json())
    .then(data => {
        displayBudgetResults(data);
    })
    .catch(error => {
        console.error('Budget optimization error:', error);
        showBudgetError('An error occurred. Please try again.');
    });
}

function showBudgetLoading() {
    const resultsContainer = document.querySelector('.budget-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="budget-loading">
                <div class="loading-spinner"></div>
                <p>Finding the best products for your budget...</p>
            </div>
        `;
        resultsContainer.classList.add('loading');
    }
    
    // Scroll to results
    setTimeout(() => {
        document.querySelector('.budget-results')?.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }, 100);
}

function displayBudgetResults(data) {
    const resultsContainer = document.querySelector('.budget-results');
    
    if (!resultsContainer) return;
    
    resultsContainer.classList.remove('loading');
    
    if (data.error) {
        resultsContainer.innerHTML = `
            <div class="budget-error">
                <h3>😕 ${data.error}</h3>
                <p>Try increasing your budget or selecting more categories</p>
            </div>
        `;
        return;
    }
    
    // Build results HTML
    let html = `
        <div class="results-summary">
            <div class="summary-card">
                <div class="summary-icon"></div>
                <div class="summary-details">
                    <h4>Budget</h4>
                    <p>$${data.budget.toFixed(2)}</p>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon"></div>
                <div class="summary-details">
                    <h4>Total Cost</h4>
                    <p>$${data.total_cost.toFixed(2)}</p>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon"></div>
                <div class="summary-details">
                    <h4>Savings</h4>
                    <p>$${data.savings.toFixed(2)}</p>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon"></div>
                <div class="summary-details">
                    <h4>Items</h4>
                    <p>${data.total_items} products</p>
                </div>
            </div>
        </div>
    `;
    
    if (data.average_rating > 0) {
        html += `
            <div class="average-rating">
                <span>Average Rating:</span>
                <span class="stars">${getStarRating(data.average_rating)}</span>
                <span>(${data.average_rating.toFixed(1)})</span>
            </div>
        `;
    }
    
    if (data.selected_products && data.selected_products.length > 0) {
        html += `
            <div class="recommended-products">
                <h3> Recommended Products</h3>
                <div class="products-grid">
                    ${data.selected_products.map(product => createRecommendationCard(product)).join('')}
                </div>
            </div>
        `;
    }
    
    resultsContainer.innerHTML = html;
    
    // Scroll to results
    resultsContainer.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

function createRecommendationCard(product) {
    const stars = getStarRating(product.rating || 0);
    
    return `
        <div class="recommendation-card">
            <div class="product-image">
                ${product.image_url ? 
                    `<img src="${product.image_url}" alt="${escapeHtml(product.name)}">` :
                    `<div class="placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <h4 class="product-name">${escapeHtml(product.name)}</h4>
                <div class="product-rating">
                    <span class="stars">${stars}</span>
                    <span class="reviews">(${product.reviews || 0})</span>
                </div>
                <div class="product-price">$${(product.price || 0).toFixed(2)}</div>
                <button class="btn btn-primary btn-sm add-to-cart-btn" data-product-id="${product.id}">
                    Add to Cart
                </button>
            </div>
        </div>
    `;
}

function showBudgetError(message) {
    const resultsContainer = document.querySelector('.budget-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="budget-error">
                <h3>⚠️ ${message}</h3>
            </div>
        `;
    }
}

function getStarRating(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    let stars = '';
    for (let i = 0; i < fullStars; i++) stars += '★';
    if (halfStar) stars += '☆';
    for (let i = 0; i < emptyStars; i++) stars += '☆';
    
    return stars;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

function initResultsDisplay() {
    // Check if we're on the results page with pre-filled budget
    const urlParams = new URLSearchParams(window.location.search);
    const budget = urlParams.get('budget');
    
    if (budget && document.querySelector('#budget-form')) {
        document.querySelector('#budget-amount').value = budget;
    }
}

// Export for use
window.BudgetOptimizer = {
    submitBudgetRequest,
    displayBudgetResults
};