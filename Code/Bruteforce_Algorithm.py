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
    optimal_cost = None
    optimal_arrangement = None
    for arrangement in possible_arrangements:
        print(f"Processing arrangement {arrangement}....")
        total_cost = calculate_cost(arrangement, distance_matrix, flow_matrix) # Calculate the cost for a specific arrangement
        print(f"Cost of arrangement {arrangement}: {total_cost}")

        # Becomes optimal cost if it's null
        if optimal_cost == None:
            optimal_cost = total_cost
            optimal_arrangement = arrangement
            print(f"Arrangement {optimal_arrangement} becomes most optimal arrangement.")

        # Replaces optimal cost if optimal cost is higher than the newly obtained cost.
        elif total_cost < optimal_cost:
            optimal_cost = total_cost
            optimal_arrangement = arrangement
            print(f"Arrangement {optimal_arrangement} becomes most optimal arrangement.")
    
    print(f"The optimal arrangement is {optimal_arrangement}, with a total cost of {optimal_cost}")

#workstations = get_workstations()

#distance_matrix = get_matrix(workstations, 1, "distance", "locations")
#flow_matrix = get_matrix(workstations, 0, "frequency of communication", "workstations")

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
