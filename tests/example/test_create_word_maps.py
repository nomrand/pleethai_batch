import pytest
import example.create_ex_cons_data as create_ex_cons_data

def test_get_sentence_data():
    org_words_data = [
        {'id':0, 'japanese':'生きる', 'english':'', 'thai':''},
        {'id':1, 'japanese':'生きている', 'english':'', 'thai':''},
        {'id':2, 'japanese':'生き物', 'english':'', 'thai':''},
        {'id':3, 'japanese':'生きていた', 'english':'', 'thai':''},
        {'id':4, 'japanese':'生きていた人', 'english':'', 'thai':''},
        {'id':5, 'japanese':'生き死に', 'english':'', 'thai':''},
        {'id':6, 'japanese':'ABC、bbb,CCC/DDD//(分割される例)', 'english':'', 'thai':''},
    ]

    word_map, sep_words_map = create_ex_cons_data._create_word_maps(org_words_data)
    assert '' not in word_map
    assert word_map['生きる'] == org_words_data[0]
    assert word_map['生きている'] == org_words_data[1]
    assert word_map['生き物'] == org_words_data[2]
    assert word_map['生きていた'] == org_words_data[3]
    assert word_map['生きていた人'] == org_words_data[4]
    assert word_map['生き死に'] == org_words_data[5]

    # separated
    assert word_map['ABC'] == org_words_data[6]
    assert word_map['bbb'] == org_words_data[6]
    assert word_map['CCC'] == org_words_data[6]
    assert word_map['DDD'] == org_words_data[6]
    assert word_map['分割される例'] == org_words_data[6]

    # 生きる changes to '生きる' > '__value__'
    # 生きている changes to '生きる' > 'いる' > '__value__'
    # 生きていた人 changes to '生きる' > 'いる' > '人' > '__value__'
    assert '' not in sep_words_map
    assert sep_words_map['生きる']['__value__'] == org_words_data[0]
    assert sep_words_map['生きる']['いる']['__value__'] == org_words_data[1]
    assert sep_words_map['生き物']['__value__'] == org_words_data[2]
    assert sep_words_map['生きる']['いる']['人']['__value__'] == org_words_data[4]
    assert sep_words_map['生きる']['死ぬ']['__value__'] == org_words_data[5]

    # separated
    assert sep_words_map['ＡＢＣ']['__value__'] == org_words_data[6]
    assert sep_words_map['ｂｂｂ']['__value__'] == org_words_data[6]
    assert sep_words_map['ＣＣＣ']['__value__'] == org_words_data[6]
    assert sep_words_map['ＤＤＤ']['__value__'] == org_words_data[6]
    assert sep_words_map['分割']['する']['例']['__value__'] == org_words_data[6]

if __name__ == '__main__':
    pytest.main(['-v', __file__])
