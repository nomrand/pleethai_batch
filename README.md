# pleethai_tool

## installation
At the top of this project ...

### Install Pakcages
```
pip install -r requirements.txt
``` 



## Usage
At the top of this project ...

### Word Conversion
Convert a Japanese Word (or a sentence)
to hiragana, roman, word classes, and simple form words
```
python main.py conv jp <Japanese Word>
```
- Sample
```
# Command
python main.py conv jp 単語変換ツール

# Result (Tab separated)
# [Japanese Word]	[hiragana]	[roman]	[word classes]	[simple form words]
単語変換ツール  たんご へんかん つーる  tango henkan tsuuru     名詞,名詞,名詞  単語,変換,ツール
```

### DB Data Creation
Create "Example", "Constituent" DB Table data
from new Japanese, Thai, Englise sentences

1. Put the exported DB Table data (xlsx files) into `excel_data\in` directory
   - The names of exported DB Table data files must be Constituent.xlsx / Example.xlsx / Tag.xlsx / Word.xlsx / WordClass.xlsx
1. Write down 1 or more new Japanese, Thai, Englise sentences
into `Example_Input` sheet in `excel_data\in\create_ex_cons_result.xlsx` file
   - This file must be closed before going to next step
1. Type command bellow
```
python main.py create ex_cons
```

The results will be output into `excel_data\out` directory

**The results will be not perfect, so you must check!!**

__________
## Testing
1. Put test code into tests/**
2. Do test
```
pytest
```
