import pytest
import data.example_func as example_func

@pytest.mark.parametrize('word, mode_from, mode_to, expect', [
    ('ワタシハ', 'K', 'H', 'わたしは'),
    ('ハシッタ', 'K', 'a', 'hashitta'),
    ('わたしは', 'H', 'K', 'ワタシハ'),
    ('私は走った', 'J', 'H', 'わたしははしった'),
])
def test_conv_word(word, mode_from, mode_to, expect):
    assert example_func.conv_word(word, mode_from, mode_to) == expect


if __name__ == '__main__':
    pytest.main(['-v', __file__])
