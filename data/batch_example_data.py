import sys
import common.excel_util as excel_util
import data.example_func as example_func

# CONST
WORK_SHEETNAME = 'new_example'


def set_example_data(filename):
    ''' Create Example data
    (from japanese -> to hiragana/roman/using words list)

    Parameters
    ----------
    filename : str
        File path to Excel
    '''
    print('### CREATE EXAMPLES DATA ###')
    sheetname = WORK_SHEETNAME

    sentences_data = excel_util.get_excel_data(filename, sheetname)
    if len(sentences_data) == 0:
        print("ERROR (NO EXAMPLES DATA)")
        return
    if sentences_data[0]["hiragana"] is not None:
        print("SKIP (ALREADY HAD EXAMPLES DATA)")
        return

    result = []
    for data in sentences_data:
        if not data['japanese']:
            break
        print('\tEx Data:%s' % data['japanese'])
        sentence = example_func.get_sentence_data(data['japanese'])
        sentence['words_list'] = ','.join(sentence['words_list'])
        result.append(sentence)

    print('WRITE to EXCEL')
    # line 1 is a header line, therefore starts line2
    excel_util.set_excel_data(result, filename, sheetname, startrow=2)
    print('### CREATED!!! ###')


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print('ERROR')
        print('Usage: # python %s excel_filename' % sys.argv[0])
        quit()

    # Read target sentences
    filename = sys.argv[1]
    set_example_data(filename)
