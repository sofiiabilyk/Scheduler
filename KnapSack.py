def knapsack_01(weights, values, capacity):
    """
    The 0-1 knapsack problem: Given items with weights and values, determine
    the maximum value that can be obtained without exceeding the weight capacity.
    Each item can be taken at most once (0-1 means either take it or don't).
    
    Parameters:
        weights
             List of weights for each item
        values
            List of values for each item
        capacity
            Maximum weight capacity of the knapsack
    
    Returns:
        tuple: (max_value, selected_items)
            - max_value: Maximum value achievable
            - selected_items: List of indices of items to include (0-indexed)
    
    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    """
    n = len(weights)
    
    # Creating DP table - dp[i][w] 
    dp = [[0 for j in range(capacity + 1)] for i in range(n + 1)]
    
    # Build DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            #Take item i-1 (if it fits)
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    # Reconstruct the solution to find which items were selected
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    selected_items.reverse()
    max_value = dp[n][capacity]
    
    return max_value, selected_items

