import time, tracemalloc


def calculate_cost(arrangement, distance_matrix, flow_matrix): # Time: O(n^2) Space: O(1)
    total_cost = 0 # Time: O(1) Space: O(1)
    i_count = 0 # Time: O(1) Space: O(1)
    for i in arrangement: # Time: O(n) Space: O(1)
        j_count = 0 # Time: O(1) Space: O(1)
        for j in arrangement: # Time: O(n) Space: O(1)
            if j_count > i_count: # Time: O(1) Space: O(1)
                total_cost += distance_matrix[i_count][j_count] * flow_matrix[i - 1][j - 1] # Time: O(1) Space: O(1)
            j_count += 1 # Time: O(1) Space: O(1)
        i_count += 1 # Time: O(1) Space: O(1)
    return total_cost # Time: O(1) Space: O(1)


def calculate_partial_cost(last_cost, new_arrangement, distance_matrix, flow_matrix): # Time: O(n) Space: O(1)
    workstation_added = new_arrangement[-1] # Time: O(1) Space: O(1)
    location_added = new_arrangement.index(workstation_added) # Time: O(n) Space: O(1)
    i_count = 0 # Time: O(1) Space: O(1)
    for i in new_arrangement: # Time: O(n) Space: O(1)
        if i != workstation_added: # Time: O(1) Space: O(1)
            last_cost += distance_matrix[i_count][location_added] * flow_matrix[i - 1][workstation_added - 1] # Time: O(1) Space: O(1)
        i_count += 1 # Time: O(1) Space: O(1)
    return last_cost # Time: O(1) Space: O(1)


def branch_and_bound(distance_matrix, flow_matrix): # Time: O(n!) Space: O(n!)
    tracemalloc.start()  # Start tracking memory usage # Time: O(1) Space: O(1)
    start_time = time.perf_counter()  # Start the timer # Time: O(1) Space: O(1)

    best_cost = float("inf")  # Initialize the best cost as infinity # Time: O(1) Space: O(1)
    best_solution = None  # To track the best solution # Time: O(1) Space: O(n)
    nums = [i + 1 for i in range(len(distance_matrix))] # Time: O(n) Space: O(n)

    # Stack to manage DFS state: (current solution, current cost)
    stack = [([], 0)] # Time: O(1) Space: O(n)

    while stack: # Time: O(n!) Space: O(1)
        solution, current_cost = stack.pop() # Time: O(1) Space: O(1)

        # If the current solution is complete, check if it's the best
        if len(solution) == len(nums): # Time: O(1) Space: O(1)
            if current_cost < best_cost: # Time: O(1) Space: O(1)
                best_cost = current_cost # Time: O(1) Space: O(1)
                best_solution = solution[:] # Time: O(n) Space: O(n)
            continue # Time: O(1) Space: O(1)

        for num in nums: # Time: O(n) Space: O(1)
            if num not in solution: # Time: O(n) Space: O(1)
                # Generate new solution by adding this facility
                new_solution = solution + [num] # Time: O(n) Space: O(n)
                new_cost = calculate_partial_cost(current_cost, new_solution, distance_matrix, flow_matrix) # Time: O(n) Space: O(1)

                # Only continue if this new cost is promising
                if new_cost < best_cost: # Time: O(1) Space: O(1)
                    stack.append((new_solution, new_cost)) # Time: O(1) Space: O(n)

    end_time = time.perf_counter()  # Stop the timer # Time: O(1) Space: O(1)
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage # Time: O(1) Space: O(1)
    tracemalloc.stop()  # Stop tracking memory usage # Time: O(1) Space: O(1)

    print(f"Elapsed time: {end_time - start_time:.6f} seconds") # Time: O(1) Space: O(1)
    print(f"Total memory used: {current} bytes") # Time: O(1) Space: O(1)
    print(f"Peak memory used: {peak} bytes") # Time: O(1) Space: O(1)
    return best_cost, best_solution # Time: O(1) Space: O(n)


distance_matrix = [[0, 7, 9, 8, 10], [7, 0, 6, 2, 2], [9, 6, 0, 8, 7], [8, 2, 8, 0, 6], [10, 2, 7, 6, 0]] # Time: O(1) Space: O(n^2)
flow_matrix = [[0, 10, 7, 10, 3], [10, 0, 6, 7, 7], [7, 6, 0, 1, 1], [10, 7, 1, 0, 4], [3, 7, 1, 4, 0]] # Time: O(1) Space: O(n^2)
optimal_cost, optimal_solution = branch_and_bound(distance_matrix, flow_matrix) # Time: O(n!) Space: O(n!)

print(f"\nThe optimal arrangement is {optimal_solution}, with a total cost of {optimal_cost}") # Time: O(1) Space: O(1)
