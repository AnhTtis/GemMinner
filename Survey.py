import os

class Testcase:
    def __init__(self):
        self.testcase_files = []
        self.output_files = []


    def read_files(self, folder_name: str):
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            self.testcase_files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
        else:
            print(f"Folder '{folder_name}' does not exist.")

    def generate_output_files(self, method: str):
        for file in self.testcase_files:
            if file.endswith(".txt"):
                base_name = file[:-len(".txt")]
                self.output_files.append(f"{base_name}_output_{method}.txt")
                
    def clear_files(self):
        if (self.testcase_files):
            self.testcase_files.clear()
        self.testcase_files = []
        if (self.output_files):
            self.output_files.clear()
        self.output_files = []
