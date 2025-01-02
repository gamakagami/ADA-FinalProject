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
    distance_list = get_row_sum(distance_matrix)
    flow_list = get_row_sum(flow_matrix)

    distance = sorted([i for i in range(len(distance_list))], key=lambda i: distance_list[i], reverse=True) # Contains the index, but sorted by the sum of the array
    flow = sorted([i for i in range(len(flow_list))], key=lambda i: flow_list[i])

    arrangement = []
    for i in range(len(distance)):
        index = distance.index(i)
        arrangement.append(flow[index] + 1)

    optimal_cost = calculate_cost(arrangement, distance_matrix, flow_matrix)
    print(f"Optimal arrangement: {arrangement}, cost: {optimal_cost}")

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

greedy_approach(distance_matrix, flow_matrix)