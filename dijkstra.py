import heapq

def dijkstra(graph, start):

    distances = {}
    previous = {}

    for node in graph:
        distances[node] = float("inf")
        previous[node] = None

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def get_path(previous, destination):

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path