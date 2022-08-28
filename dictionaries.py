
# CODE를 단어로 바꾸기 위한 변수들. 차후 구조 변경예정
#정의부
from numpy import isin
import pandas as pd


class relationship_tree():
    """
    relationship tree는 단어간 코드간의 종속성을 정의하는 트리입니다.
    만약 key 값에 커피(CO)가 있다면 뒤에 있는 코드들의 단어들만 올 수 있습니다. 
    예제에서는 CO 뒤에는 OT, CT, BT, SZ에 해당되는 단어들만 올 수 있습니다.
    
    """
    def __init__(self):   
        """
        member variable :
            _node : Tree의 정보가 들어 있습니다.
        """
        self._node = {} 
        
    def __getitem__(self, key):
        """ Python의 Magic Method로써, dictionary에 value를 get 하기 위해 사용됩니다.

        Args:
            key (string): node의 key값, 주 code값으로써 종속 code값을 가지고 오는 key값입니다.
            

        Returns:
            value (string): 종속되는 code 값입니다. 
        """
        return self._node[key]
    
    def __setitem__(self, key, value):
        """_summary_

        Args:
            key (string): 새로운 값을 설정할 key 값
            value (string): 새로운 값을 지정할 value 값

        Raises:
            ValueError: key 값이 string이 아닐 경우 raise 함
            ValueError: value값이 list가 아닐 경우 raise 함
        """
        if isinstance(key,str) == False:
            raise ValueError("key type should be string")
        if isinstance(value,list) == False:
            raise ValueError("value type should be list")
        self._node[key] = value
    
    def read_csv(self,file_name : str):
        df = pd.read_csv(file_name)
        df = df.set_index("index_code")
        for index in df.index:
            self._node[index] = df.loc[index,:].dropna().to_list()
            
            
    def __iter__(self):
        return iter(self._node)
    
    def keys(self):
        return self._node.keys()
    
    def items(self):
        return self._node.items()
    
    def values(self):
        return self._node.values()
    
    def raw_data(self):
        return self._node
    

class wordset_dictionary():
    def __init__ (self):
        
        #정의 부 
        self._node = {}

    def __getitem__(self, key):
        return self._node[key]
    
    def __setitem__(self, key, value):
        if isinstance(key,str) == False:
            raise ValueError("key type should be string")
        if isinstance(value,list) == False:
            raise ValueError("value type should be list")
        self._node[key] = value
    
    def read_csv(self,file_name : str):
        df = pd.read_csv(file_name)
        df = df.set_index("index_code")
        for index in df.index:
            self._node[index] = df.loc[index,:].dropna().to_list()
    
    def __iter__(self):
        return iter(self._node)
    
    def keys(self):
        return self._node.keys()
    
    def items(self):
        return self._node.items()
    
    def values(self):
        return self._node.values()
    
    def raw_data(self):
        return self._node


if __name__ == '__main__':
    my_dict = wordset_dictionary()
    for key, value in my_dict.items():
        print(value)
    for key, value in relationship_tree().items():
        print(value)
