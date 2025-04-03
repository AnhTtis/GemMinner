import os
import sys
from copy import deepcopy
from itertools import combinations
from pysat.solvers import Solver

class Board:
    def __init__(self, file_path: str):
        self.board = self.handle_file(file_path)
        if (self.board == []):
            self.rows = 0
            self.columns = 0
        else:
            self.rows = len(self.board)
            self.columns = len(self.board[0])
        self.list_var = []
        self.dict_var = self.assign_variables()
        self.result = []
      
    
    def handle_line(self, get_line: str) -> list[str]:
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

        
    def handle_file(self, file_path:str) -> list[list[str]]:
        data = []
        with open(file_path, "r") as file:
            for f in file:
                data.append(self.handle_line(f))
        return data
    
    def assign_variables(self) -> dict[tuple[int, int], int]:
        variables = {}
        var_num = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):   
                if self.board[i][j] == "":
                    variables[(i, j)] = var_num
                    self.list_var.append(var_num)
                    var_num += 1
                    
        return variables
    
    def get_pos(self, var:int) -> tuple[int, int]:
        for pos, val in self.dict_var.items():
            if val == var:
                return pos
        return None
    
    def get_neighbors(self, num_row: int, num_col: int) -> list[int]:
        rows = len(self.board)
        cols = len(self.board[0])
    
        neighbors = []

        # Get legal 8 neighbors around the cell
        for i in range(max(0, num_row-1), min(rows, num_row+2)):
            for j in range(max(0, num_col-1), min(cols, num_col+2)):
                if (i, j) != (num_row, num_col):
                    if self.board[i][j] == "":
                        neighbors.append(self.dict_var[(i, j)])
                    
        return neighbors
    
    def generate_cnf(self, vars: list[int], k: int) -> list[list[int]]:
        cnf = []
        if (len(vars) < k):
            return cnf
        # Generate all possible combinations of k variables
        for comb in combinations(vars, len(vars) - k + 1):
            cnf.append([v for v in comb])
        
        if (k < len(vars)):
            for comb in combinations(vars, k + 1):
                cnf.append([-v for v in comb])
        
        return cnf
        
    def get_cnf(self):
        cnf = []
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j].isdigit():
                    sub_cnf = []
                    num_traps = int(self.board[i][j])
                    neighbors = self.get_neighbors(i, j)
                    sub_cnf = self.generate_cnf(neighbors, num_traps)
                    
                    if sub_cnf != []:
                        cnf.extend(sub_cnf)
                    
                    sub_cnf.clear()
                    neighbors.clear()
        # Remove duplicate clauses
        unique_cnf = [list(clause) for clause in set(tuple(sorted(clause)) for clause in cnf)]

        return unique_cnf
    
    def transform_model(self, model: list[int]):
        self.result = deepcopy(self.board)
        for var in model:
            pos = self.get_pos(abs(var))
            if pos:
                if var > 0:
                    self.result[pos[0]][pos[1]] = "T"
                else:
                    self.result[pos[0]][pos[1]] = "G"
    
    def check_valid(self) -> bool:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.result[i][j].isdigit():
                    num_traps = int(self.result[i][j])
                    neighbors = self.get_neighbors(i, j)
                    num_traps_around = 0
                    for neighbor in neighbors:
                        pos = self.get_pos(neighbor)
                        grid_i, grid_j = pos
                        if self.result[grid_i][grid_j] == 'T':
                            num_traps_around += 1
                    if num_traps_around != num_traps:
                        return False
                    neighbors.clear()
        return True

    
    def get_result(self) -> list[list[str]]:
        return self.result
    
    def get_list_var(self) -> list[int]:
        return self.list_var
    
    def print_board(self):
        for i in range(self.rows):
            print(self.board[i])