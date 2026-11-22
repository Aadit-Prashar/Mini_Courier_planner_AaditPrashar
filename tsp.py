def nearest_neighbour(distance_matrix, start):

    unvisited = list(distance_matrix.keys())
    unvisited.remove(start)

    route = [start]
    total_distance = 0
    current = start

    while unvisited:

        nearest = None
        min_distance = float("inf")

        for location in unvisited:

            distance = distance_matrix[current][location]

            if distance < min_distance:
                min_distance = distance
                nearest = location

        if nearest is None or min_distance == float("inf"):
            break

        total_distance += min_distance
        route.append(nearest)
        unvisited.remove(nearest)

        current = nearest

    # Return to starting point
    if current in distance_matrix and start in distance_matrix[current]:
        return_distance = distance_matrix[current][start]

        if return_distance != float("inf"):
            total_distance += return_distance
            route.append(start)

    return route, total_distance