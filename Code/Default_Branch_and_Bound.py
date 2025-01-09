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


def branch_and_bound(distance_matrix, flow_matrix):
    start = time.perf_counter()
    tracemalloc.start()

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

        for num in nums:
            if num not in solution:
                solution.append(num)
                partial_cost = calculate_cost(solution, distance_matrix, flow_matrix)
                print(solution)
                if partial_cost >= best_cost: 
                    solution.pop()
                    print(f"Pruning Branch {solution}")
                    continue
                backtrack()
                solution.pop()

    backtrack()  
    end_time = time.perf_counter()
    exec_time = end_time - start
    print(exec_time)
    print(tracemalloc.get_traced_memory())
    return best_cost, best_solution

distance_matrix = [[0, 7, 9, 8, 10], [7, 0, 6, 2, 2], [9, 6, 0, 8, 7], [8, 2, 8, 0, 6], [10, 2, 7, 6, 0]]
flow_matrix = [[0, 10, 7, 10, 3], [10, 0, 6, 7, 7], [7, 6, 0, 1, 1], [10, 7, 1, 0, 4], [3, 7, 1, 4, 0]]
optimal_cost, optimal_solution = branch_and_bound(distance_matrix, flow_matrix)

print("Optimal Cost:", optimal_cost)
print("Optimal Solution:", optimal_solution)