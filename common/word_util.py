import sys
from pykakasi import kakasi  # translate japanese to roman
from janome.tokenizer import Tokenizer  # analysis sentence
import common.const as const


def conv_word(word, mode_from, mode_to):
    ''' Convert word
    Parameters
    ----------
    mode_from, mode_to : str
        K	Katakana
        H	Hiragana
        J	Kanji
        a	Roman

    See Also
    --------
    https://pykakasi.readthedocs.io/en/latest/api.html#conversion-options
    '''
    k = kakasi()
    k.setMode(mode_from, mode_to)
    conv = k.getConverter()

    return conv.do(word)


def get_tokens_simple(sentence):
    ''' Separete sentence to words tokens list (simple mode)
    Parameters
    ----------
    sentence : str
        1 line of Japanese example(sentence) ex. 私は走った

    Returns
    -------
    result : list of dict
    
    result[n]['surface'] : str,
    result[n]['base'] : str,
    result[n]['katakana'] : str,
    result[n]['wordclass'] : str,
      ex.
      result[0] = {'surface': '私',    'base': '私', 'katakana': 'ワタシ',  'wordclass': '代名詞'}
      result[1] = {'surface': 'は',    'base': 'は', 'katakana': 'ハ',      'wordclass': '助詞'}
      result[2] = {'surface': '走った','base': '走る','katakana': 'ハシッタ','wordclass': '動詞'}
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

    result = []
    for t in tokens:
        surface_str = t.surface
        base_str = t.base_form
        katakana_str = t.reading if t.reading != '*' else t.surface

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
        
        result.append({
            "surface": surface_str,
            "base": base_str,
            "katakana": katakana_str,
            "wordclass": wordclass_str,
        })

    return result


def get_tokens(sentence):
    ''' Separete sentence to words tokens list
    Parameters
    ----------
    sentence : str
        1 line of Japanese example(sentence) ex. 私は走った

    Returns
    -------
    result : list of dict
    
    result[n]['surface'] : str,
    result[n]['base'] : str,
    result[n]['katakana'] : str,
    result[n]['wordclass'] : str,
    result[n]['hiragana'] : str,
    result[n]['roman'] : str,
      ex.
      result[0] = {'surface': '私',    'base': '私', 'katakana': 'ワタシ',  'wordclass': '代名詞',
        'hiragana': 'わたし', 'roman': 'watashi'}
      result[1] = {'surface': 'は',    'base': 'は', 'katakana': 'ハ',      'wordclass': '助詞',
        'hiragana': 'は', 'roman': 'wa'}
      result[2] = {'surface': '走った','base': '走る','katakana': 'ハシッタ','wordclass': '動詞',
        'hiragana': 'はしった', 'roman': 'hashitta'}
    '''
    tokens = get_tokens_simple(sentence)

    result = []
    for t in tokens:
        katakana_str = t['katakana']
        # add hira & roman
        # Get Hiragana
        hiragana_str = conv_word(katakana_str, 'K', 'H')
        t['hiragana'] = hiragana_str

        # Normalization Katakana for roman
        katakana_str = katakana_str.translate(str.maketrans(const.SIMBOL_CONVERT_TO_HANKAKU))
        # ハ->ワ(to make roman 'wa')
        if t['wordclass'] == '助詞' and katakana_str == 'ハ':
            katakana_str = 'ワ'

        # Get Roman
        roman = conv_word(katakana_str, 'K', 'a')
        t['roman'] = roman

        result.append(t)

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
        result['wordclasses_list']   List of wordclasses
    '''
    tokens = get_tokens(sentence)

    hiras = ''
    romans = ''
    words_list = []
    wordclasses_list = []
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
            wordclasses_list.append(t['wordclass'])

    hiras = hiras.strip()
    romans = romans.strip()

    result = {
        'hiragana': hiras,
        'roman': romans,
        'words_list': words_list,
        'wordclasses_list': wordclasses_list,
    }
    return result
