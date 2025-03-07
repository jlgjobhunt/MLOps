# ./MLOPS/xlsxwriter/xlsxwriter.install.test0.py

import datetime as dt
import os
import xlsxwriter as xlw

def confirm_xlsxwriter_installation(filename="xlsxwriter_test.xlsx"):
    """
    Confirms xlsxwriter installation and demonstrates its capabilities.
    """
    try:
        # Create a new workbook and add worksheets.
        # The 'calc_on_load' option enables workbooks to load and calculate formulas.
        workbook = xlw.Workbook(filename, {'calc_on_load': True})
        worksheet1 = workbook.add_worksheet('Data Types')
        worksheet2 = workbook.add_worksheet('Formatting')
        worksheet3 = workbook.add_worksheet('Charts and Images')

        # Worksheet 1: Data Types
        worksheet1.write('A1', 'Text')
        worksheet1.write('B1', 123.45)
        worksheet1.write('C1', dt.datetime(2025, 3, 4))
        worksheet1.write_formula('D1', "=B1*2")

        # Worksheet 2: Formatting
        bold = workbook.add_format({'bold': True, 'font_color': 'red'})
        worksheet2.write('A1', 'Bold Red Text', bold)
        worksheet2.write('A2', 10, workbook.add_format({'bg_color': 'yellow', 'border': 1}))

        # Worksheet 3: Charts and Images
        # Insert an image.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir, 'example_image.png')

        try:
            worksheet3.insert_image('A1', image_path)
        except FileNotFoundError:
            print("Image file not found. Please place 'example_image.png' in the same directory.")

        # Create a chart (example: column chart)
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({'values': '=Formatting!A2:A10'})
        worksheet3.insert_chart('E1', chart)

        # Close the workbook.
        workbook.close()

        print(f"xlsxwriter installation confirmed. File '{filename}' created successfully.")

    except ImportError:
        print("xlsxwriter is not installed.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    confirm_xlsxwriter_installation()


        
