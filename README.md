# How to use util
이 util은 문장을 생성하는 code 입니다.
이 code를 실행하면, relationship tree와 word dictionary 기반으로 문장이 생성되며, 단어를 기준으로 NER(Named Entity Recognition)에 사용되는 "BIO" tag값이 생성됩니다.


이 페이지에서는 파일의 구조와 역할에 대해 설명하는 문서 입니다.
사용법을 알고 싶으시다면 <span style="color:orange">  
./quickstart.ipynb</span>를 참조 부탁드립니다.


## Repo structure

```bash
sentence_placeholder
├── data
│   ├── rela_tree_data.csv
│   └── word_dict_data.csv
├── dictionaries.py
├── sentence_placeholder.py
└── quickstart.ipynb
```


# 파일 설명
  

## sentence_placeholder.py
홑화살괄호로 감싸진 code들로 채워진 sentence를  
학습에 사용될 sentence와 character단위의 ner_tag를 만드는 함수들의 집합입니다.
 
    - 문장을 생성하는 class
    - 괄호의 유효성을 검토
    - wordset_dictionary를 이용하여 괄호내 CODE 내 대응되는 단어들을 채움
    - relationship_tree를 이용하여 CODE끼리 의존 관계가 없는 code 조합을 피함
    - dictionary로 파일을 return
  
## dictionaries.py 
- 문장 생성기에서 사용할 dictionary들의 class 집합입니다.
    - relationship_tree 와 wordset_dictionary로 이루어져 있습니다.
    - wordset_dictionary는 단어 집합을 관리하고 있습니다
    - wordset_dictionary의 key값은 code이고, value 값은 code 집합내의 단어들입니다.
    - 문장내 홑화살괄호로 감싸져 있는 코드값들은 wordset_dictionary 내에서 단어로 치환되어 생성됩니다.
    - relationship_tree내에 있는 code값들은 code간 의존도를 나타냅니다.
    - key값에 있는 code가 나왔다면 value값에 있는 code값만 허용이 됩니다.
    - 각 class의 object는 파일을 입력을 받아 dictionary가 완성됩니다.

## dictionaries.py 
recur_create_sentence에 사용할 dictionary의 모음입니다.

1. convert_dic
- NER_TAG를 매칭하고 NER_TAG에 맞는 Keyword로 변환하는 dictionary 입니다.
- 숫자의 경우에는 추후 TNTAG를 이용하여 글자로 변환할 예정입니다.
2. dictionaries.py
- NER_TAG간 관계를 나타내는 dictionary 입니다.
- 부모 NER_TAG 내에 자식 NER_TAG가 없으면 그 문장은 생성되지 않습니다.


## data directory

### rela_tree_data
- relation tree에 있는 code들의 집합입니다.

### word_dict_data.csv
- wordset_dictionary 에 있는 key값과 value값의 집합입니다.







