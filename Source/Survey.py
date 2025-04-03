import os
import re

class Testcase:
    def __init__(self):
        self.testcase_files = []
        self.output_files = []

    def read_files(self, folder_name: str):
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # Get list of files
            files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
            # Sort with natural ordering
            self.testcase_files = sorted(files, key=lambda x: [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', x)])
        else:
            print(f"Folder '{folder_name}' does not exist.")
            self.testcase_files = []  # Added to ensure attribute is always set

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
