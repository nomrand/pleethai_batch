
import random
import sys

import common.excel_util as excel_util
import common.word_util as word_util
import example.create_ex_cons_data as create_ex_cons_data


def conv_func():
    if len(sys.argv) < 3:
        print('ERROR')
        print('Usage: # python %s %s jp <Japanese Word>' % (sys.argv[0], sys.argv[1]))
        quit()

    cmd = sys.argv[2]
    if len(sys.argv) < 4:
        if cmd == 'word':
            pass
        if cmd == 'example':
            pass
        return

    # Read target sentences
    jp = sys.argv[3]
    if cmd == 'jp':
        result = create_ex_cons_data.get_sentence_data(jp)
        # japanese	hiragana	roman   wordclasses(,separated) words(,separated)
        print('%s\t%s\t%s\t%s\t%s' % (
            jp, result['hiragana'], result['roman'],
            ','.join(result['wordclasses_list']),
            ','.join(result['words_list']),
        ))
    if cmd == 'jp_datail':
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
        create_ex_cons_data.set_temp_data(toppath)
    if cmd == 'ex_cons':
        create_ex_cons_data.set_temp_data(toppath)
        create_ex_cons_data.set_actual_data(toppath, color)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR')
        print('Usage: # python %s <Param> ...' % sys.argv[0])
        quit()

    if sys.argv[1] == 'conv':
        conv_func()
    elif sys.argv[1] == 'create':
        create_func()
