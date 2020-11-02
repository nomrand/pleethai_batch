
import random
import sys

import common.excel_util as excel_util
import common.word_util as word_util
import example.create_ex_cons_data as create_ex_cons_data


def word_func():
    if len(sys.argv) < 4:
        print('ERROR')
        print('Usage: # python %s %s conv <Japanese>' % (sys.argv[0], sys.argv[1]))
        quit()

    cmd = sys.argv[2]
    jp = sys.argv[3]

    # Read target sentences
    if cmd == 'conv_all':
        result = word_util.get_tokens(jp)
        print(result)
    if cmd == 'conv':
        result = create_ex_cons_data.get_sentence_data(jp)
        # japanese	hiragana	roman   wordclasses(,separated) words(,separated)
        print('%s\t%s\t%s\t%s\t%s' % (
            jp, result['hiragana'], result['roman'],
            ','.join(result['wordclasses_list']),
            ','.join(result['words_list']),
        ))


def ex_func():
    if len(sys.argv) < 3:
        print('ERROR')
        print('Usage: # python %s %s create_all' % (sys.argv[0], sys.argv[1]))
        quit()

    toppath = 'excel_data'
    cmd = sys.argv[2]
    color = random.choice(excel_util.COLOR_INDEX)

    if cmd == 'create':
        create_ex_cons_data.set_temp_data(toppath)
    if cmd == 'create_all':
        create_ex_cons_data.set_temp_data(toppath)
        create_ex_cons_data.set_actual_data(toppath, color)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR')
        print('Usage: # python %s <Param> ...' % sys.argv[0])
        quit()

    if sys.argv[1] == 'word':
        word_func()
    elif sys.argv[1] == 'ex':
        ex_func()
