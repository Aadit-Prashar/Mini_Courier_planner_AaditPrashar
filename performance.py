import time
import matplotlib.pyplot as plt

from sorting import sort_by_priority
from knapsack import knapsack
from dijkstra import dijkstra
from tsp import nearest_neighbour


def compare_performance(parcels, graph, capacity, start):

    results = {}
    repetitions = 100

    # 1. Bubble Sort
    start_time = time.perf_counter()

    for _ in range(repetitions):
        sort_by_priority(parcels)

    end_time = time.perf_counter()

    results["Bubble Sort"] = (end_time - start_time) / repetitions

    # 2. Knapsack DP
    start_time = time.perf_counter()

    for _ in range(repetitions):
        knapsack(parcels, capacity)

    end_time = time.perf_counter()

    results["Knapsack DP"] = (end_time - start_time) / repetitions

    # 3. Dijkstra
    start_time = time.perf_counter()

    for _ in range(repetitions):
        dijkstra(graph, start)

    end_time = time.perf_counter()

    results["Dijkstra"] = (end_time - start_time) / repetitions

    # 4. Prepare distance matrix for Nearest Neighbor
    distance_matrix = {}

    for node in graph:
        distances, previous = dijkstra(graph, node)
        distance_matrix[node] = distances

    # 5. Nearest Neighbor
    start_time = time.perf_counter()

    for _ in range(repetitions):
        nearest_neighbour(distance_matrix, start)

    end_time = time.perf_counter()

    results["Nearest Neighbour"] = (end_time - start_time) / repetitions

    return results


def generate_graphs(results):

    algorithms = list(results.keys())
    runtimes = list(results.values())

    # BAR GRAPH
    plt.figure(figsize=(9, 5))

    plt.bar(algorithms, runtimes)

    plt.title("Algorithm Runtime Comparison")
    plt.xlabel("Algorithms")
    plt.ylabel("Average Runtime (seconds)")
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig("runtime_bar_chart.png")
    plt.show()

    # LINE GRAPH
    plt.figure(figsize=(9, 5))

    plt.plot(algorithms, runtimes, marker="o")

    plt.title("Algorithm Runtime Trend")
    plt.xlabel("Algorithms")
    plt.ylabel("Average Runtime (seconds)")
    plt.xticks(rotation=20)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("runtime_line_chart.png")
    plt.show()
