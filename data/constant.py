# batch common constants
DEBUG = False

# word class id data
WORD_CLASS = {
    "動詞": 1,
    "形容詞": 2,
    "名詞": 3,
    "副詞": 4,
    "助動詞": 5,
    "接続詞": 6,
    "前置詞": 7,
    "代名詞": 8,
}

# [0:2] -> check, [3] -> converted class
WORD_CLASS_CONV = [
    ['名詞', '接尾', '人名', '代名詞'],
    ['連体詞', None, None, '代名詞'],
    ['感動詞', None, None, '副詞'],
    [None, '代名詞', None, '代名詞'],
    ['助詞', '格助詞', None, '前置詞'],
    ['助詞', '副助詞', None, '前置詞'],
    [None, '数', None, '数'],
    [None, '接尾', None, '接尾'],
    [None, None, '人名', '人名'],
    ['名詞', '非自立', '一般', '名詞非自立'],
]

# CONVERT MAP ZENKAKU TO HANKAKU
SIMBOL_CONVERT_TO_HANKAKU = {
    "、": ",",
    "。": ".",
    "「": "\"",
    "」": "\"",
    "・": " ",
}
SIMBOL_CONVERT_TO_HANKAKU.update({
    chr(0xFF01 + i): chr(0x0021 + i) for i in range(94)})

# CONVERT MAP HANKAKU TO ZENKAKU
SIMBOL_CONVERT_TO_ZENKAKU = {
    chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}
