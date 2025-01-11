import time, tracemalloc

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
    solution = []
    nums = [i + 1 for i in range(len(distance_matrix))]
    current_cost = 0

    def backtrack():
        nonlocal best_cost, best_solution, current_cost

        if len(solution) == len(nums):
            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = solution[:]
            return

        for num in nums:
            if num not in solution:
                solution.append(num)
                new_cost = calculate_partial_cost(current_cost, solution, distance_matrix, flow_matrix)
                if new_cost >= best_cost:
                    solution.pop()
                    continue

                previous_cost = current_cost
                current_cost = new_cost

                backtrack()
                current_cost = previous_cost
                solution.pop()

    backtrack()
    end_time = time.perf_counter()  # Stop the timer
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop tracking memory usage

    print(f"Elapsed time: {end_time - start_time:.6f} seconds")
    print(f"Total memory used: {current} bytes")
    print(f"Peak memory used: {peak} bytes")
    return best_cost, best_solution


distance_matrix = [[0, 2, 6, 6, 1, 4, 3, 9, 7, 6], [2, 0, 7, 8, 5, 6, 4, 6, 2, 4], [6, 7, 0, 10, 4, 10, 2, 9, 7, 5],
                   [6, 8, 10, 0, 6, 7, 7, 4, 5, 3], [1, 5, 4, 6, 0, 3, 10, 2, 1, 10], [4, 6, 10, 7, 3, 0, 9, 10, 6, 8],
                   [3, 4, 2, 7, 10, 9, 0, 5, 8, 7], [9, 6, 9, 4, 2, 10, 5, 0, 9, 3], [7, 2, 7, 5, 1, 6, 8, 9, 0, 7],
                   [6, 4, 5, 3, 10, 8, 7, 3, 7, 0]]
flow_matrix = [[0, 3, 3, 6, 5, 6, 9, 1, 9, 3], [3, 0, 6, 10, 2, 2, 10, 1, 3, 9], [3, 6, 0, 8, 8, 6, 8, 1, 8, 4],
               [6, 10, 8, 0, 6, 8, 7, 5, 3, 4], [5, 2, 8, 6, 0, 8, 9, 10, 9, 7], [6, 2, 6, 8, 8, 0, 5, 10, 10, 9],
               [9, 10, 8, 7, 9, 5, 0, 5, 8, 4], [1, 1, 1, 5, 10, 10, 5, 0, 7, 1], [9, 3, 8, 3, 9, 10, 8, 7, 0, 2],
               [3, 9, 4, 4, 7, 9, 4, 1, 2, 0]]
optimal_cost, optimal_solution = branch_and_bound(distance_matrix, flow_matrix)

print(f"\nThe optimal arrangement is {optimal_solution}, with a total cost of {optimal_cost}")
