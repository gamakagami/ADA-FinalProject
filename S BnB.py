import time, tracemalloc


def calculate_cost(arrangement, distance_matrix, flow_matrix):
    total_cost = 0
    i_count = 0
    for i in arrangement:
        j_count = 0
        for j in arrangement:
            if j_count > i_count:
                total_cost += distance_matrix[i_count][j_count] * flow_matrix[i - 1][j - 1]
            j_count += 1
        i_count += 1
    return total_cost


def calculate_partial_cost(last_cost, new_arrangement, distance_matrix, flow_matrix):
    workstation_added = new_arrangement[-1]
    location_added = new_arrangement.index(workstation_added)
    i_count = 0
    for i in new_arrangement:
        if i != workstation_added:
            last_cost += distance_matrix[i_count][location_added] * flow_matrix[i - 1][workstation_added - 1]
        i_count += 1
    return last_cost


def branch_and_bound(distance_matrix, flow_matrix):
    tracemalloc.start()  # Start tracking memory usage
    start_time = time.perf_counter()  # Start the timer

    best_cost = float("inf")  # Initialize the best cost as infinity
    best_solution = None  # To track the best solution
    nums = [i + 1 for i in range(len(distance_matrix))]

    # Stack to manage DFS state: (current solution, current cost)
    stack = [([], 0)]

    while stack:
        solution, current_cost = stack.pop()

        # If the current solution is complete, check if it's the best
        if len(solution) == len(nums):
            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = solution[:]
            continue

        for num in nums:
            if num not in solution:
                # Generate new solution by adding this facility
                new_solution = solution + [num]
                new_cost = calculate_partial_cost(current_cost, new_solution, distance_matrix, flow_matrix)

                # Only continue if this new cost is promising
                if new_cost < best_cost:
                    stack.append((new_solution, new_cost))

    end_time = time.perf_counter()  # Stop the timer
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop tracking memory usage

    print(f"Elapsed time: {end_time - start_time:.6f} seconds")
    print(f"Total memory used: {current} bytes")
    print(f"Peak memory used: {peak} bytes")
    return best_cost, best_solution


distance_matrix = [[0, 6, 8, 1, 4, 10, 10], [6, 0, 3, 1, 5, 9, 10], [8, 3, 0, 1, 6, 6, 9], [1, 1, 1, 0, 5, 4, 2], [4, 5, 6, 5, 0, 6, 9], [10, 9, 6, 4, 6, 0, 10], [10, 10, 9, 2, 9, 10, 0]]
flow_matrix = [[0, 5, 8, 10, 4, 4, 5], [5, 0, 10, 8, 2, 4, 5], [8, 10, 0, 5, 4, 9, 9], [10, 8, 5, 0, 6, 9, 8], [4, 2, 4, 6, 0, 4, 7], [4, 4, 9, 9, 4, 0, 6], [5, 5, 9, 8, 7, 6, 0]]
optimal_cost, optimal_solution = branch_and_bound(distance_matrix, flow_matrix)

print(f"\nThe optimal arrangement is {optimal_solution}, with a total cost of {optimal_cost}")
