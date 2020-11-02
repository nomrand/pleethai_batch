import pytest
import data.batch_update as batch_update

@pytest.mark.parametrize('sentence, expect', [
    ('私は走った',
        {'hiragana': 'わたし は はしった', 'roman': 'watashi wa hashitta',
        'words_list': ['私', '走る']},
    ),
])
def test_get_sentence_data(sentence, expect):
    assert batch_update.get_sentence_data(sentence) == expect

if __name__ == '__main__':
    pytest.main(['-v', __file__])
