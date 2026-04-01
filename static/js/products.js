/**
 * Products - Filter & Search
 * Client-side product filtering and search
 */

document.addEventListener('DOMContentLoaded', function() {
    initProductFilters();
});

function initProductFilters() {
    // Search functionality
    initSearch();
    
    // Category filters
    initCategoryFilters();
    
    // Sort functionality
    initSort();
}

function initSearch() {
    const searchInput = document.querySelector('#search-input');
    const searchForm = document.querySelector('.search-form');
    
    if (searchInput && searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                performSearch(query);
            }
        });
        
        // Debounced search on input
        let debounceTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const query = this.value.trim();
                if (query.length >= 3) {
                    liveSearch(query);
                }
            }, 300);
        });
    }
}

function performSearch(query) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('q', query);
    currentUrl.searchParams.delete('page');
    window.location.href = currentUrl.toString();
}

function liveSearch(query) {
    fetch(`/api/products?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(products => {
            updateProductGrid(products);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function initCategoryFilters() {
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            applyFilters();
        });
    });
    
    // Clear filters button
    const clearFiltersBtn = document.querySelector('.clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            clearAllFilters();
        });
    }
}

function applyFilters() {
    const selectedCategories = [];
    document.querySelectorAll('.filter-checkbox:checked').forEach(checkbox => {
        selectedCategories.push(checkbox.value);
    });
    
    const currentUrl = new URL(window.location.href);
    
    if (selectedCategories.length > 0) {
        currentUrl.searchParams.set('category', selectedCategories.join(','));
    } else {
        currentUrl.searchParams.delete('category');
    }
    
    currentUrl.searchParams.delete('page');
    window.location.href = currentUrl.toString();
}

function clearAllFilters() {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.delete('category');
    currentUrl.searchParams.delete('q');
    currentUrl.searchParams.delete('page');
    window.location.href = currentUrl.toString();
}

function initSort() {
    const sortSelect = document.querySelector('#sort-select');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('sort', this.value);
            window.location.href = currentUrl.toString();
        });
    }
}

function updateProductGrid(products) {
    const grid = document.querySelector('.products-grid');
    
    if (!grid) return;
    
    if (products.length === 0) {
        grid.innerHTML = `
            <div class="no-products">
                <h3>No products found</h3>
                <p>Try adjusting your search or filters</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = products.map(product => createProductCard(product)).join('');
}

function createProductCard(product) {
    const stars = getStarRating(product.rating);
    
    return `
        <div class="product-card">
            <a href="/product/${product.id}">
                <div class="product-image">
                    ${product.image_url ? 
                        `<img src="${product.image_url}" alt="${escapeHtml(product.name)}">` :
                        `<div class="placeholder-image">📦</div>`
                    }
                </div>
                <div class="product-info">
                    <h3 class="product-name">${escapeHtml(product.name)}</h3>
                    <div class="product-rating">
                        <span class="stars">${stars}</span>
                        <span class="rating-count">(${product.reviews || 0})</span>
                    </div>
                    <div class="product-price">
                        $${product.price.toFixed(2)}
                    </div>
                    <div class="product-category">${escapeHtml(product.category || '')}</div>
                </div>
            </a>
            <button class="btn btn-primary add-to-cart-btn" data-product-id="${product.id}">
                Add to Cart
            </button>
        </div>
    `;
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
    div.textContent = text;
    return div.innerHTML;
}

// Export for use
window.ProductFilters = {
    performSearch,
    applyFilters,
    clearAllFilters
};