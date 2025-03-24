
import os
import sys
from copy import deepcopy
from itertools import combinations
from pysat.solvers import Solver

def handle_line(get_line: str) -> list[str]:
    tokens = []
    token = ""
    length = len(get_line)
    for get_token in get_line:
        length -= 1
        if get_token == ',' or length == 0:
            if get_token == get_line[-1] and get_line[-1] <= '9' and get_line[-1] >= '0':
                token += get_line[-1]
            tokens.append(token)
            token = ""
                
        if get_token <= '9' and get_token >= '0':
            token += get_token

    return tokens

def handle_file(file_path:str) -> list[list[str]]:
    data = []
    with open(file_path, "r") as file:
        for f in file:
            data.append(handle_line(f))
    return data

def write_output(file_path:str, result: list[list[str]]):
    if not result:
        with open(file_path, "w") as file:
            file.write("No solution")
        return
    with open(file_path, "w") as file:
        for r in result:
            file.write(", ".join(r) + "\n")
            
# Build a dictionary of variables Tuple(i, j) -> variable number and return it
def assign_variables(grid: list[list[str]]) -> dict[tuple[int, int], int]:
    variables = {}
    var_num = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "":
                variables[(i, j)] = var_num
                var_num += 1
    return variables

def get_pos(variables: dict[tuple[int, int], int], var: int) -> tuple[int, int]:
    for pos, val in variables.items():
        if val == var:
            return pos
    return None

def get_neighbors(num_row: int, num_col: int, grid: list[list[str]], variables: dict[tuple[int, int], int]) -> list[int]:
    rows = len(grid)
    cols = len(grid[0])
    
    neighbors = []
    # Get legal 8 neighbors around the cell
    for i in range(max(0, num_row-1), min(rows, num_row+2)):
        for j in range(max(0, num_col-1), min(cols, num_col+2)):
            if (i, j) != (num_row, num_col):
                
                if grid[i][j] == "":
                    neighbors.append(variables[(i, j)])
                    
    return neighbors

def generate_cnf(vars: list[int], k: int) -> list[list[int]]:
    cnf = []
    # At least k variables are true
    pos = 0
    get_vars = []
    
    for i in range(len(vars)):
        get_vars.append(pos)
        pos += 1
        
    for comb in combinations(get_vars, k):
        get_cnf = vars.copy()
        for i in range(k):
            get_cnf[comb[i]] = - vars[comb[i]]
        cnf.append(get_cnf)
    
    return cnf

def solve_cnf(cnf: list[list[int]], var: dict[tuple[int, int], int]) -> list[int]:
    print("Get here")
    solver = Solver()
    get: list[list[int]]  = []
    for clause in cnf:
        sub_solver = Solver()
        for sub_clause in clause:
            sub_solver.add_clause(sub_clause)
        if sub_solver.solve():
            for m in sub_solver.enum_models():
                print(m)
                get.append(m)
                solver.add_clause(m)
        sub_solver.delete()
    
    print(get)
    if solver.solve():
        return solver.get_model()

    return None

def check_solution(solution: list[int], variables: dict[tuple[int, int], int], grid: list[list[str]]) -> bool:
    data = interpret_solution(solution, variables, grid)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isdigit():
                num_traps = int(grid[i][j])
                neighbors = get_neighbors(i, j, grid, variables)
                
                # Count the number of traps around the cell
                num_traps_around = 0
                for neighbor in neighbors:
                    pos = get_pos(variables, neighbor)
                    grid_i = pos[0]
                    grid_j = pos[1]
                    if data[grid_i][grid_j] == 'T':
                        num_traps_around += 1
                if num_traps_around != num_traps:
                    return False
    
    return True
                    


def interpret_solution(solution: list[int], variables: dict[tuple[int, int], int], grid: list[list[str]]) -> list[list[str]]:
    result_grid = deepcopy(grid)
    for (i, j), var in variables.items():
        if var in solution and var > 0:
            result_grid[i][j] = 'G'
        else:
            result_grid[i][j] = 'T'
    
    return result_grid

def using_library(grid: list[list[str]]) -> list[list[str]]:
    variables: dict[tuple[int, int], int] = assign_variables(grid)
    print(variables)
    constraints: list[list[int]] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isdigit():
                num_traps = int(grid[i][j])
                neighbors = get_neighbors(i, j, grid, variables)
                constraints.append(generate_cnf(neighbors, num_traps))
             
    solution: list[int] = solve_cnf(constraints, variables)
    print(solution)
    if solution:
        return interpret_solution(solution, variables, grid)
    else:
        return None

# Bruce force by trying every possible situations without using the library
def is_lack_traps(grid: list[list[str]], data:list[list[str]],variables: dict[tuple[int, int], int]) -> bool:
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isdigit():
                num_traps = int(grid[i][j])
                neighbors = get_neighbors(i, j, grid, variables)
                
                # Count the number of traps around the cell
                num_traps_around = 0
                for neighbor in neighbors:
                    pos = get_pos(variables, neighbor)
                    grid_i = pos[0]
                    grid_j = pos[1]
                    if data[grid_i][grid_j] == 'T':
                        num_traps_around += 1
            
                if num_traps_around < num_traps:
                    return False
    return True

def bruce_force(grid: list[list[str]]) -> list[list[str]]:
    variables: dict[tuple[int, int], int] = assign_variables(grid)

    
    # Assign all blank with T
    data = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "":
                data[i][j] = "T"
    
    # Sign each one with gem and see if it is a valid solution
    for (i, j), var in variables.items():
        data[i][j] = "G"
        if not is_lack_traps(grid, data, variables):
            data[i][j] = "T"
    data = [["T", "T", "T", "T", "T", "3", "T", "3", "T", "T", "T", "T", "2", "G", "G", "3", "3", "T", "2", "T"],
["G", "5", "T", "6", "4", "T", "5", "T", "6", "T", "T", "4", "T", "3", "T", "T", "T", "3", "T", "2"],
["2", "4", "T", "4", "T", "3", "T", "T", "7", "T", "G", "3", "G", "T", "5", "T", "4", "T", "4", "G"],
["T", "T", "3", "T", "T", "3", "4", "T", "T", "T", "T", "2", "1", "G", "T", "5", "T", "4", "T", "T"],
["3", "5", "G", "6", "T", "3", "4", "T", "6", "6", "T", "G", "1", "4", "T", "6", "T", "T", "4", "2"],
["T", "T", "T", "T", "T", "4", "T", "T", "T", "4", "T", "4", "T", "5", "T", "T", "5", "T", "3", "G"],
["4", "6", "G", "T", "4", "G", "T", "8", "T", "G", "5", "T", "5", "T", "T", "G", "4", "T", "G", "1"],
["T", "T", "T", "4", "T", "4", "T", "T", "T", "T", "T", "T", "4", "T", "4", "T", "3", "3", "T", "2"],
["4", "T", "5", "T", "3", "T", "4", "5", "T", "6", "T", "5", "G", "3", "G", "5", "T", "G", "3", "T"],
["T", "4", "T", "4", "G", "4", "T", "3", "G", "4", "T", "T", "4", "T", "T", "T", "T", "4", "T", "2"],
["G", "5", "T", "G", "T", "4", "T", "3", "2", "T", "G", "5", "T", "T", "8", "T", "6", "T", "3", "G"],
["T", "4", "T", "4", "T", "4", "4", "T", "4", "3", "T", "T", "5", "T", "T", "T", "5", "T", "4", "1"],
["3", "T", "4", "3", "4", "T", "4", "T", "3", "T", "5", "T", "G", "3", "4", "G", "4", "T", "T", "G"],
["2", "T", "G", "T", "3", "T", "4", "3", "G", "2", "3", "T", "4", "T", "2", "2", "T", "3", "3", "2"],
["2", "3", "T", "4", "4", "3", "T", "3", "T", "2", "G", "2", "4", "T", "G", "4", "T", "4", "3", "T"],
["3", "T", "5", "T", "T", "4", "G", "T", "4", "T", "3", "3", "T", "3", "3", "T", "T", "G", "T", "T"],
["T", "T", "T", "5", "T", "4", "T", "3", "T", "4", "T", "T", "3", "G", "T", "4", "4", "T", "3", "2"],
["4", "6", "5", "T", "4", "T", "4", "G", "4", "T", "4", "G", "3", "T", "3", "3", "T", "4", "G", "2"],
["T", "T", "T", "4", "T", "T", "4", "T", "4", "T", "G", "2", "T", "3", "T", "G", "3", "T", "T", "T"],
["3", "T", "T", "G", "2", "2", "T", "2", "3", "T", "3", "T", "2", "G", "1", "2", "T", "3", "G", "2"]]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isdigit():
                num_traps = int(grid[i][j])
                neighbors = get_neighbors(i, j, grid, variables)
                
                # Count the number of traps around the cell
                num_traps_around = 0
                for neighbor in neighbors:
                    pos = get_pos(variables, neighbor)
                    grid_i = pos[0]
                    grid_j = pos[1]
                    if data[grid_i][grid_j] == 'T':
                        num_traps_around += 1
            
                if num_traps_around != num_traps:
                    print("wrong at", i, j)
                    print(num_traps_around, num_traps)
    return data

# Backtracking developed from bruce force
def is_valid_configuration(grid, data, variables):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].isdigit():
                num_traps = int(grid[i][j])
                neighbors = get_neighbors(i, j, grid, variables)
                num_traps_around = 0
                for neighbor in neighbors:
                    pos = get_pos(variables, neighbor)
                    grid_i, grid_j = pos
                    if data[grid_i][grid_j] == 'T':
                        num_traps_around += 1
                if num_traps_around != num_traps:
                    return False
    return True

def recursive_solve(grid, data, variables, index):
    if index == len(variables):
        if is_valid_configuration(grid, data, variables):
            return deepcopy(data)
        return None

    (i, j), var = list(variables.items())[index]
    if grid[i][j].isdigit():
        return recursive_solve(grid, data, variables, index + 1)

    # Try placing a trap
    data[i][j] = 'T'
    result = recursive_solve(grid, data, variables, index + 1)
    if result:
        return result

    # Try placing a gem
    data[i][j] = 'G'
    result = recursive_solve(grid, data, variables, index + 1)
    if result:
        return result

    # Reset the cell and backtrack
    data[i][j] = ''
    return None

def backtracking(grid: list[list[str]]) -> list[list[str]]:
    variables: dict[tuple[int, int], int] = assign_variables(grid)
    data = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '':
                data[i][j] = 'T'
    return recursive_solve(grid, data, variables, 0)

def check_valid_clause(clause:list[int], solution: list[int]) -> bool:
    for c in clause:
        get_compare = solution[abs(c)-1]
        if (c == get_compare):
            return True
    return False

def check_valid_solution(solution: list[int], cnf: list[list[int]]) -> bool:
    for clause in cnf:
        if not check_valid_clause(clause, solution):
            return False
    return True

def solve_CNF_bruce_force(cnf: list[list[int]], var: list[int]) -> list[int]:
    solution = deepcopy(var)
    for i in range(len(solution)):
        solution[i] = solution[i] * (-1)
        
    for k in range(1, len(var)+1):
        for comb in combinations(var, k):
            get_test = deepcopy(solution)
            for c in comb:
                get_test[c-1] = -solution[c-1]
            
            if check_valid_solution(get_test, cnf):
                return get_test
            
    return None    

def backtrack(cnf: list[list[int]], solution: list[int], index: int) -> bool:
    if index == len(solution):
        return check_valid_solution(solution, cnf)
    
    # Try assigning the positive value to the current variable
    solution[index] = index + 1
    if backtrack(cnf, solution, index + 1):
        return True
    
    # Try assigning the negative value to the current variable
    solution[index] = -(index + 1)
    if backtrack(cnf, solution, index + 1):
        return True
    
    # If neither assignment works, backtrack
    return False

def solve_CNF_backtracking(cnf: list[list[int]], var: list[int]) -> list[int]:
    solution = [0] * len(var)
    if backtrack(cnf, solution, 0):
        return solution
    return None

cnf = [[-1, -2, -3, -4], [-1, -2, 3, -4], [-1, -2, 3, 4], [1, -2, 3, -4], [1, 2, 3, -4], [1, 2, -3, -4], [-1, 2, -3, -4], [-1, 2, -3, 4], [-1, -2, -3, 4], [1, -2, -3, 4], [1, -2, -3, -4], [1, 2, -3, 4], [-1, 2, 3, 4], [-1, 2, 3, -4], [-1, -2, -3, -4, -5], [-1, -2, 3, -4, -5], [-1, -2, 3, 4, -5], [1, -2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, -3, 4, 5], [1, 2, -3, -4, 5], [1, 2, -3, 4, -5], [-1, 2, -3, 4, 5], [1, -2, -3, 4, 5], [1, 2, 3, -4, 5], [1, 2, 3, 4, -5], [-1, 2, 3, 4, 5], [-1, -2, 3, -4, 5], [-1, -2, -3, -4, 5], [-1, -2, -3, 4, -5], [-1, 2, 3, -4, -5], [-1, 2, -3, -4, -5], [1, -2, -3, -4, -5], [1, -2, 3, -4, -5], [-1, -2, -3, -4, -5, -6, -7], [-1, -2, 3, -4, -5, -6, -7], [-1, -2, 3, 4, -5, -6, -7], [-1, -2, 3, 4, -5, 6, -7], [-1, -2, 3, 4, 5, 6, 7], [-1, -2, 3, 4, 5, -6, 7], [-1, -2, -3, 4, 5, -6, 7], [-1, -2, -3, 4, 5, 6, 7], [-1, -2, -3, 4, -5, 6, -7], [-1, -2, -3, 4, -5, -6, -7], [-1, -2, -3, -4, 5, -6, -7], [-1, -2, -3, -4, 5, 6, -7], [-1, -2, 3, -4, 5, 6, -7], [-1, -2, 3, -4, 5, -6, -7], [-1, -2, 3, -4, -5, -6, 7], [-1, -2, -3, -4, -5, -6, 7], [-1, -2, -3, -4, -5, 6, 7], [-1, -2, -3, -4, -5, 6, -7], [-1, -2, 3, -4, -5, 6, -7], [-1, -2, 3, -4, -5, 6, 7], [1, -2, -3, -4, -5, 6, -7], [1, -2, -3, -4, -5, -6, -7], [1, -2, 3, -4, -5, -6, -7], [1, -2, 3, -4, -5, 6, -7], [1, 2, -3, -4, -5, 6, 7], [1, 2, -3, -4, -5, -6, 7], [-1, 2, -3, -4, -5, -6, -7], [-1, 2, -3, -4, -5, 6, -7], [1, 2, 3, -4, -5, 6, 7], [1, 2, 3, -4, -5, -6, 7], [-1, 2, 3, -4, -5, -6, -7], [-1, 2, 3, -4, -5, 6, -7], [1, 2, 3, -4, 5, 6, 7], [1, 2, -3, -4, 5, 6, 7], [1, 2, -3, -4, 5, -6, 7], [1, 2, -3, -4, 5, -6, -7], [1, 2, 3, -4, 5, -6, -7], [1, 2, 3, -4, 5, 6, -7], [1, 2, -3, -4, 5, 6, -7], [1, 2, 3, 4, 5, -6, -7], [1, 2, -3, 4, 5, -6, -7], [1, 2, -3, 4, 5, -6, 7], [1, 2, -3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, -7], [1, 2, -3, 4, 5, 6, -7], [1, 2, 3, 4, -5, 6, 7], [1, 2, -3, 4, -5, 6, 7], [1, 2, -3, 4, -5, -6, 7], [1, 2, -3, 4, -5, -6, -7], [1, 2, 3, 4, -5, -6, -7], [1, 2, 3, 4, -5, 6, -7], [1, 2, -3, 4, -5, 6, -7], [-1, 2, 3, 4, 5, -6, -7], [-1, 2, 3, 4, 5, -6, 7], [-1, 2, 3, 4, 5, 6, -7], [1, -2, 3, 4, 5, 6, -7], [1, -2, 3, 4, 5, 6, 7], [1, -2, 3, 4, 5, -6, -7], [1, -2, -3, 4, 5, -6, -7], [1, -2, -3, 4, 5, 6, -7], [1, -2, -3, 4, 5, 6, 7], [1, -2, -3, 4, 5, -6, 7], [1, -2, 3, 4, 5, -6, 7], [1, 2, 3, 4, 5, -6, 7], [1, 2, 3, 4, -5, -6, 7], [1, -2, 3, 4, -5, -6, 7], [1, -2, 3, 4, -5, 6, 7], [1, -2, -3, 4, -5, 6, 7], [1, -2, -3, 4, -5, -6, 7], [1, -2, -3, -4, 5, 6, 7], [1, -2, -3, -4, 5, -6, 7], [1, -2, 3, -4, 5, -6, 7], [1, -2, 3, -4, 5, 6, 7], [1, 2, 3, -4, 5, -6, 7], [-1, 2, -3, -4, 5, 6, 7], [-1, 2, -3, -4, 5, -6, 7], [-1, 2, 3, -4, 5, -6, 7], [-1, 2, 3, -4, 5, 6, 7], [-1, 2, -3, 4, 5, -6, -7], [-1, 2, -3, 4, 5, 6, -7], [-1, 2, -3, 4, 5, -6, 7], [-1, 2, -3, 4, 5, 6, 7], [-1, 2, 3, 4, 5, 6, 7], [-1, 2, -3, 4, -5, 6, 7], [-1, 2, -3, 4, -5, -6, 7], [-1, 2, 3, 4, -5, -6, 7], [-1, 2, 3, 4, -5, 6, 7], [-1, -2, -3, -4, -5, -6], [-1, -2, 3, -4, -5, -6], [-1, -2, 3, 4, -5, -6], [-1, -2, 3, 4, 5, -6], [1, -2, 3, 4, 5, -6], [1, 2, 3, 4, 5, -6], [1, 2, -3, 4, 5, -6], [1, 2, -3, -4, 5, -6], [-1, 2, -3, -4, 5, -6], [-1, 2, -3, -4, -5, -6], [-1, -2, -3, -4, 5, -6], [-1, -2, -3, -4, 5, 6], [-1, -2, 3, -4, 5, 6], [-1, -2, -3, 4, 5, 6], [1, -2, -3, 4, 5, 6], [1, -2, -3, 4, -5, 6], [1, 2, -3, 4, -5, 6], [1, 2, -3, 4, -5, -6], [1, 2, 3, 4, -5, -6], [1, 2, 3, -4, -5, -6], [-1, 2, 3, 4, -5, -6], [-1, 2, 3, 4, 5, -6], [-1, 2, -3, 4, 5, -6], [-1, -2, -3, 4, 5, -6], [-1, -2, -3, 4, -5, -6], [1, -2, 3, -4, -5, -6], [1, -2, -3, -4, -5, -6], [1, -2, -3, -4, -5, 6], [1, 2, -3, -4, -5, 6], [1, 2, -3, -4, 5, 6], [1, 2, -3, 4, 5, 6], [1, 2, 3, -4, 5, 6], [-1, 2, 3, -4, 5, 6], [-1, 2, 3, -4, 5, -6], [-1, -2, 3, -4, 5, -6], [-1, 2, 3, -4, -5, -6], [-1, 2, -3, 4, -5, -6], [1, 2, -3, -4, -5, -6], [1, 2, 3, -4, -5, 6], [1, -2, 3, -4, -5, 6], [1, -2, 3, -4, 5, 6], [1, -2, -3, -4, 5, 6], [-1, -2, -3, 4, -5, 6], [1, -2, -3, 4, -5, -6], [1, -2, -3, 4, 5, -6], [1, 2, 3, -4, 5, -6], [-1, 2, -3, -4, 5, 6], [-1, 2, -3, 4, 5, 6], [-1, 2, -3, 4, -5, 6], [-1, -2, -3, -4, -5, 6], [-1, -2, 3, -4, -5, 6], [-1, 2, 3, -4, -5, 6], [1, -2, 3, 4, -5, -6], [1, -2, 3, -4, 5, -6], [1, -2, -3, -4, 5, -6], [-1, 2, -3, -4, -5, 6], [-1, -2, -3, -4, -5, -6, -7], [-1, -2, 3, -4, -5, -6, -7], [-1, -2, 3, 4, 5, -6, -7], [-1, -2, 3, 4, 5, 6, -7], [-1, -2, 3, 4, 5, 6, 7], [-1, -2, 3, -4, 5, 6, 7], [-1, -2, 3, -4, 5, -6, 7], [-1, -2, -3, -4, 5, -6, 7], [-1, -2, -3, 4, 5, -6, 7], [-1, -2, -3, 4, 5, 6, 7], [-1, -2, -3, -4, 5, 6, 7], [-1, -2, -3, 4, -5, -6, 7], [-1, -2, 3, 4, -5, -6, 7], [1, -2, 3, 4, -5, -6, 7], [1, -2, 3, 4, -5, 6, 7], [1, -2, -3, 4, -5, 6, 7], [-1, -2, -3, 4, -5, 6, 7], [-1, -2, 3, 4, -5, 6, 7], [1, -2, -3, 4, 5, 6, 7], [1, -2, -3, 4, 5, 6, -7], [1, -2, -3, 4, 5, -6, -7], [-1, -2, -3, 4, 5, -6, -7], [-1, -2, -3, 4, 5, 6, -7], [-1, -2, -3, -4, -5, 6, -7], [-1, 2, -3, -4, -5, -6, -7], [1, -2, -3, -4, -5, -6, -7], [1, -2, -3, -4, -5, 6, -7], [-1, 2, -3, -4, -5, 6, -7], [-1, 2, -3, 4, 5, 6, -7], [-1, 2, -3, 4, 5, -6, -7], [1, 2, -3, 4, 5, -6, -7], [1, 2, -3, 4, 5, 6, -7], [1, 2, -3, -4, -5, -6, -7], [1, 2, -3, 4, -5, -6, 7], [1, -2, -3, 4, -5, -6, 7], [1, -2, -3, 4, 5, -6, 7], [1, 2, -3, 4, 5, 6, 7], [1, -2, -3, -4, 5, 6, 7], [1, -2, -3, -4, 5, -6, 7], [1, -2, 3, -4, 5, -6, 7], [1, 2, 3, -4, 5, -6, 7], [1, 2, 3, -4, 5, 6, 7], [1, 2, -3, -4, 5, 6, 7], [1, 2, -3, -4, 5, -6, 7], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, -5, 6, 7], [1, 2, -3, 4, -5, 6, 7], [-1, 2, -3, 4, -5, 6, 7], [-1, 2, -3, 4, 5, 6, 7], [-1, 2, 3, 4, 5, 6, 7], [-1, 2, 3, 4, -5, 6, 7], [-1, 2, -3, 4, 5, -6, 7], [-1, 2, -3, 4, -5, -6, 7], [1, 2, 3, 4, -5, -6, 7], [1, 2, 3, 4, 5, -6, 7], [-1, 2, 3, 4, -5, -6, 7], [1, 2, -3, -4, -5, 6, -7], [1, 2, 3, -4, -5, 6, -7], [1, -2, 3, -4, -5, 6, -7], [-1, 2, 3, -4, -5, 6, -7], [-1, 2, 3, 4, 5, 6, -7], [-1, 2, 3, 4, 5, -6, -7], [1, 2, 3, 4, 5, -6, -7], [1, -2, 3, 4, 5, -6, -7], [1, -2, 3, 4, 5, 6, -7], [1, -2, 3, -4, 5, 6, 7], [-1, 2, 3, -4, 5, 6, 7], [-1, 2, -3, -4, 5, 6, 7], [-1, 2, -3, -4, 5, -6, 7], [-1, 2, 3, -4, 5, -6, 7], [1, -2, 3, -4, -5, -6, -7], [-1, -2, 3, -4, -5, 6, -7], [-1, 2, 3, -4, -5, -6, -7], [1, 2, 3, -4, -5, -6, -7], [1, 2, 3, 4, 5, 6, -7], [1, 2, -3, 4, 5, -6, 7], [1, -2, 3, 4, 5, 6, 7], [1, -2, 3, 4, 5, -6, 7], [-1, -2, 3, 4, 5, -6, 7], [-1, 2, 3, 4, 5, -6, 7]]

data = handle_file("Testcase/Testcase6.txt")
result = bruce_force(data)
write_output("output_5.txt", result)
