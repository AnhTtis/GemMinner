from Board import Board
from Tool import Tool_Library, Tool_bruce_force, Tool_backtracking
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
    tool.solve()
    sub_time_list.append(tool.get_time())
    file_path = f"{folder_output}/{test.output_files[i]}"
    tool.write_output(file_path)
test.clear_files()
time_list.append(sub_time_list)
sub_time_list = []
    
# Test the bruce force
test.read_files(folder_test)
test.generate_output_files("bruce_force")
for i in range(len(test.testcase_files)):
    file_path = f"{folder_test}/{test.testcase_files[i]}"
    board = Board(file_path)
    
    tool = Tool_bruce_force(board)
    tool.solve()
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
    
    tool = Tool_backtracking(board)
    tool.solve()
    sub_time_list.append(tool.get_time())
    file_path = f"{folder_output}/{test.output_files[i]}"
    tool.write_output(file_path)
test.clear_files()
time_list.append(sub_time_list)
sub_time_list = []

# Print the result
print("Order\t\tLibrary\t\t\tBruce Force\t\t\tBacktracking")
for i in range(len(order_list)):
    print(f"{order_list[i]}\t{time_list[0][i]}\t{time_list[1][i]}\t{time_list[2][i]}")
    