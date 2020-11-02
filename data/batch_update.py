import datetime
import re

import common.excel_util as excel_util
import common.word_util as word_util

import data.const as const


def set_temp_data(filename):
    ''' Create Temporaly Example data & Set to Excel

    Parameters
    ----------
    filename : str
        File path to Excel
    '''
    print('### CREATE TEMPORALY DATA ###')
    sheetname = const.WORK_SHEETNAME

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
        sentence = get_sentence_data(data['japanese'])
        sentence['words_list'] = ','.join(sentence['words_list'])
        result.append(sentence)

    print('WRITE to EXCEL')
    # line 1 is a header line, therefore starts line2
    excel_util.set_excel_data(result, filename, sheetname, startrow=2)
    print('### CREATED!!! ###')


def set_actual_data(filename, color=None):
    ''' Create Actual Example, Constituent data & Set to Excel

    Parameters
    ----------
    filename : str
        File path to Excel
    color : str
        Cell style color code for new data (such as '00112233')
    '''
    print('### SET ACTUAL DB DATA ###')
    work_sheetname = const.WORK_SHEETNAME
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print('### PREPARE DATA ###')
    # Get Original Data
    print('\tGetting Example Data' )
    org_ex_data = excel_util.get_excel_data(filename, const.EXAMPLE_SHEETNAME)
    org_ex_jap = {org_data['japanese']: org_data for org_data in org_ex_data}
    print('\tGetting Constituent Data' )
    org_cons_data = excel_util.get_excel_data(filename, const.CONSTITUENT_SHEETNAME)
    org_cons_ex_ids = [org_data['example_id'] for org_data in org_cons_data]

    print('\tCreating Temp Word Data' )
    org_words_data = excel_util.get_excel_data(filename, const.WORD_SHEETNAME)
    org_words_data.sort(key=lambda x: x['searchs'], reverse=True)
    word_map, sep_words_map = _create_word_maps(org_words_data)

    # Get Work Data
    work_ex_data = excel_util.get_excel_data(filename, work_sheetname)
    ex_ids = [org_data['id'] for org_data in org_ex_data]
    ex_max_id = 0
    if len(ex_ids) > 0:
        ex_max_id = max(ex_ids)
    ex_target = []

    cons_ids = [org_data['id'] for org_data in org_cons_data]
    cons_max_id = 0
    if len(cons_ids) > 0:
        cons_max_id = max(cons_ids)
    cons_target = []

    # Create Data to Write
    for data in work_ex_data:
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
            cons_data_list = _create_cons_data(data, word_map, sep_words_map)
            if len(cons_data_list) == 0:
                print('\tSkip "Constituent" (No constituent data)')
            else:
                # update constitute id
                for cons_data in cons_data_list:
                    cons_max_id += 1
                    cons_data['id'] = cons_max_id

            cons_target.extend(cons_data_list)

    print('#### WRITE to EXCEL')
    print('EXAMPLE(num=%d)' % len(ex_target))
    # this starts from 1, and skip header line (=2)
    excel_util.set_excel_data(
        ex_target, filename, const.EXAMPLE_SHEETNAME, color=color)

    print('CONSTITUENT(num=%d)' % len(cons_target))
    # this starts from 1, and skip header line (=2)
    excel_util.set_excel_data(
        cons_target, filename, const.CONSTITUENT_SHEETNAME, color=color)
    excel_util.set_excel_data(
        cons_target, filename, const.WORK_CONS_SHEETNAME, color=color)

    print('### UPDATED!!! ###')


def get_sentence_data(sentence):
    ''' Convert example(sentence) to Hiragana, Roman, Words...
    Parameters
    ----------
    sentence : str
        1 line of Japanese example(sentence) ex. 私は走った

    Returns
    -------
    result : dict
        result['hiragana']   Hiragana (space-separated) (ex. わたし は はしっ た)
        result['roman']   Roman (space-separated) (ex. watashi ha hashitsu ta)
        result['words_list']   List of words (ex. result['words_list'][0]=私, result['words_list'][1]=走る, ...)
    '''
    tokens = word_util.get_tokens(sentence)

    hiras = ''
    romans = ''
    words_list = []
    for t in tokens:
        hiras += t['hiragana'] + ' '
        romans += t['roman'] + ' '

        # Set Words
        if t['wordclass'] in const.WORD_CLASS:
            if t['base'] in const.NO_WORDS_LIST_TARGETS:
                # Not for target
                continue
            if (len(t['base']) == 1) and (t['base'] == t['hiragana']) and (t['wordclass'] != '名詞'):
                # Not for target (postpositional particle, such as 'は', 'が', 'へ', 'の', 'と', 'も' ...)
                continue
            words_list.append(t['base'])

    hiras = hiras.strip()
    romans = romans.strip()

    result = {
        'hiragana': hiras,
        'roman': romans,
        'words_list': words_list,
    }
    return result


def _create_word_maps(org_words_data):
    ''' *** This operation will take long time up to number of WORD table records ***
    Create 2 types of word data

    Returns
    -------
    result : tupple of dict
    
    result[0] : dict (key=japanese-string : value=word-data-object)
      ex.
      result[0]['おお'] = {'japanese':'おお', 'hiragana':'おお', ...} # word data of the word 'おお'
      result[0]['歴史的な'] = {'japanese':'歴史的な', 'hiragana':'れきしてきな', ...}
      result[0]['生きている'] = {'japanese':'生きている', 'hiragana':'いきている', ...}
      ...
    result[1] : dict (stored separated japanese words recursively)
      ex. (if Words data are 'おお', '生きている')
      result[1]['おお']['__value__'] = {'japanese':'おお', 'hiragana':'おお', ...} # word data of the word 'おお'
      result[1]['生きる']['いる']['__value__'] =
        {'japanese':'生きている', 'hiragana':'いきている', ...} # word data of the word '生きている'
    '''

    word_map = {}
    sep_words_map = {}
    for i, word in enumerate(org_words_data):
        if i % 200 == 0:
            print('\tCreate Temp Word Data No.%d of %d (%d%%)' %
                (i, len(org_words_data), int(i*100 / len(org_words_data))))

        for wordstr in re.split(r'[()/／（）、,]+', word['japanese']):
            if wordstr in word_map:
                continue

            # set japanese vs word-data map
            word_map[wordstr] = word

            # set separeted data map, such as
            # sep_words_map['生きる']['いる']['__value__'] -> word data of the word '生きている'
            disp_txt = ''
            word_data = get_sentence_data(wordstr)
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


def _create_cons_data(example_data, word_map, sep_words_map):
    ''' Find the word that used in the target Example from all exist words
    and return the constituent data
    '''
    cons_data_list = []
    order = 0

    words_list = example_data['words_list'].split(',')
    index = 0
    max_index = len(words_list)
    while index < max_index:
        cons_data = {}
        w = words_list[index]
        word_obj = None

        if w in word_map:
            # perfect match
            word_obj = word_map[w]
        if w in sep_words_map:
            # find from the separated words
            # ex.
            # 　if target Example is '生きていたXXXX' -> it will be changed ['生きる', 'いる', XXXX]
            # 　and it will match with the Word '生きている'(==sep_words_map['生きる']['いる']['__value__'])
            tmp_word_obj = None
            tmp_map = sep_words_map[w]
            tmp_index = index + 1
            while tmp_index < max_index and (words_list[tmp_index] in tmp_map):
                tmp_map = tmp_map[words_list[tmp_index]]

                if '__value__' in tmp_map:
                    # separated words match
                    tmp_word_obj = tmp_map['__value__']
                elif 'する' in tmp_map and '__value__' in tmp_map['する']:
                    # 'XXする' matches the word 'XX'
                    tmp_word_obj = tmp_map['する']['__value__']
                    
                tmp_index += 1

            if tmp_word_obj is not None:
                word_obj = tmp_word_obj
                index = tmp_index - 1

        if word_obj is not None:
            # Word match
            order += 1
            # for real Constituent data
            cons_data['example_id'] = example_data['id']
            cons_data['word_id'] = word_obj['id']
            cons_data['order'] = order

            # for tmp Constituent data
            cons_data['example'] = example_data['japanese']
            cons_data['word'] = '/'.join([word_obj['japanese'],
                                          word_obj['english'], word_obj['thai']])

            cons_data_list.append(cons_data)

        index += 1

    return cons_data_list
