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
    ]
    word_map, sep_words_map = create_ex_cons_data._create_word_maps(org_words_data)
    example_data = {'id':10, 'japanese':'', 'words_list':'生き物,生きる,死ぬ,生きる,いる,人,生きる,いる,生きる,たい',}
    
    cons_data_list = create_ex_cons_data._create_cons_data(example_data, word_map, sep_words_map)
    assert len(cons_data_list) == 5
    # 'id':2, 'japanese':'生き物'
    assert cons_data_list[0]['example_id'] == 10
    assert cons_data_list[0]['word_id'] == 2
    assert cons_data_list[0]['order'] == 1
    # 'id':5, 'japanese':'生き死に'
    assert cons_data_list[1]['example_id'] == 10
    assert cons_data_list[1]['word_id'] == 5
    assert cons_data_list[1]['order'] == 2
    # 'id':4, 'japanese':'生きていた人'
    assert cons_data_list[2]['example_id'] == 10
    assert cons_data_list[2]['word_id'] == 4
    assert cons_data_list[2]['order'] == 3
    # 'id':1, 'japanese':'生きている'
    assert cons_data_list[3]['example_id'] == 10
    assert cons_data_list[3]['word_id'] == 1
    assert cons_data_list[3]['order'] == 4
    # 'id':0, 'japanese':'生きる'
    assert cons_data_list[4]['example_id'] == 10
    assert cons_data_list[4]['word_id'] == 0
    assert cons_data_list[4]['order'] == 5


if __name__ == '__main__':
    pytest.main(['-v', __file__])
