import tracemalloc
import time

def calculate_partial_cost(partial_assignment, distance_matrix, flow_matrix):
    """
    Calculates the cost of a partial assignment.
    """
    total_cost = 0
    for i, loc_i in enumerate(partial_assignment):
        for j, loc_j in enumerate(partial_assignment):
            if i < j:
                total_cost += distance_matrix[i][j] * flow_matrix[loc_i - 1][loc_j - 1]
    return total_cost

def calculate_bound(partial_assignment, distance_matrix, flow_matrix, num_workstations):
    """
    Estimates the upper bound for a partial assignment.
    """
    bound = calculate_partial_cost(partial_assignment, distance_matrix, flow_matrix)
    unassigned = [i + 1 for i in range(num_workstations) if i + 1 not in partial_assignment]
    remaining_cost = sum(
        flow_matrix[fac_i - 1][fac_j - 1]
        for i, fac_i in enumerate(unassigned)
        for j, fac_j in enumerate(unassigned) if i < j
    )
    return bound + remaining_cost

def branch_and_bound(distance_matrix, flow_matrix):
    """
    Solves the facility location problem using Branch and Bound.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    num_workstations = len(distance_matrix)
    nodes = []
    best_cost = float('inf')
    best_arrangement = None

    initial_bound = calculate_bound([], distance_matrix, flow_matrix, num_workstations)
    nodes.append((initial_bound, 0, [], list(range(1, num_workstations + 1))))

    while nodes:
        nodes.sort(key=lambda x: x[0])
        bound, current_cost, current_assignment, remaining_facilities = nodes.pop(0)

        if bound >= best_cost:
            continue

        if len(current_assignment) == num_workstations:
            if current_cost < best_cost:
                best_cost = current_cost
                best_arrangement = current_assignment
            continue

        for facility in remaining_facilities:
            next_assignment = current_assignment + [facility]
            next_remaining = [f for f in remaining_facilities if f != facility]
            partial_cost = calculate_partial_cost(next_assignment, distance_matrix, flow_matrix)
            bound = calculate_bound(next_assignment, distance_matrix, flow_matrix, num_workstations)

            if bound < best_cost:
                nodes.append((bound, partial_cost, next_assignment, next_remaining))

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nThe optimal arrangement is {best_arrangement}, with a total cost of {best_cost}")
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")
    print(f"Total memory used: {current} bytes")
    print(f"Peak memory used: {peak} bytes")
    return best_arrangement, best_cost

# Example usage
distance_matrix = [
    [0, 3, 5],
    [3, 0, 4],
    [5, 4, 0],
]

flow_matrix = [
    [0, 2, 1],
    [2, 0, 3],
    [1, 3, 0],
]

branch_and_bound(distance_matrix, flow_matrix)
