import this
import pandas as pd
import re
import copy
import sys
from collections import deque
import inspect
from dictionaries import wordset_dictionary, relationship_tree

class sentence_placeholder():
    """
    sentence placeholder는 placeholder에 원하는 단어들의 집합을 dictionary로 지정하면,
    단어들을 채워 문장을 생성하는 Tool 입니다.
    
    기본적으로는 dictionary를 override 한 형태로 이루어집니다. 함수에 대한 설명은 다음돠 같습니다.
    """

    def __init__(self):
        """
        __init__ instance를 생성하는 Magic method 입니다.
        
        member variable :
            wordset_dict - 단어집합을 가지고 있는 dictionary 입니다. 단어 코드내 해당하는 단어가 value로 존재합니다.
            rela_tree    - 단어 코드간에 관계를 정의하는 tree 입니다.
        """
        self.wordset_dict = wordset_dictionary()
        self.rela_tree  = relationship_tree()   

    def wordset_dic_readcsv(self, file_name : str):
        try:
            self.wordset_dict.read_csv(file_name)
        except Exception as e :
            print(f"function_name : {inspect.stack()[0][3]} line - {sys.exc_info()[-1].tb_lineno}  exception : {e}")
            
    def rela_tree_readcsv(self, file_name : str):
        try:
            self.rela_tree.read_csv(file_name)
        except Exception as e :
            print(f"function_name : {inspect.stack()[0][3]} line - {sys.exc_info()[-1].tb_lineno}  exception : {e}")
    
    
    def __call__(self,
                 input_df :pd.DataFrame, 
                 ) -> pd.DataFrame :
        
        output_df = pd.DataFrame(columns=["sentence","char_tag"])
        output_dict = {"sent":[],"char_tag":[] }

        for i in range(input_df.shape[0]):    
            try :
                cur_index_sententce = input_df.iloc[i].sentence

                angle_list = [(m.start() ,m.end()) for m in re.finditer(r'\<[^(\<\>)]*\>',cur_index_sententce)]
                tag_list = [cur_index_sententce[start+1:end-1].split('|') for start,end in angle_list]
                self.check_angle_pairs(cur_index_sententce)
                ner_tag = cur_index_sententce
                ner_tag = re.sub(r'\<[^(\<\>)]*\>',r'@',ner_tag)
                ner_tag = ['@' if c == '@' else 'O' for c in ner_tag]
                
                output_dict = self.generate_new_sentence(cur_index_sententce, ner_tag, tag_list)
            except Exception as e:
                print(f"function_name : {inspect.stack()[0][3]} line - {sys.exc_info()[-1].tb_lineno}  exception : {e} process continue")
                continue

        output_df = pd.DataFrame(data=output_dict)
        return output_df
    

    def generate_new_sentence(self,sentence, ner_tag, tag_list)-> dict:
        try :
            cur_sent_deque = deque([(sentence,ner_tag,"")])
            
            cur_tag = copy.deepcopy(ner_tag)
            return_dic = {"sent":[], "ner_tags":[]}

            for cur_tags in tag_list:    
                next_sent_deque = deque()
                while cur_sent_deque :
                    cur_sent, cur_nertag, parent_tag = cur_sent_deque.popleft()

                    angles = next(re.finditer(r'\<[^(\<\>)]*\>',cur_sent)).span()
                    cur_at_loc = cur_nertag.index('@')
                    for cur_tag in cur_tags:
                        try:
                            self.check_tag_dep(parent_tag, cur_tag)
                            self.append_slot_content(cur_sent, cur_tag, angles, cur_at_loc, cur_nertag, parent_tag, next_sent_deque)
                        except Exception as e:
                            #print(f"Exception = {e}, parent_tag = {parent_tag}, cur_tag = {cur_tag}")
                            continue
                cur_sent_deque = next_sent_deque 

            for sent, tag_by_char, _ in cur_sent_deque:
                return_dic["sent"].append(sent), return_dic["ner_tags"].append(tag_by_char)        
        except Exception as e:
            print(f"function_name : {inspect.stack()[0][3]} line - {sys.exc_info()[-1].tb_lineno}  exception : {e} process continue")
            raise Exception(e)
        else:
            return return_dic           

  
    def append_slot_content(self, 
                            cur_sent,
                            cur_tag,
                            angles,
                            cur_at_loc,
                            cur_nertag,
                            parent_tag,
                            next_sent_deque):      
        B_TAG = "B-"+cur_tag
        I_TAG = "I-"+cur_tag
        angle_start, angle_end = angles
        try:
            for slot_content_raw in self.wordset_dict[cur_tag] :
                slot_content_extended = []
                if len(slot_content_raw) > 0 and re.search(r'\[[^(\[\])]*\]',slot_content_raw):
                    s,e = next(re.finditer(r'\[[^(\[\])]*\]',slot_content_raw)).span()
                    searched_tag_start, searched_tag_end = re.search(r'\[[^(\[\])]*\]',slot_content_raw).span()
                    searched_tag = slot_content_raw[searched_tag_start+1 : searched_tag_end-1]
                    if searched_tag == "NUM":
                        tag_content_exp = [slot_content_raw[:s] + str(i) + (slot_content_raw[e:] if e <= len(slot_content_raw) else "") for i in range(1,int(self.wordset_dict[searched_tag])) ]
                    else :
                        tag_content_exp = [slot_content_raw[:s] + str(i) + (slot_content_raw[e:] if e <= len(slot_content_raw) else "") for i in self.wordset_dict[searched_tag]]
                    slot_content_extended += tag_content_exp
                else:
                    slot_content_extended.append(slot_content_raw)

                for slot_content in slot_content_extended:    
                    tobe_sentence = cur_sent[:angle_start]
                    tobe_sentence += slot_content
                    tobe_sentence += (cur_sent[angle_end:] if angle_end <= len(cur_sent)-1 else "")

                    tobe_nertag = cur_nertag[:cur_at_loc]
                    for slot_content_char in range(len(slot_content)):
                        this_tag = I_TAG if slot_content_char != 0 else B_TAG
                        tobe_nertag.append(this_tag)
                    tobe_nertag += (cur_nertag[cur_at_loc+1:] if cur_at_loc < len(cur_nertag)-1 else "")
                    tobe_tag = cur_tag if cur_tag in self.rela_tree.keys() else parent_tag
                    next_sent_deque.append((tobe_sentence,tobe_nertag,tobe_tag))
        except Exception as e:
            print(f"function_name : {inspect.stack()[0][3]} line - {sys.exc_info()[-1].tb_lineno}  exception : {e} process continue")
            raise Exception(e)

                
    ## 괄호의 짝이 맞는지 확인하는 함수.
    def check_angle_pairs(self,str):
        stack = []
        push_chars, pop_chars = "<", ">"
        for c in str :
            if c in push_chars :
                stack.append(c)
            elif c in pop_chars :
                if not len(stack) :
                    raise SyntaxError("angle parentheses not match")
                else :
                    stack_top = stack.pop()
                    balancing_bracket = push_chars[pop_chars.index(c)]
                    if stack_top != balancing_bracket :
                      return SyntaxError("angle parentheses not match")
        return True
    
    
    def check_tag_dep(self, parent_tag, cur_tag):
        
        if not parent_tag :
            return
        elif not parent_tag in self.rela_tree.keys() :
            raise Exception("Parent is not parent")
        elif not cur_tag in self.rela_tree[parent_tag] :
            raise Exception("Not supported format")   
        return
                       
    def add_wordset_dict(self,**kwargs):
        try :
            for key, value in kwargs.items():
                self.wordset_dict[key] = value
        except Exception as e:
            print("Error message :", end=" ")
            print(e)
        else :
            print("registered new keyword complete")
    
    def add_rela_tree(self, **kwargs):
        try :
            for key, value in kwargs.items():
                self.wordset_dict[key] = value
        except Exception as e:
            print("Error message :", end=" ")
            print(e)
        else :
            print("registered new keyword complete")    

