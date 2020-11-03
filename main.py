
import random
import sys

import common.excel_util as excel_util
import common.word_util as word_util
import create.ex_cons_data as ex_cons_data
import create.hira_roman as hira_roman



def conv_func():
    if len(sys.argv) < 3:
        print('ERROR')
        print('Usage: # python %s %s jp <Japanese Word>' % (sys.argv[0], sys.argv[1]))
        quit()

    # Read target sentences
    cmd = sys.argv[2]
    if len(sys.argv) < 4:
        return

    jp = sys.argv[3]
    if cmd == 'jp':
        result = word_util.get_sentence_data(jp)
        # japanese	hiragana	roman   wordclasses(,separated) words(,separated)
        print('%s\t%s\t%s\t%s\t%s' % (
            jp, result['hiragana'], result['roman'],
            ','.join(result['wordclasses_list']),
            ','.join(result['words_list']),
        ))
    if cmd == 'jp_detail':
        result = word_util.get_tokens(jp)
        print(result)


def create_func():
    if len(sys.argv) < 3:
        print('ERROR')
        print('Usage: # python %s %s ex_cons' % (sys.argv[0], sys.argv[1]))
        quit()

    toppath = 'excel_data'
    cmd = sys.argv[2]
    color = random.choice(excel_util.COLOR_INDEX)

    if cmd == 'ex_tmp':
        ex_cons_data.set_temp_data(toppath)
    if cmd == 'ex_cons':
        ex_cons_data.set_temp_data(toppath)
        ex_cons_data.set_actual_data(toppath, color)
        
    if cmd == 'word_info':
        hira_roman.create_info_word(toppath)
    if cmd == 'ex_info':
        hira_roman.create_info_ex(toppath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR')
        print('Usage: # python %s <Param> ...' % sys.argv[0])
        quit()

    if sys.argv[1] == 'conv':
        conv_func()
    elif sys.argv[1] == 'create':
        create_func()
