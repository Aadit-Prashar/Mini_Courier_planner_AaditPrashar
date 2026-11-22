def knapsack(parcels, capacity=12):

    # Convert capacity and weights into units of 0.1 kg
    capacity_units = int(capacity * 10)

    n = len(parcels)

    dp = [[0 for _ in range(capacity_units + 1)] for _ in range(n + 1)]

    # Build the DP table
    for i in range(1, n + 1):

        weight = int(round(parcels[i - 1]["weight"] * 10))
        value = int(parcels[i - 1]["delivery_cost"])

        for w in range(capacity_units + 1):

            if weight <= w:

                dp[i][w] = max(
                    value + dp[i - 1][w - weight],
                    dp[i - 1][w]
                )

            else:
                dp[i][w] = dp[i - 1][w]

    # Trace back selected parcels
    selected = []
    w = capacity_units

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            parcel = parcels[i - 1]
            selected.append(parcel)

            w -= int(round(parcel["weight"] * 10))

    selected.reverse()

    # Calculate total selected weight
    total_weight = sum(p["weight"] for p in selected)

    # Calculate total delivery value
    total_value = dp[n][capacity_units]

    return selected, total_weight, total_value


def optimize_parcels(parcels, capacity=12):
    return knapsack(parcels, capacity)