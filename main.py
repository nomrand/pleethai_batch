import common.excel_util as excel_util
import data.batch_example_data as batch_example_data
import data.batch_update as batch_update

if __name__ == '__main__':
    import sys
    import random

    filename = 'data\example_result.xlsx'
    batch_example_data.set_example_data(filename)
    batch_update.update(filename, random.choice(excel_util.COLOR_INDEX))
