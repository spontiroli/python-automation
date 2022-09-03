#!/usr/bin/env python3
import csv

def read_employees(csv_file_location):
    with open(csv_file_location, "r") as f:
        csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
        employee_dict = csv.DictReader(f, dialect = 'empDialect')
        employee_list = []
        for employee in employee_dict:
            employee_list.append(employee)
    return employee_list

def process_data(employee_list):
    department_list = []
    # get all departments from the employee list
    for employee_data in employee_list:
        department_list.append(employee_data['Department'])

    # let's build a department data dictiornary without redundant values
    # we will have department name:number of employees in that department
    department_data = {}
    for department_name in set(department_list):
        department_data[department_name] = department_list.count(department_name)
    return department_data

def write_report(dictionary, report_file):
    # w+ for writing and reading
    with open(report_file, "w+") as f:
        for entry in sorted(dictionary):
            f.write(str(entry) + ':' + str(dictionary[entry]) + '\n')



employee_list = read_employees("/home/student-03-c4854d3cc119/data/employees.csv")
print(employee_list)

dictionary = process_data(employee_list)
print(dictionary)

write_report(dictionary, "/home/student-03-c4854d3cc119/test_report.txt")
