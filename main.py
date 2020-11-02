import common.excel_util as excel_util
import example.create_ex_cons_data as create_ex_cons_data

if __name__ == '__main__':
    import sys
    import random

    filename = 'example\create_ex_cons_result.xlsx'
    create_ex_cons_data.set_temp_data(filename)
    create_ex_cons_data.set_actual_data(filename, random.choice(excel_util.COLOR_INDEX))
