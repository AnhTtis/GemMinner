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
        self.name = ""
        self.result = []
        self.model = 1000000
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
    

    def write_output(self, file_path: str):
        """
        Writes the output to the specified file. If self.name is "library", it writes from the start.
        Otherwise, it appends to the file. The self.name is written with decoration "***" at the top.
        """
        # Determine the mode based on self.name
        mode = "w" if self.name == "library" else "a"

        with open(file_path, mode) as file:
            # Write the name with decoration at the beginning
            file.write(f"*** {self.name} ***\n")

            # No solution after 1000000 models
            if self.result == []:
                if self.board.board == []:
                    file.write("Board is empty\n")
                else:
                    file.write("No solution after 1000000 models\n")
                return

            # Write the results
            for r in self.result:
                file.write(", ".join(r) + "\n")
class Tool_Library(Tool):
    def solve(self):
        start_time = time.time()
        solver = Solver()
        self.name = "library"
        for clause in self.cnf:
            solver.add_clause(clause)
        
        for m in solver.enum_models():
            self.model -= 1
            model = m
            if self.check_valid(model):
                self.result = self.board.get_result()
                end_time = time.time()
                self.time = end_time - start_time
                return
            if self.model == 0:
                end_time = time.time()
                self.time = end_time - start_time
                return
        
        end_time = time.time()
        self.time = end_time - start_time
        
class Tool_Brute_Force(Tool):
    def solve(self):
        start_time = time.time()
        self.name = "brute_force"
        solution = deepcopy(self.list_var)
        
        for k in range(0, len(self.list_var)):
            for comb in combinations(self.list_var, k):
                self.model -= 1
                get_test = deepcopy(solution)
                for c in comb:
                    get_test[c-1] = -solution[c-1]
            
                if self.check_valid_solution(get_test, self.cnf):
                    self.result = self.board.get_result()
                    end_time = time.time()
                    self.time = end_time - start_time
                    return
                if (self.model == 0):
                    end_time = time.time()
                    self.time = end_time - start_time
                    return

        end_time = time.time()
        self.time = end_time - start_time

class Tool_Backtracking(Tool):
    def solve(self):
        start_time = time.time()
        self.name = "backtracking"
        solution = [0] * len(self.list_var)
        if self.backtrack(solution, 0) == True:
            self.result = self.board.get_result()
        
        end_time = time.time()
        self.time = end_time - start_time

    def backtrack(self, solution: list[int], index: int) -> bool:
        if self.model == 0:
            return False
    
        if index == len(solution):
            self.model -= 1
            return self.check_valid_solution(solution, self.cnf)
        
        for value in [self.list_var[index], -self.list_var[index]]:
            solution[index] = value
            if self.backtrack(solution, index + 1):
                return True
        return False