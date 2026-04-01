"""
Budget Optimizer Service - Knapsack Algorithm Implementation
Finds the optimal combination of products within a given budget
"""

def optimize_budget(products, budget):
    """
    Uses dynamic programming (0/1 knapsack) to find optimal product combinations.
    
    Args:
        products: List of product dictionaries with 'id', 'price', 'value' (rating)
        budget: Maximum budget amount
    
    Returns:
        List of selected products and total value
    """
    if not products or budget <= 0:
        return [], 0
    
    # Filter products within budget
    valid_products = [p for p in products if p['price'] <= budget]
    if not valid_products:
        return [], 0
    
    n = len(valid_products)
    W = int(budget)
    
    # DP table: dp[i][w] = max value with first i items and weight limit w
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    # Build DP table
    for i in range(1, n + 1):
        product = valid_products[i - 1]
        weight = int(product['price'])
        value = product.get('rating', 0) * product.get('reviews', 1)  # Use rating * reviews as value
        
        for w in range(W + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Backtrack to find selected items
    selected = []
    w = W
    total_cost = 0
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            product = valid_products[i - 1]
            selected.append(product)
            total_cost += product['price']
            w -= int(product['price'])
    
    return selected, total_cost


def get_budget_recommendations(all_products, budget, categories=None):
    """
    Get budget recommendations with optional category filtering.
    
    Args:
        all_products: List of all available products
        budget: Maximum budget
        categories: Optional list of preferred categories
    
    Returns:
        Dictionary with recommendations and metadata
    """
    # Filter by categories if specified
    if categories:
        filtered = [p for p in all_products if p.get('category') in categories]
    else:
        filtered = all_products
    
    # Optimize
    selected, total_cost = optimize_budget(filtered, budget)
    
    # Calculate savings
    savings = budget - total_cost
    
    return {
        'selected_products': selected,
        'total_cost': round(total_cost, 2),
        'budget': budget,
        'savings': round(savings, 2),
        'total_items': len(selected),
        'average_rating': sum(p.get('rating', 0) for p in selected) / len(selected) if selected else 0
    }