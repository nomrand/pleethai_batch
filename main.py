import common.excel_util as excel_util
import data.batch_update as batch_update

if __name__ == '__main__':
    import sys
    import random

    filename = 'data\example_result.xlsx'
    batch_update.set_temp_data(filename)
    batch_update.set_actual_data(filename, random.choice(excel_util.COLOR_INDEX))
