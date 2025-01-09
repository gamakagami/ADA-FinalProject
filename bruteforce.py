import tracemalloc
import time

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
                    while value_valid == False:
                        try:
                            value = int(input(f"Enter the {variable} between {variable2} {i + 1} and {j + 1}: "))
                            if value < minimum_value:
                                raise ValueError
                            else:
                                temporary_array.append(value)
                                value_valid = True
                        except:
                            print(f"The {variable} must be an integer and greater than 0.")
                else:
                    temporary_array.append(matrix[j][i])
            matrix.append(temporary_array)
    return matrix

def permutations(nums):
    perms = []
    solution = []

    def backtrack():
        if len(nums) == len(solution):
            perms.append(solution[:]) # Once the solution array reaches the maximum length, the copy of the solution is appended.
            return  
        for num in nums:
            if num not in solution: # Ensure no number is used twice
                solution.append(num)
                backtrack() # Continue appending numbers to the current solution
                solution.pop() # Remove the last number added
    
    backtrack()
    return perms

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

def bruteforce(distance_matrix, flow_matrix, possible_arrangements):
    tracemalloc.start()  # Start tracking memory usage
    start_time = time.perf_counter()  # Start the timer

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

    end_time = time.perf_counter()  # Stop the timer
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop tracking memory usage

    print(f"\nThe optimal arrangement is {optimal_arrangement}, with a total cost of {optimal_cost}")
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")
    print(f"Total memory used: {current} bytes")
    print(f"Peak memory used: {peak} bytes")


#workstations = get_workstations()

#distance_matrix = get_matrix(workstations, 1, "distance", "locations")
#flow_matrix = get_matrix(workstations, 0, "frequency of communication", "workstations")

workstations = 10

distance_matrix = [[0, 2, 6, 6, 1, 4, 3, 9, 7, 6], [2, 0, 7, 8, 5, 6, 4, 6, 2, 4], [6, 7, 0, 10, 4, 10, 2, 9, 7, 5],
                   [6, 8, 10, 0, 6, 7, 7, 4, 5, 3], [1, 5, 4, 6, 0, 3, 10, 2, 1, 10], [4, 6, 10, 7, 3, 0, 9, 10, 6, 8],
                   [3, 4, 2, 7, 10, 9, 0, 5, 8, 7], [9, 6, 9, 4, 2, 10, 5, 0, 9, 3], [7, 2, 7, 5, 1, 6, 8, 9, 0, 7],
                   [6, 4, 5, 3, 10, 8, 7, 3, 7, 0]]
flow_matrix = [[0, 3, 3, 6, 5, 6, 9, 1, 9, 3], [3, 0, 6, 10, 2, 2, 10, 1, 3, 9], [3, 6, 0, 8, 8, 6, 8, 1, 8, 4],
               [6, 10, 8, 0, 6, 8, 7, 5, 3, 4], [5, 2, 8, 6, 0, 8, 9, 10, 9, 7], [6, 2, 6, 8, 8, 0, 5, 10, 10, 9],
               [9, 10, 8, 7, 9, 5, 0, 5, 8, 4], [1, 1, 1, 5, 10, 10, 5, 0, 7, 1], [9, 3, 8, 3, 9, 10, 8, 7, 0, 2],
               [3, 9, 4, 4, 7, 9, 4, 1, 2, 0]]

indexes = [i + 1 for i in range(workstations)]
possible_outcomes = permutations(indexes)

bruteforce(distance_matrix, flow_matrix, possible_outcomes)
