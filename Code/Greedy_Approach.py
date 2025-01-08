import time
import tracemalloc

def calculate_cost(arrangement, distance_matrix, flow_matrix):
    total_cost = 0
    i_count = 0
    # i and j are used to go through all possible pairs of workstations, the arrangement array contains the workstation number (As an index), where the position index is used as the location.
    for i in arrangement:
        j_count = 0
        for j in arrangement:
            # i_count must be lower than j_count to make sure that only the top half of the matrix is calculated in order to prevent calculating the same pair twice.
            if i_count < j_count:
                # The count represents the index of the distance between locations in the distance matrix, while the values in the arrangement array represents the index of the workstations in the flow matrix.
                total_cost += distance_matrix[i_count][j_count] * flow_matrix[i - 1][j - 1]
            j_count += 1
        i_count += 1
    return total_cost

def get_row_sum(matrix):
    container = []
    for array in matrix:
        sum = 0
        for nums in array:
            sum += nums
        container.append(sum)

    return container

def greedy_approach(distance_matrix, flow_matrix):
    start = time.perf_counter()
    tracemalloc.start()

    distance_list = get_row_sum(distance_matrix)
    flow_list = get_row_sum(flow_matrix)

    distance = sorted([i for i in range(len(distance_list))], key=lambda i: distance_list[i], reverse=True) # Contains the index, but sorted by the sum of the array
    flow = sorted([i for i in range(len(flow_list))], key=lambda i: flow_list[i]) # Each value of the input array is assigned with a new value, and the original values are sorted by that new value.

    arrangement = [] # Flow[i] is assigned to Distance[i]
    for i in range(len(distance)): # i or index of the arrangement list represents the location.
        index = distance.index(i) # Find index of location i 
        arrangement.append(flow[index] + 1) # For location i, append the flow assigned to it, and add it by 1 (Because the calculate cost function calculates for workstations 1 and so on)

    optimal_cost = calculate_cost(arrangement, distance_matrix, flow_matrix)
    print(f"Optimal arrangement: {arrangement}, cost: {optimal_cost}")

    end = time.perf_counter()
    exec_time = end - start
    print(f"Execution Time: {exec_time}")
    print(tracemalloc.get_traced_memory())

    tracemalloc.stop()

distance_matrix = [[0, 2, 6, 6, 1, 4, 3, 9, 7, 6], [2, 0, 7, 8, 5, 6, 4, 6, 2, 4], [6, 7, 0, 10, 4, 10, 2, 9, 7, 5], [6, 8, 10, 0, 6, 7, 7, 4, 5, 3], [1, 5, 4, 6, 0, 3, 10, 2, 1, 10], [4, 6, 10, 7, 3, 0, 9, 10, 6, 8], [3, 4, 2, 7, 10, 9, 0, 5, 8, 7], [9, 6, 9, 4, 2, 10, 5, 0, 9, 3], [7, 2, 7, 5, 1, 6, 8, 9, 0, 7], [6, 4, 5, 3, 10, 8, 7, 3, 7, 0]]
flow_matrix = [[0, 3, 3, 6, 5, 6, 9, 1, 9, 3], [3, 0, 6, 10, 2, 2, 10, 1, 3, 9], [3, 6, 0, 8, 8, 6, 8, 1, 8, 4], [6, 10, 8, 0, 6, 8, 7, 5, 3, 4], [5, 2, 8, 6, 0, 8, 9, 10, 9, 7], [6, 2, 6, 8, 8, 0, 5, 10, 10, 9], [9, 10, 8, 7, 9, 5, 0, 5, 8, 4], [1, 1, 1, 5, 10, 10, 5, 0, 7, 1], [9, 3, 8, 3, 9, 10, 8, 7, 0, 2], [3, 9, 4, 4, 7, 9, 4, 1, 2, 0]]
greedy_approach(distance_matrix, flow_matrix)
