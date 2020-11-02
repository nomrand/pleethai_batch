import pytest
import common.word_util as word_util

@pytest.mark.parametrize('sentence, expect', [
    ('私は走った', [
        {'surface': '私',    'base': '私', 'katakana': 'ワタシ',  'wordclass': '代名詞'},
        {'surface': 'は',    'base': 'は', 'katakana': 'ハ',      'wordclass': '助詞'},
        {'surface': '走った','base': '走る','katakana': 'ハシッタ','wordclass': '動詞'},
    ]),
])
def test_get_tokens_simple(sentence, expect):
    assert word_util.get_tokens_simple(sentence) == expect


@pytest.mark.parametrize('sentence, expect', [
    ('私は走った', [
        {'surface': '私',    'base': '私', 'katakana': 'ワタシ',  'wordclass': '代名詞',
        'hiragana': 'わたし', 'roman': 'watashi'},
        {'surface': 'は',    'base': 'は', 'katakana': 'ハ',      'wordclass': '助詞',
        'hiragana': 'は', 'roman': 'wa'},
        {'surface': '走った','base': '走る','katakana': 'ハシッタ','wordclass': '動詞',
        'hiragana': 'はしった', 'roman': 'hashitta'},
    ]),
])
def test_get_tokens(sentence, expect):
    assert word_util.get_tokens(sentence) == expect


if __name__ == '__main__':
    pytest.main(['-v', __file__])
