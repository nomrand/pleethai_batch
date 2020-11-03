import pytest
import common.word_util as word_util

@pytest.mark.parametrize('sentence, expect', [
    ('私は走った',
        {
            'hiragana': 'わたし は はしった',
            'roman': 'watashi wa hashitta',
            'words_list': ['私', '走る'],
            'wordclasses_list': ['代名詞', '動詞']
        },
    ),
])
def test(sentence, expect):
    assert word_util.get_sentence_data(sentence) == expect

if __name__ == '__main__':
    pytest.main(['-v', __file__])
