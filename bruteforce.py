import time
import tracemalloc

def calculate_cost(arrangement, distance_matrix, flow_matrix):  # Time: O(n^2), Space: O(1)
    total_cost = 0  # Time: O(1), Space: O(1)
    i_count = 0  # Time: O(1), Space: O(1)
    for i in arrangement:  # Time: O(n), Space: O(1)
        j_count = 0  # Time: O(1), Space: O(1)
        for j in arrangement:  # Time: O(n), Space: O(1)
            if i_count < j_count:  # Time: O(1), Space: O(1)
                total_cost += distance_matrix[i_count][j_count] * flow_matrix[i - 1][j - 1]  # Time: O(1), Space: O(1)
            j_count += 1  # Time: O(1), Space: O(1)
        i_count += 1  # Time: O(1), Space: O(1)
    return total_cost  # Time: O(1), Space: O(1)

def bruteforce(distance_matrix, flow_matrix):  # Time: O(n!), Space: O(n!)
    tracemalloc.start()  # Start tracking memory usage # Time: O(1), Space: O(1)
    start_time = time.perf_counter()  # Start the timer # Time: O(1), Space: O(1)

    optimal_cost = float("inf")  # Initialize the optimal cost # Time: O(1), Space: O(1)
    optimal_arrangement = None  # Initialize the optimal arrangement # Time: O(1), Space: O(n)

    def permutations(nums):  # Time: O(n!), Space: O(n!)
        solution = []  # Time: O(1), Space: O(n)
        def backtrack():  # Time: O(n!), Space: O(n)
            nonlocal optimal_cost, optimal_arrangement
            if len(nums) == len(solution):  # Time: O(1), Space: O(1)
                total_cost = calculate_cost(solution, distance_matrix, flow_matrix)  # Time: O(n^2), Space: O(1)
                if total_cost < optimal_cost:  # Time: O(1), Space: O(1)
                    optimal_cost = total_cost  # Time: O(1), Space: O(1)
                    optimal_arrangement = solution[:]  # Time: O(n), Space: O(n)
                return  # Time: O(1), Space: O(1)

            for num in nums:  # Time: O(n), Space: O(1)
                if num not in solution:  # Time: O(n), Space: O(1)
                    solution.append(num)  # Time: O(1), Space: O(1)
                    backtrack()  # Recursive call # Time: O(n!), Space: O(n)
                    solution.pop()  # Backtrack step # Time: O(1), Space: O(1)
        backtrack()
        return optimal_cost, optimal_arrangement  # Time: O(1), Space: O(n)
        

    indexes = [i + 1 for i in range(len(distance_matrix))]  # Time: O(n), Space: O(n)
    optimal_cost, optimal_arrangement = permutations(indexes)  # Time: O(n!), Space: O(n!)

    print(f"Optimal cost: {optimal_cost}, arrangement: {optimal_arrangement}")  # Time: O(1), Space: O(1)

    end_time = time.perf_counter()  # Stop the timer # Time: O(1), Space: O(1)
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage # Time: O(1), Space: O(1)
    tracemalloc.stop()  # Stop tracking memory usage # Time: O(1), Space: O(1)

    print(f"\nThe optimal arrangement is {optimal_arrangement}, with a total cost of {optimal_cost}")  # Time: O(1), Space: O(1)
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")  # Time: O(1), Space: O(1)
    print(f"Total memory used: {current} bytes")  # Time: O(1), Space: O(1)
    print(f"Peak memory used: {peak} bytes")  # Time: O(1), Space: O(1)

distance_matrix = [[0, 2, 6, 6, 1, 4, 3, 9, 7, 6], [2, 0, 7, 8, 5, 6, 4, 6, 2, 4], [6, 7, 0, 10, 4, 10, 2, 9, 7, 5], [6, 8, 10, 0, 6, 7, 7, 4, 5, 3], [1, 5, 4, 6, 0, 3, 10, 2, 1, 10], [4, 6, 10, 7, 3, 0, 9, 10, 6, 8], [3, 4, 2, 7, 10, 9, 0, 5, 8, 7], [9, 6, 9, 4, 2, 10, 5, 0, 9, 3], [7, 2, 7, 5, 1, 6, 8, 9, 0, 7], [6, 4, 5, 3, 10, 8, 7, 3, 7, 0]]  # Time: O(1), Space: O(n^2)
flow_matrix = [[0, 3, 3, 6, 5, 6, 9, 1, 9, 3], [3, 0, 6, 10, 2, 2, 10, 1, 3, 9], [3, 6, 0, 8, 8, 6, 8, 1, 8, 4], [6, 10, 8, 0, 6, 8, 7, 5, 3, 4], [5, 2, 8, 6, 0, 8, 9, 10, 9, 7], [6, 2, 6, 8, 8, 0, 5, 10, 10, 9], [9, 10, 8, 7, 9, 5, 0, 5, 8, 4], [1, 1, 1, 5, 10, 10, 5, 0, 7, 1], [9, 3, 8, 3, 9, 10, 8, 7, 0, 2], [3, 9, 4, 4, 7, 9, 4, 1, 2, 0]]  # Time: O(1), Space: O(n^2)
bruteforce(distance_matrix, flow_matrix)  # Time: O(n!), Space: O(n!)
