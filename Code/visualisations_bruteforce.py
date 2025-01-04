import time
import matplotlib.pyplot as plt
from math import factorial

def get_workstations():
    try:
        workstations_num = int(input("Enter the number of workstations: "))
        if workstations_num < 3:
            print("Number of workstations must be greater than 2.")
            return get_workstations()
        return workstations_num
    except:
        print("Please enter an integer")
        return get_workstations()


def get_matrix(workstations_count, minimum_value, variable, variable2):
    matrix = []
    for i in range(workstations_count):
        temporary_array = []
        for j in range(workstations_count):
            if i == j:
                temporary_array.append(0)
                continue
            if j > i:
                value_valid = False
                while not value_valid:
                    try:
                        value = int(input(f"Enter the {variable} between {variable2} {i + 1} and {j + 1}: "))
                        if value < minimum_value:
                            raise ValueError
                        else:
                            temporary_array.append(value)
                            value_valid = True
                    except:
                        print(f"The {variable} must be an integer and greater than {minimum_value - 1}.")
            else:
                temporary_array.append(matrix[j][i])
        matrix.append(temporary_array)
    return matrix


def permutations(nums):
    perms = []
    solution = []

    def backtrack():
        if len(nums) == len(solution):
            perms.append(solution[:])
            return
        for num in nums:
            if num not in solution:
                solution.append(num)
                backtrack()
                solution.pop()

    backtrack()
    return perms


def calculate_cost(arrangement, distance_matrix, flow_matrix):
    total_cost = 0
    i_count = 0
    for i in arrangement:
        j_count = 0
        for j in arrangement:
            if i_count < j_count:
                total_cost += distance_matrix[i_count][j_count] * flow_matrix[i - 1][j - 1]
            j_count += 1
        i_count += 1
    return total_cost


def bruteforce(distance_matrix, flow_matrix, possible_arrangements):
    optimal_cost = None
    optimal_arrangement = None
    for arrangement in possible_arrangements:
        print(f"Processing arrangement {arrangement}....")
        total_cost = calculate_cost(arrangement, distance_matrix, flow_matrix)
        print(f"Cost of arrangement {arrangement}: {total_cost}")
        if optimal_cost is None or total_cost < optimal_cost:
            optimal_cost = total_cost
            optimal_arrangement = arrangement
            print(f"Arrangement {optimal_arrangement} becomes most optimal arrangement.")
    print(f"The optimal arrangement is {optimal_arrangement}, with a total cost of {optimal_cost}")


def measure_time(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start


def simulate_matrix_creation(n):
    return [[0 if i == j else 1 for j in range(n)] for i in range(n)]


def simulate_permutations(n):
    nums = list(range(1, n + 1))
    return permutations(nums)


def simulate_cost_calculation(n):
    distance_matrix = simulate_matrix_creation(n)
    flow_matrix = simulate_matrix_creation(n)
    arrangements = simulate_permutations(n)
    for arr in arrangements:
        calculate_cost(arr, distance_matrix, flow_matrix)


input_sizes = range(3, 8)
times = {"Matrix Creation": [], "Permutation Generation": [], "Cost Calculation": []}

for n in input_sizes:
    times["Matrix Creation"].append(measure_time(simulate_matrix_creation, n))
    times["Permutation Generation"].append(measure_time(simulate_permutations, n))
    times["Cost Calculation"].append(measure_time(simulate_cost_calculation, n))

plt.figure(figsize=(10, 6))
for step, time_list in times.items():
    plt.plot(input_sizes, time_list, label=step)

plt.title("Time Complexity")
plt.xlabel("Input Size")
plt.ylabel("Execution Time")
plt.legend()
plt.grid()
plt.show()

space_complexity = [n ** 2 + factorial(n) for n in input_sizes]
plt.figure(figsize=(10, 6))
plt.plot(input_sizes, space_complexity, marker='o', label="Space Complexity (O(n^2 + n!))")
plt.title("Space Complexity")
plt.xlabel("Input Size")
plt.ylabel("Space Usage")
plt.legend()
plt.grid()
plt.show()

workstations = 3
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
indexes = [i + 1 for i in range(workstations)]
possible_outcomes = permutations(indexes)
bruteforce(distance_matrix, flow_matrix, possible_outcomes)

def visualize_big_o():
    input_sizes = range(3, 8)

    matrix_creation_time = [n ** 2 for n in input_sizes]  # O(n^2)
    permutation_generation_time = [factorial(n) * n for n in input_sizes]  # O(n * n!)
    brute_force_time = [factorial(n) * (n ** 2) for n in input_sizes]  # O(n! * n^2)

    space_complexity = [n ** 2 + factorial(n) for n in input_sizes]  # O(n^2 + n!)

    plt.figure(figsize=(12, 6))
    plt.plot(input_sizes, matrix_creation_time, label="Matrix Creation (O(n^2))", marker='o')
    plt.plot(input_sizes, permutation_generation_time, label="Permutation Generation (O(n * n!))", marker='o')
    plt.plot(input_sizes, brute_force_time, label="Brute Force (O(n! * n^2))", marker='o')
    plt.title("Big O Time Complexity")
    plt.xlabel("Input Size")
    plt.ylabel("Time Complexity")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(12, 6))
    plt.plot(input_sizes, space_complexity, label="Space Complexity (O(n^2 + n!))", marker='o')
    plt.title("Big O Space Complexity")
    plt.xlabel("Input Size")
    plt.ylabel("Space Complexity")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.show()


workstations = 3
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
indexes = [i + 1 for i in range(workstations)]
possible_outcomes = permutations(indexes)
bruteforce(distance_matrix, flow_matrix, possible_outcomes)

visualize_big_o()

def measure_bruteforce_time(n):
    distance_matrix = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    flow_matrix = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    indexes = [i + 1 for i in range(n)]
    possible_arrangements = permutations(indexes)

    start = time.perf_counter()
    bruteforce(distance_matrix, flow_matrix, possible_arrangements)
    end = time.perf_counter()
    return end - start


results = []

for n in range(3, 6):
    execution_time = measure_bruteforce_time(n)
    results.append((n, execution_time))

input_sizes = [r[0] for r in results]
execution_times = [r[1] for r in results]

threshold = 0.001
adjusted_execution_times = [max(time, threshold) for time in execution_times]


plt.figure(figsize=(10, 6))
plt.bar(input_sizes, adjusted_execution_times, color='skyblue', edgecolor='black')
plt.title("Execution Time for Brute Force Function", fontsize=14)
plt.xlabel("Input Size", fontsize=12)
plt.ylabel("Execution Time", fontsize=12)
plt.xticks(input_sizes)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
