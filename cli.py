
from data_manager import load_parcels, load_graph
from sorting import sort_by_priority
from knapsack import knapsack
from dijkstra import dijkstra, get_path
from tsp import nearest_neighbour
from performance import compare_performance, generate_graphs


def display_parcels(parcels):

    if not parcels:
        print("\nNo parcels found.")
        return

    print("\n" + "=" * 90)
    print("                         PARCEL DETAILS")
    print("=" * 90)

    print(f"{'ID':<12} {'Destination':<20} {'Weight':<12} "
          f"{'Priority':<12} {'Cost':<12} {'Status':<15}")

    print("-" * 90)

    for parcel in parcels:
        print(f"{parcel['parcel_id']:<12} "
              f"{parcel['destination']:<20} "
              f"{parcel['weight']:<12} "
              f"{parcel['priority']:<12} "
              f"{parcel['delivery_cost']:<12} "
              f"{parcel['status']:<15}")

    print("=" * 90)
    print(f"Total parcels: {len(parcels)}")


# 1. VIEW PARCELS
def view_parcels():
    parcels = load_parcels()
    display_parcels(parcels)


# 2. SORT PARCELS
def sort_parcels():

    parcels = load_parcels()

    if not parcels:
        print("\nNo parcels found.")
        return

    sorted_parcels = sort_by_priority(parcels)

    print("\nParcels sorted by priority (High -> Medium -> Low):")
    display_parcels(sorted_parcels)


# 3. KNAPSACK PACKING
def optimize_packing():

    parcels = load_parcels()

    if not parcels:
        print("\nNo parcels available.")
        return

    capacity = 12

    selected, total_weight, max_value = knapsack(parcels, capacity)

    print("\n========== OPTIMIZED PACKING PLAN ==========")
    print(f"Vehicle capacity: {capacity} kg")

    if not selected:
        print("No parcels selected.")
        return

    display_parcels(selected)

    total_weight = sum(p["weight"] for p in selected)
    total_cost = sum(p["delivery_cost"] for p in selected)

    print(f"\nTotal weight: {total_weight:.2f} kg")
    print(f"Total delivery value: {total_cost:.2f}")
    print(f"Maximum optimized value: {max_value}")


# 4. DIJKSTRA SHORTEST PATH
def find_shortest_paths():

    graph = load_graph()

    if not graph:
        print("\nGraph is empty.")
        return

    locations = list(graph.keys())

    print("\n========== DELIVERY LOCATIONS ==========")

    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")

    start = input("\nEnter starting location: ").strip()

    if start not in graph:
        print("\nInvalid location name.")
        return

    distances, previous = dijkstra(graph, start)

    print(f"\n========== SHORTEST PATHS FROM {start} ==========")

    for destination in locations:

        if distances[destination] == float("inf"):
            print(f"\n{destination}: Unreachable")
            continue

        path = get_path(previous, destination)

        print(f"\nDestination: {destination}")
        print(f"Distance: {distances[destination]} km")
        print("Path: " + " -> ".join(path))


# 5. TSP DELIVERY ROUTE
def generate_delivery_route():

    graph = load_graph()

    if not graph:
        print("\nGraph is empty.")
        return

    locations = list(graph.keys())

    print("\n========== DELIVERY LOCATIONS ==========")

    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")

    start = input("\nEnter starting location: ").strip()

    if start not in graph:
        print("\nInvalid starting location.")
        return

    distance_matrix = {}

    for source in locations:
        distances, previous = dijkstra(graph, source)
        distance_matrix[source] = distances

    route, total_distance = nearest_neighbour(distance_matrix, start)

    print("\n========== DELIVERY ROUTE ==========")
    print("Route: " + " -> ".join(route))
    print(f"Total route distance: {total_distance} km")


# 6. PERFORMANCE ANALYSIS + GRAPHS
def performance_analysis():

    parcels = load_parcels()
    graph = load_graph()

    if not parcels or not graph:
        print("\nParcels or graph data is missing.")
        return

    locations = list(graph.keys())

    print("\n========== DELIVERY LOCATIONS ==========")

    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")

    start = input("\nEnter starting location for performance test: ").strip()

    if start not in graph:
        print("\nInvalid location name.")
        return

    capacity = 12

    print("\nRunning performance tests (100 repetitions)...")

    results = compare_performance(parcels, graph, capacity, start)

    print("\n========== PERFORMANCE RESULTS ==========")
    print(f"{'Algorithm':<25} {'Average Runtime (seconds)':<25}")
    print("-" * 55)

    for algorithm, runtime in results.items():
        print(f"{algorithm:<25} {runtime:.8f}")

    print("-" * 55)

    print("\nGenerating performance graphs...")

    generate_graphs(results)

    print("\nGraphs saved as:")
    print("1. runtime_bar_chart.png")
    print("2. runtime_line_chart.png")


# MAIN TERMINAL MENU
def run_terminal():

    while True:

        print("\n========== MINI-COURIER PLANNER ==========")
        print("1. View all parcels")
        print("2. Sort parcels by priority")
        print("3. Optimize parcel packing (Knapsack)")
        print("4. Find shortest paths (Dijkstra)")
        print("5. Generate delivery route (TSP)")
        print("6. Performance analysis + graphs")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_parcels()

        elif choice == "2":
            sort_parcels()

        elif choice == "3":
            optimize_packing()

        elif choice == "4":
            find_shortest_paths()

        elif choice == "5":
            generate_delivery_route()

        elif choice == "6":
            performance_analysis()

        elif choice == "7":
            print("\nExiting Terminal Mode.")
            break

        else:
            print("\nInvalid choice. Try again.")


if __name__ == "__main__":
    run_terminal()
