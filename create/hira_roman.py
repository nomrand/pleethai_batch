import datetime
import re
import shutil

import common.excel_util as excel_util
import common.file_util as file_util
import common.word_util as word_util
import common.const as const



def create_info_word(top_path):
    create_info(top_path, 'WORD')

def create_info_ex(top_path):
    create_info(top_path, 'EXAMPLE')


def create_info(top_path, target_table):
    ''' Create Example data & Set to Excel

    Parameters
    ----------
    top_path : str
        Top path of Excel file
    '''
    # check the files that will be used in this operation
    if target_table == 'WORD':
        # IN
        file_in = file_util.get_filepath_exist(top_path, 'in', const.EXCEL_WORD)
        # OUT
        file_out = file_util.get_filepath_noexist(top_path, 'out', const.EXCEL_WORD)
    elif target_table == 'EXAMPLE':
        # IN
        file_in = file_util.get_filepath_exist(top_path, 'in', const.EXCEL_EXAMPLE)
        # OUT
        file_out = file_util.get_filepath_noexist(top_path, 'out', const.EXCEL_EXAMPLE)
    else:
        print('ERROR')
        print('%s is invalid target!' % target_table)
        quit()
    shutil.copyfile(file_in, file_out)

    print('### CREATE %s DB DATA START!!! ###' % target_table)
    print('### PREPARE DATA ###')
    print('\tGetting Original Data' )
    org_data = excel_util.get_excel_data(file_in)

    target_data = []
    # Create Data to Write
    for data in org_data:
        print('\tData(for update):%s' % data['japanese'])
        converted = word_util.get_sentence_data(data['japanese'])
        # Update only target keys in 'target_data'
        target_data.append({
            'hiragana': converted['hiragana'],
            'roman': converted['roman'],
        })

    print('#### WRITE to EXCEL')
    print('EXAMPLE(num=%d)' % len(target_data))
    # this starts from 1, and skip header line (=2)
    excel_util.set_excel_data(target_data, file_out, startrow=2)

    print('### UPDATED!!! ###')
