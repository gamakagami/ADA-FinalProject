import time, tracemalloc


def calculate_cost(arrangement, distance_matrix, flow_matrix):
    """
    Calculates the total cost of a given arrangement.
    """
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


def calculate_bound(arrangement, distance_matrix, flow_matrix, nums):
    """
    Estimates the upper bound for a given partial arrangement.
    """
    bound = calculate_cost(arrangement, distance_matrix, flow_matrix)
    remaining_facilities = [num for num in nums if num not in arrangement]

    # Calculate the remaining cost (upper bound for remaining assignments)
    remaining_cost = sum(
        flow_matrix[fac_i - 1][fac_j - 1]
        for i, fac_i in enumerate(remaining_facilities)
        for j, fac_j in enumerate(remaining_facilities) if i < j
    )
    return bound + remaining_cost


def branch_and_bound(distance_matrix, flow_matrix):
    tracemalloc.start()
    start_time = time.perf_counter()

    best_cost = float("inf")  # Initialize the best cost as infinity
    best_solution = None  # To track the best solution
    solution = []  # Current solution (partial arrangement)
    nums = [i + 1 for i in range(len(distance_matrix))]  # Facility numbers

    def backtrack():
        nonlocal best_cost, best_solution

        if len(solution) == len(nums):
            cost = calculate_cost(solution, distance_matrix, flow_matrix)
            if cost < best_cost:
                best_cost = cost
                best_solution = solution[:]
            return

        # Generate the next candidate solutions
        for num in nums:
            if num not in solution:
                solution.append(num)

                # Calculate the upper bound for the current partial solution
                bound = calculate_bound(solution, distance_matrix, flow_matrix, nums)

                # Prune the branch if the bound is greater than or equal to the best cost
                if bound >= best_cost:
                    solution.pop()
                    continue

                # Recurse to explore the next step
                backtrack()
                solution.pop()

    # Start the backtracking search
    backtrack()

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nThe optimal arrangement is {best_solution}, with a total cost of {best_cost}")
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")
    print(f"Total memory used: {current} bytes")
    print(f"Peak memory used: {peak} bytes")

    return best_cost, best_solution


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

optimal_cost, optimal_solution = branch_and_bound(distance_matrix, flow_matrix)

print("Optimal Cost:", optimal_cost)
print("Optimal Solution:", optimal_solution)
