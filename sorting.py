
def sort_by_priority(parcels):

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    parcels = parcels.copy()

    n = len(parcels)

    # Bubble Sort
    for i in range(n):
        for j in range(0, n - i - 1):

            if priority_order[parcels[j]["priority"]] > priority_order[parcels[j + 1]["priority"]]:

                temp = parcels[j]
                parcels[j] = parcels[j + 1]
                parcels[j + 1] = temp

    return parcels
