import common.word_util as word_util
import example.create_ex_cons_data as create_ex_cons_data

if __name__ == '__main__':
    import sys
    import random

    if len(sys.argv) != 3:
        print('ERROR')
        print('Usage: # python %s <Command> <Japanese sentence>' % sys.argv[0])
        quit()

    # Read target sentences
    if sys.argv[1] == 'conv_base':
        result = word_util.get_tokens(sys.argv[2])
        print(result)
    if sys.argv[1] == 'conv':
        result = create_ex_cons_data.get_sentence_data(sys.argv[2])
        print(result)