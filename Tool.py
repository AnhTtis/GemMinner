from Board import Board
from pysat.solvers import Solver
from itertools import combinations
from copy import deepcopy
import time
class Tool:
    def __init__(self, board: 'Board'):
        self.board = board
        self.cnf = board.get_cnf()
        self.list_var = board.get_list_var()
        self.time = 0
        self.found_solution = False
        self.result = []
        self.model = 0
        self.solve()

    
    def check_valid_clause(self, clause:list[int], solution: list[int]) -> bool:
        for c in clause:
            get_compare = solution[abs(c)-1]
            if (c == get_compare):
                return True
        return False

    def check_valid_solution(self, solution: list[int], cnf: list[list[int]]) -> bool:
        for clause in cnf:
            if not self.check_valid_clause(clause, solution):
                return False
        if not (self.check_valid(solution)):
            return False
        
        return True
                
    def check_valid(self, model: list[int]) -> bool:
        self.board.transform_model(model)
        return self.board.check_valid()

    def solve(self):
        pass
    
    def get_time(self):
        return self.time
    

    def write_output(self, file_path:str):
        if not self.result:
            with open(file_path, "w") as file:
                file.write("No solution")
            return
        with open(file_path, "w") as file:
            for r in self.result:
                file.write(", ".join(r) + "\n")
    
class Tool_Library(Tool):
    def solve(self):
        start_time = time.time()
        solver = Solver(name = "g4")
        for clause in self.cnf:
            solver.add_clause(clause)
        
        for m in solver.enum_models(): 
            self.model += 1
            model = m
            if self.check_valid(model):
                self.result = self.board.get_result()
                end_time = time.time()
                self.time = end_time - start_time
                return
            print(f"Model {self.model} is not valid")
        end_time = time.time()
        self.time = end_time - start_time

class Tool_bruce_force(Tool):
    def solve(self):
        start_time = time.time()
        solution = deepcopy(self.list_var)
        
        for k in range(0, len(self.list_var)):
            for comb in combinations(self.list_var, k):
                get_test = deepcopy(solution)
                for c in comb:
                    get_test[c-1] = -solution[c-1]
            
                if self.check_valid_solution(get_test, self.cnf):
                    self.result = self.board.get_result()
                    end_time = time.time()
                    self.time = end_time - start_time
                    return 
                
        end_time = time.time()
        self.time = end_time - start_time

class Tool_backtracking(Tool):
    def solve(self):
        start_time = time.time()
        solution = [0] * len(self.list_var)
        if self.backtrack(solution, 0):
            self.result = self.board.get_result()
        end_time = time.time()
        self.time = end_time - start_time

    def backtrack(self, solution: list[int], index: int) -> bool:
        if index == len(solution):
            return self.check_valid_solution(solution, self.cnf)
        
        for value in [self.list_var[index], -self.list_var[index]]:
            solution[index] = value
            if self.backtrack(solution, index + 1):
                return True
        return False