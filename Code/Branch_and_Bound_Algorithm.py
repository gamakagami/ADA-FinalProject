def get_workstations():
    """
    Prompts the user to input the number of workstations.
    Ensures the input is a valid integer greater than 2.
    If the input is invalid, it recursively asks the user for input again.
    """
    try:
        workstations_num = int(input("Enter the number of workstations: "))
        if workstations_num <= 2:
            print("Number of workstations must be greater than 2.")
            return get_workstations()  # Retry if the input is invalid
        return workstations_num
    except ValueError:
        print("Please enter an integer")  # Inform the user of the error
        return get_workstations()  # Retry if the input is not an integer

def get_matrix(workstations_count, minimum_value, variable, variable2):
    """
    Prompts the user to input values for a symmetric matrix (distance or flow).
    Ensures the values are integers and meet the specified minimum value condition.
    Parameters:
        workstations_count: Number of workstations (size of the matrix)
        minimum_value: Minimum acceptable value for the matrix entries
        variable: Name of the matrix (e.g., 'distance', 'flow')
        variable2: Descriptive term (e.g., 'workstation', 'facility')
    Returns:
        A symmetric matrix where diagonal elements are 0 and values are user-provided.
    """
    matrix = []  # Initialize the matrix
    for i in range(workstations_count):
        temporary_array = []  # Temporary row for the matrix
        for j in range(workstations_count):
            if i == j:
                temporary_array.append(0)  # Diagonal values are always 0
                continue
            if j > i:
                # For upper triangular part of the matrix
                value_valid = False
                while not value_valid:
                    try:
                        value = int(input(f"Enter the {variable} between {variable2} {i + 1} and {j + 1}: "))
                        if value < minimum_value:
                            raise ValueError  # Value must meet the minimum condition
                        temporary_array.append(value)
                        value_valid = True  # Exit the loop on valid input
                    except ValueError:
                        print(f"The {variable} must be an integer and greater than {minimum_value - 1}.")
            else:
                # For lower triangular part, mirror the upper triangular values
                temporary_array.append(matrix[j][i])
        matrix.append(temporary_array)  # Add the completed row to the matrix
    return matrix

def calculate_partial_cost(partial_assignment, distance_matrix, flow_matrix):
    """
    Calculates the total cost of a partial facility assignment.
    The cost is computed as the product of distances between assigned locations
    and flows between assigned facilities.
    Parameters:
        partial_assignment: List of assigned facilities
        distance_matrix: Matrix of distances between workstations
        flow_matrix: Matrix of flows between facilities
    Returns:
        The total cost for the current partial assignment.
    """
    total_cost = 0
    for i in range(len(partial_assignment)):
        for j in range(i + 1, len(partial_assignment)):
            loc_i, loc_j = i, j
            fac_i, fac_j = partial_assignment[i], partial_assignment[j]
            # Add the cost for this pair of facilities
            total_cost += distance_matrix[loc_i][loc_j] * flow_matrix[fac_i - 1][fac_j - 1]
    return total_cost

def calculate_bound(partial_assignment, distance_matrix, flow_matrix, num_workstations):
    """
    Calculates the upper bound on the total cost for a given partial assignment.
    The bound includes:
    - The actual cost of the current partial assignment.
    - An estimated cost for unassigned facilities, based on the remaining flow matrix.
    Parameters:
        partial_assignment: List of currently assigned facilities
        distance_matrix: Matrix of distances between workstations
        flow_matrix: Matrix of flows between facilities
        num_workstations: Total number of workstations
    Returns:
        The upper bound on the total cost for the current partial assignment.
    """
    # Calculate the cost of the current partial assignment
    bound = calculate_partial_cost(partial_assignment, distance_matrix, flow_matrix)
    
    # Identify facilities that are not yet assigned
    unassigned = [i + 1 for i in range(num_workstations) if i + 1 not in partial_assignment]
    
    # Estimate the cost for unassigned facilities
    remaining_cost = 0
    for i in range(len(unassigned)):
        for j in range(i + 1, len(unassigned)):
            fac_i, fac_j = unassigned[i], unassigned[j]
            remaining_cost += flow_matrix[fac_i - 1][fac_j - 1]
    
    # Add the estimated cost of unassigned facilities to the bound
    bound += remaining_cost
    return bound

def branch_and_bound(distance_matrix, flow_matrix):
    """
    Solves the facility location optimization problem using the Branch and Bound algorithm.
    Parameters:
        distance_matrix: Matrix of distances between workstations
        flow_matrix: Matrix of flows between facilities
    Returns:
        The optimal arrangement of facilities and the associated total cost.
    """
    num_workstations = len(distance_matrix)  # Total number of workstations
    
    # Initialize the list of nodes with the root node
    nodes = []
    initial_assignment = []  # Start with no assignments
    remaining_facilities = list(range(1, num_workstations + 1))  # All facilities are unassigned initially
    
    # Calculate the bound for the root node
    initial_bound = calculate_bound(initial_assignment, distance_matrix, flow_matrix, num_workstations)
    nodes.append((initial_bound, 0, initial_assignment, remaining_facilities))
    
    best_cost = float('inf')  # Initialize the best cost to infinity
    best_arrangement = None  # Initialize the best arrangement
    
    while nodes:
        # Sort nodes by their bound and pop the one with the smallest bound
        nodes.sort(key=lambda x: x[0])  # Sort by bound
        bound, current_cost, current_assignment, remaining_facilities = nodes.pop(0)
        
        # Prune nodes whose bound exceeds the best known cost
        if bound >= best_cost:
            continue
        
        # If we have a complete assignment, update the best cost and arrangement
        if len(current_assignment) == num_workstations:
            if current_cost < best_cost:
                best_cost = current_cost
                best_arrangement = current_assignment
            continue
        
        # Branch to explore all remaining facilities
        for facility in remaining_facilities:
            next_assignment = current_assignment + [facility]  # Add this facility to the assignment
            next_remaining = [f for f in remaining_facilities if f != facility]  # Remaining facilities
            
            # Calculate the cost and bound for this branch
            partial_cost = calculate_partial_cost(next_assignment, distance_matrix, flow_matrix)
            bound = calculate_bound(next_assignment, distance_matrix, flow_matrix, num_workstations)
            
            # Only add the branch if it could potentially improve the solution
            if bound < best_cost:
                nodes.append((bound, partial_cost, next_assignment, next_remaining))
    
    print(f"The optimal arrangement is {best_arrangement}, with a total cost of {best_cost}")
    return best_arrangement, best_cost

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

# Solve the problem
branch_and_bound(distance_matrix, flow_matrix)
