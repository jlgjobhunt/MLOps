# ./MLOPS/openpyxl/openpyxl.install.test0.py

import openpyxl

def create_minimal_xlsx(filename):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet['A1'] = "Test Data"
    workbook.save(filename)

create_minimal_xlsx("minimal_test.xlsx")