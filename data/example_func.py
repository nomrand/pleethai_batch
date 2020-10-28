import sys
from pykakasi import kakasi  # translate japanese to roman
from janome.tokenizer import Tokenizer  # analysis sentence
import data.constant as const


def conv_word(word, mode1, mode2):
    ''' Convert word
    Parameters
    ----------
    mode1, mode2 : str
        K	Katakana
        H	Hiragana
        J	Kanji
        a	Roman

    See Also
    --------
    https://pykakasi.readthedocs.io/en/latest/api.html#conversion-options
    '''
    k = kakasi()
    k.setMode(mode1, mode2)
    conv = k.getConverter()

    return conv.do(word)


def get_tokens(sentence):
    ''' Separete sentence to words list
    Returns
    -------
    result : dict

    result['surface'] : list of str
        ex. ['私', 'は', '走っ', 'た']
    result['base'] : list of str
        ex. ['私', 'は', '走る', 'た']
    result['katakana'] : list of str
        ex. ['ワタシ', 'ハ', 'ハシッ', 'タ']
    result['wordclass'] : list of str
        ex. ['名詞', '助詞', '動詞', '助動詞']
    '''
    # Normalization
    sentence = sentence.translate(
        str.maketrans(const.SIMBOL_CONVERT_TO_ZENKAKU))
    tokens = Tokenizer().tokenize(sentence)
    # Normalization
    for t in tokens[:]:
        if t.reading.endswith('ッ'):
            # If tokens[i] is 'ハシッ' and tokens[i+1] is 'タ',
            # => tokens[i] will become 'ハシッタ', and delete tokens[i+1]
            # Because 'ハシッ' can't be converted to roman (it will be 'hashitsu')
            i = tokens.index(t)
            tokens[i].surface += tokens[i+1].surface
            tokens[i].reading += tokens[i+1].reading
            tokens.pop(i+1)

    result = {
        "surface": [],
        "base": [],
        "katakana": [],
        "wordclass": [],
    }
    for t in tokens:
        result["surface"].append(t.surface)
        result["base"].append(t.base_form)
        result["katakana"].append(t.reading if t.reading != '*' else t.surface)

        if const.DEBUG:
            print("DEBUG)", t.base_form, ":", t.part_of_speech)

        wordclass = t.part_of_speech.split(',')
        wordclass_str = wordclass[0]
        for class_chk_conv in const.WORD_CLASS_CONV:
            chk0 = class_chk_conv[0] is None or class_chk_conv[0] == wordclass[0]
            chk1 = class_chk_conv[1] is None or class_chk_conv[1] == wordclass[1]
            chk2 = class_chk_conv[2] is None or class_chk_conv[2] == wordclass[2]

            if all([chk0, chk1, chk2]):
                wordclass_str = class_chk_conv[3]
                break
        result["wordclass"].append(wordclass_str)

    return result


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
    t = get_tokens(sentence)

    hiras = ''
    romans = ''
    words_list = []
    for i, (kata, wordclass, word) in enumerate(zip(t["katakana"], t["wordclass"], t["base"])):
        # Get Hiragana (sentence -> Katakana(space-separated) -> Hiragana(space-separated))
        hira = conv_word(kata, 'K', 'H')
        hiras += hira + ' '

        # Get Roman (Katakana(space-separated) -> Roman(space-separated))
        # Normalization
        kata = kata.translate(str.maketrans(const.SIMBOL_CONVERT_TO_HANKAKU))
        # ハ->ワ(to make roman 'wa')
        if t["wordclass"][i] == '助詞' and kata == 'ハ':
            kata = 'ワ'
        roman = conv_word(kata, 'K', 'a')
        romans += roman + ' '

        # Get Words & WordClass
        if wordclass in const.WORD_CLASS:
            if word in ['～']:
                # Not for target
                pass
            elif (len(word) == 1) and (word == hira) and (wordclass != '名詞'):
                # Not for target
                pass
            else:
                words_list.append(word)

    hiras = hiras.strip()
    romans = romans.strip()

    result = {
        'hiragana': hiras,
        'roman': romans,
        'words_list': words_list,
    }
    return result
