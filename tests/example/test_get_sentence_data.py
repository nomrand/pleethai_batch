import pytest
import example.create_ex_cons_data as create_ex_cons_data

@pytest.mark.parametrize('sentence, expect', [
    ('私は走った',
        {'hiragana': 'わたし は はしった', 'roman': 'watashi wa hashitta',
        'words_list': ['私', '走る']},
    ),
])
def test_get_sentence_data(sentence, expect):
    assert create_ex_cons_data.get_sentence_data(sentence) == expect

if __name__ == '__main__':
    pytest.main(['-v', __file__])
