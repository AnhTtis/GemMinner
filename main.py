from Board import Board
from Tool import Tool_Library, Tool_Brute_Force, Tool_Backtracking
from Survey import Testcase

test = Testcase()

folder_test = "Testcase"
folder_output = "Result"

order_list = []
time_list = []
sub_time_list = []

# Test the library
test.read_files(folder_test)
test.generate_output_files("library")
for i in range(len(test.testcase_files)):
    order_list.append(test.testcase_files[i])    
    file_path = f"{folder_test}/{test.testcase_files[i]}"
    board = Board(file_path)
    tool = Tool_Library(board)
    sub_time_list.append(tool.get_time())
    file_path = f"{folder_output}/{test.output_files[i]}"
    tool.write_output(file_path)
test.clear_files()
time_list.append(sub_time_list)
sub_time_list = []
    
# Test the bruce force
test.read_files(folder_test)
test.generate_output_files("brute_force")
for i in range(len(test.testcase_files)):    
    file_path = f"{folder_test}/{test.testcase_files[i]}"
    board = Board(file_path)
    tool = Tool_Brute_Force(board)
    sub_time_list.append(tool.get_time())
    file_path = f"{folder_output}/{test.output_files[i]}"
    tool.write_output(file_path)
test.clear_files()
time_list.append(sub_time_list)
sub_time_list = []

# Test the backtracking
test.read_files(folder_test)
test.generate_output_files("backtracking")
for i in range(len(test.testcase_files)):
    file_path = f"{folder_test}/{test.testcase_files[i]}"
    board = Board(file_path)
    tool = Tool_Backtracking(board)
    sub_time_list.append(tool.get_time())
    file_path = f"{folder_output}/{test.output_files[i]}"
    tool.write_output(file_path)
test.clear_files()
time_list.append(sub_time_list)
sub_time_list = []

# Print the result with formatted columns and units
print(f"{'Order':<15} {'Library (s)':<15} {'Bruce Force (s)':<15} {'Backtracking (s)':<15}")
print("-" * 60)  # Separator line
for i in range(len(order_list)):
    print(f"{order_list[i]:<15} "
          f"{time_list[0][i]:<15.6f} "
          f"{time_list[1][i]:<15.6f} "
          f"{time_list[2][i]:<15.6f}")