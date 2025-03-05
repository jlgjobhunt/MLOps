# ./MLOPS/openpyxl/openpyxl.install.test1.py

import openpyxl
import datetime


def create_sample_xlsx(filename):
    """
    Creates an xlsx file with multiple worksheets, data types, and formulas.
    """
    
    workbook = openpyxl.Workbook()

    # Worksheet 1: Data Types
    worksheet1 = workbook.create_sheet("Data Types")

    worksheet1.title = 'Data Types'

    worksheet1['A1'] = "Text"
    worksheet1['B1'] = "Number"
    worksheet1['C1'] = "Date"
    worksheet1['D1'] = "Boolean"
    worksheet1['A2'] = "John Q. Public"
    worksheet1['B2'] = 60000.00
    worksheet1['C2'] = datetime.datetime(2025, 3, 4)
    worksheet1['D2'] = False
    

    # Worksheet 2: Compound Interest
    worksheet2 = workbook.create_sheet("Compound Interest")

    worksheet2.title = 'Compound Interest'

    worksheet2['A1'] = "Principal"
    worksheet2['B1'] = "Interest Rate"
    worksheet2['C1'] = "Years"
    worksheet2['D1'] = "Future Value"
    worksheet2['A2'] = 1000
    worksheet2['B2'] = 0.05
    worksheet2['C2'] = 5
    worksheet2['D2'] = "=A2*(1+B2)^C2"


    # Worksheet 3: Key-Value Pairs
    worksheet3 = workbook.create_sheet("Key-Value Pairs")

    worksheet3.title = 'Key-Value Pairs'

    worksheet3['A1'] = "Number"
    worksheet3['B1'] = "User"
    worksheet3['A2'] = 1000001
    worksheet3['B2'] = "Joshua Greenfield"
    worksheet3['A3'] = "=A2+1"
    worksheet3['B3'] = "Luigi Da' Plumber"
    worksheet3['A4'] = "=A3+1"
    worksheet3['B4'] = "The Third Man"


    # Remove the default first sheet in the workbook.
    try:
        remove_sheet = workbook['Sheet']
        workbook.remove(remove_sheet)
    except KeyError:
        print(f"Error: Default worksheet 'Sheet' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    workbook.save(filename)


def main():

    import os
    
    print(f"Current directory: {os.getcwd()}")

    try:
        create_sample_xlsx("output_test1.xlsx")

    except Exception as e:
        print(f"Unable to create Openpyxl example file. Error: {e}")


if __name__ == "__main__":
    main()