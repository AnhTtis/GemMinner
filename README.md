# GemMinner
A lab from Introduction in AI. This is an exercise on how to use CNF to solve a problem that is quite similar to Minesweeper.

## Annalyze the problem:

- The problem is quite similar to Minesweeper. It is first initialized with a grid NxN, in which some cells are marked with a number from 1 to 8 (show information about the number of traps surrounding that cell) and the goal is to fill the blank cell with whether letter 'T' (representing for Trap) or letter 'G' (representing for Gem).
- The purpose of the lab is using  [CNF (Conjunctive Normal Form)](https://en.wikipedia.org/wiki/Conjunctive_normal_form) to solve this problem. 
- In this lab, there are some main missions we have to achieve:
 + Mission 1: Convert the problem into CNF.
 + Mission 2: Using the **Pysat library** to solve the problem. You can read more about this library on this [link](https://pysathq.github.io/)
 + Mission 3: From the generated CNF, solving the problem by **Bruce-force**
 + Mission 4: From the generated CNF, solving the problem by **Backtracking**
 + Mission 5: Compare three methods using time excution while solving the problem.

## Solving each mission:

### Mutual properties:

- To solve the CNF, we have to decide the logic of each cell. In my solution, i will use the following logic: The cell is a **Trap** if its CNF value is **True** and a **Gem** if its CNF value is **False**.
- We will mark the blank cells with a number that increase from left to right and top to downn.

#### Mission 1: Creating the CNF

- Focus on the way the library store the CNF and solve it, we have to build a funcion with the following properties:
 + The function will takes a list of neighboring cells and a specified number of
traps. It generates two sets of combinations to form the CNF clauses. 
 + The first set ensures that at least the specified number of traps are present.This is done by generating combinations of a length that is one more than the difference between the total number of neighbors and the number of traps. Each combination in this set represents a scenario where at least one of the selected neighbors must be a trap.
 + The second set of combinations ensures that no more than the specified number of traps are present. This is achieved by generating combinations of a length that is one more than the number of traps. Each combination in this set represents a scenario where at least one of the selected neighbors must be a gem. 
 + By combining these two sets of combinations, the function creates a comprehensive set of CNF clauses that accurately represent the constraints for the number of traps in the neighboring cells. This approach ensures that the constraints are both necessary and sufficient for determining the presence of traps, providing a robust method for solving the Gem Miner problem.
- The generated CNF will help us limit the number of possible models (models can be a solution or not) and make the problem easier to solve.

#### Mission 2: Solving the problem with Pysat library

- The CNF will be as a 2-D list. It will first include a list of clauses and each clause will represent the constraints of variable related to each other.
- We wil take turn get the clause add to the **boot_strap** of the **solver** of PySat librar.
- Since it can have many models and i am not certain that it is the first model or not (even though it seems correct right the first one every time with this way of generating the CNF), we will have to check each model to see if it is a valid by using the function **enum_models()** and build a function **check_valid()** for the solution

#### Mission 3: Solving the problem by Bruce-force

- We will first use the list of all variable need to fill (and the list is created from the work we mark the blank cell with a positive integer) as a intial model as every cell is a **Trap**.
- We will then use the **itertools** library to get all combinations of gems amog the **Traps** above and check if the model is a correct solution or not.

#### Mission 4: Solving the problem by Backtracking

- We will initializes model as a list with zeros. 
- It then calls the backtrack method, starting from the first variable (index 0). The backtrack method recursively assigns each variable in the solution list to either a trap (positive value) or a gem (negative value). For each assignment, it checks if the current partial solution is valid by recursively calling itself with the next index.
- If the end of the solution list is reached (base case), it validates the entire solution against the CNF constraints. If a valid solution is found, it returns True, causing the recursion to unwind and ultimately updating the result in the solve method. If no valid solution is found, it returns False, and the algorithm continues exploring other configurations. 
- This backtracking approach ensures that all possible configurations are explored, the first valid solution is identified efficiently and the function will end directly after finding the first valid solution.

#### Mission 5: Compare three methods using time execution while solving the problem

- In this mission, we will use the **time** library to measure the time it takes to solve the problem
- We will have a variable to count time in each method for the comparing in the end