import re
import datetime
import common.excel_util as excel_util
import data.constant as const
import data.example_func as example_func
import data.batch_example_data as batch_example_data

# CONST
WORK_SHEETNAME = 'new_example'
WORK_CONS_SHEETNAME = 'tmp_Constituent'
EXAMPLE_SHEETNAME = 'Example'
WORD_SHEETNAME = 'Word'
CONSTITUENT_SHEETNAME = 'Constituent'


def update(filename, color=None):
    ''' Write Data to Excel 
    (Example & Constituent)

    Parameters
    ----------
    filename : str
        File path to Excel
    color : str
        Cell style color code for new data (such as '00112233')
    '''
    print('### UPDATE DB DATA ###')
    sheetname = WORK_SHEETNAME
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print('### PREPARE DATA ###')
    # Get Original Data
    org_ex_data = excel_util.get_excel_data(filename, EXAMPLE_SHEETNAME)
    org_ex_jap = {org_data['japanese']: org_data for org_data in org_ex_data}
    org_cons_data = excel_util.get_excel_data(filename, CONSTITUENT_SHEETNAME)
    org_cons_ex_ids = [org_data['example_id'] for org_data in org_cons_data]
    word_map, sep_words_map = _create_word_maps(filename)

    # Get New Data
    new_ex_data = excel_util.get_excel_data(filename, sheetname)
    ex_max_id = max(org_data['id'] for org_data in org_ex_data)
    ex_target = []
    cons_max_id = max(org_data['id'] for org_data in org_cons_data)
    cons_target = []

    # Create Data to Write
    for data in new_ex_data:
        print('\tEx Data(for update):%s' % data['japanese'])
        # Example
        if data['japanese'] in org_ex_jap:
            print('\tSkip "Example" (Already exist)')
            data['id'] = org_ex_jap[data['japanese']]['id']
        else:
            ex_max_id += 1
            data['id'] = ex_max_id
            data['created_at'] = nowtime
            ex_target.append(data)

        # Constituent
        if data['id'] in org_cons_ex_ids:
            print('\tSkip "Constituent" (Already exist)')
        elif (data['words_list'] is '') or (data['words_list'] is None):
            print('\tSkip "Constituent" (No words list)')
        else:
            cons_max_id, cons_data_list = _create_cons_data(
                data, cons_max_id, word_map, sep_words_map)
            if len(cons_data_list) == 0:
                print('\tSkip "Constituent" (No constituent data)')

            cons_target.extend(cons_data_list)

    print('#### WRITE to EXCEL')
    print('EXAMPLE(num=%d)' % len(ex_target))
    # this starts from 1, and skip header line (=2)
    excel_util.set_excel_data(
        ex_target, filename, EXAMPLE_SHEETNAME, color=color)

    print('CONSTITUENT(num=%d)' % len(cons_target))
    # this starts from 1, and skip header line (=2)
    excel_util.set_excel_data(
        cons_target, filename, CONSTITUENT_SHEETNAME, color=color)
    excel_util.set_excel_data(
        cons_target, filename, WORK_CONS_SHEETNAME, color=color)

    print('### UPDATED!!! ###')


def _create_word_maps(filename):
    org_words_data = excel_util.get_excel_data(filename, WORD_SHEETNAME)
    org_words_data.sort(key=lambda x: x['searchs'], reverse=True)

    word_map = {}
    sep_words_map = {}
    for word in org_words_data:
        for wordstr in re.split(r'[()/／（）、,]+', word['japanese']):
            if wordstr in word_map:
                continue

            word_map[wordstr] = word

            disp_txt = ''
            word_data = example_func.get_sentence_data(wordstr)
            if len(word_data['words_list']) > 0:
                rec_map = sep_words_map
                for d in word_data['words_list']:
                    disp_txt += d + ' > '
                    if d not in rec_map:
                        rec_map[d] = {}
                    rec_map = rec_map[d]
                if '__value__' not in rec_map:
                    rec_map['__value__'] = word

            if const.DEBUG:
                print("\tWord Data(for check):",
                      word['id'], wordstr, '('+disp_txt+')')
    return (word_map, sep_words_map)


def _create_cons_data(data, cons_max_id, word_map, sep_words_map):
    cons_data_list = []
    order = 0

    words_list = data['words_list'].split(',')
    index = 0
    while index < len(words_list):
        cons_data = {}
        w = words_list[index]
        target_w = w
        word_obj = None
        if w in word_map:
            word_obj = word_map[w]
        elif w in sep_words_map:
            tmp_map = sep_words_map[w]
            while (index+1 < len(words_list)) and (words_list[index+1] in tmp_map):
                index += 1
                w = words_list[index]
                target_w += ' > ' + w
                tmp_map = tmp_map[w]
            if '__value__' in tmp_map:
                word_obj = tmp_map['__value__']
            elif 'する' in tmp_map and '__value__' in tmp_map['する']:
                word_obj = tmp_map['する']['__value__']

        if word_obj is not None:
            # Word Match
            cons_max_id += 1
            order += 1
            # for real Constituent data
            cons_data['id'] = cons_max_id
            cons_data['example_id'] = data['id']
            cons_data['word_id'] = word_obj['id']
            cons_data['order'] = order

            # for tmp Constituent data
            cons_data['example'] = data['japanese']
            cons_data['word'] = '/'.join([word_obj['japanese'],
                                          word_obj['english'], word_obj['thai']])

            cons_data_list.append(cons_data)

        index += 1

    return (cons_max_id, cons_data_list)


if __name__ == '__main__':
    import sys
    import random

    if (len(sys.argv) == 3) and (sys.argv[2] == 'all'):
        # Read target sentences
        filename = sys.argv[1]
        batch_example_data.set_example_data(filename)
        update(filename, random.choice(excel_util.COLOR_INDEX))
        quit()
    if len(sys.argv) != 2:
        print('ERROR')
        print('Usage: # python %s excel_filename' % sys.argv[0])
        quit()

    # Read target sentences
    filename = sys.argv[1]
    update(filename, random.choice(excel_util.COLOR_INDEX))
