import os
import logging

logging.basicConfig(level=logging.INFO)
test_case_folder = "test_cases\\input"


# handle input for printing all translated test cases to console
def print_out_all_console():
    test_case_files = []
    for i in get_test_case_count():
        file_path = test_case_folder + "/" + i
        with open(file_path, "r") as f:
            file = parse_file(f)
            test_case_files.append(file)

    logging.info(test_case_files)
    return test_case_files


# handle input for printing the translation for a selected test case (for GUI)
def single_file(test_case_file_path):
    with open(test_case_file_path, "r") as f:
        file = parse_file(f)

    return file


# parses and returns a clean consistent format of a file
def parse_file(file):
    line_list = []
    lines = file.readlines()
    for line in lines:
        if line.strip() != "":
            if line == "" or line == None:
                continue
            else:
                sanitize = line.rstrip()
                sanitize = sanitize.replace("\t", "")
                if sanitize[-1] == ";":
                    sanitize = sanitize[:-1]
                sanitize = sanitize.strip()
                line_list.append(sanitize)

    return line_list


# Gets number of test cases in test_cases folder
def get_test_case_count():
    list = os.listdir(test_case_folder)
    return list


