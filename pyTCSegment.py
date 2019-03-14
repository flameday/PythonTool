#!/usr/bin/python
#-*- coding: gb18030 -*-

import sys
import os
import pyUsage
import pyString

###把每个分词结果的 "词"+"词性"拆开为2元组
def extract_word_charactor(element):
#     print('element= ', element)
    pos = element.rfind('/')
    if -1 == pos:
        print(pyUsage.get_cur_info(), 'no split for chara error! element=', element)
        sys.exit(0)
        ###对符号进行加"/w"操作
        if len(element.encode('utf8')) == len(element):
            return [element, 'w']
        elif len(element) > 10:
            print(pyUsage.get_cur_info(), 'error! too much long! element=', element)
            sys.exit(0)
        else:
            return [element, '']
            #sys.exit(0)

    return [element[:pos], element[pos+1:]]

###把分句结果按词分拆
def split_text(text):
    t_list = text.split(' ')
    t_list = [e.strip() for e in t_list if len(e.strip()) > 0]
    t_list = [extract_word_charactor(e) for e in t_list]
    return t_list

###分词的时候,"符号,英文,数字,汉字"之间增加空格,从而便于分词预处理
def addSpaceSeperator(text):
    res = ''
    for i,e in enumerate(text):
        res += e
        if i + 1 < len(text) and isAddSpaceSeperate(e, text[i+1]):
            if len(res) > 0 and res[-1] != ' ':###避免2个空格
                res += ' '
    return res
    
###是否需要增加空格
###英文/数字是一类
###符号是一类
###汉字是一类
def isAddSpaceSeperate(cur_ch, next_ch):
    ###跳过空格
    if cur_ch == ' ':
        return False
    ###符号
    elif pyString.isCharactorSeperator(cur_ch):
        if not pyString.isCharactorSeperator(next_ch):
            return True
    ###英文,数字合并
    elif pyString.isCharactorEnglish(cur_ch) or pyString.isCharactorNumber(cur_ch):
        if (not pyString.isCharactorEnglish(next_ch)) \
            and (not pyString.isCharactorNumber(next_ch)):
            return True
    ###汉字
    else:
        if (pyString.isCharactorSeperator(next_ch)    \
            or pyString.isCharactorEnglish(next_ch) \
            or pyString.isCharactorNumber(next_ch) ):
            return True
        #print('e=|%s|'%e, 'res=|%s|'%res)
    return False

###生成BMI训练语料:暂不考虑英文,数字,符号
def genTrainText(text, flag_single_column = False):
    word_list = text.split(' ')
    res_list = []
        
    for i, word in enumerate(word_list):
        t = ''
        if word == ' ' or len(word) == 0:
            pass
        ###英文/数字是一类
        ###符号是一类
        ###汉字是一类
        ###字,所在的词长度,类别,位置大类别,位置index数字
#################################################第一个版本,保留原始英文和数字
#         elif pyString.isAllSeperator(word):
#             res_list.append((word, 1, 'SEPERATOR', 'S'))
#         elif pyString.isAllEnglish(word):
#             res_list.append((word, 1, 'ENGLISH', 'S'))
#         elif pyString.isAllNumber(word):
#             res_list.append((word, 1, 'NUMBER', 'S'))
#         elif pyString.isAllNumberOrEnglish(word):
#             res_list.append((word, 1, 'NUM_ENG', 'S'))
#         ###1个
#         elif len(word) == 1:
#             res_list.append((word, len(word), 'HAN', 'S'))
#         elif len(word) == 2:
#             res_list.append((word[0], len(word), 'HAN', 'B'))
#             res_list.append((word[1], len(word), 'HAN', 'I'))
#         else:
#             res_list.append((word[0], len(word), 'HAN', 'B'))
#             for i,e in enumerate(word[1:-1]):
#                 res_list.append((e, len(word), 'HAN', 'M'))
#             res_list.append((word[-1], len(word), 'HAN', 'I'))
#     ###把数字转成字符串
#     res_list = [list(e[:-1]) + ['%s'%e[-1]] for e in res_list]
#     res_list = [list(e[:1]) + ['%s'%e[1]] + list(e[2:]) for e in res_list]
#     ###对所有串进行处理
#     labeled_result = []
#     if flag_single_column:
#         labeled_result = ['\t\t'.join(e[:-1]) for e in res_list]
#     else:
#         for e in res_list:
#             #print('e= ', e)
#             labeled_result.append('\t\t'.join(e))
# 
#     res =  '\n'.join(labeled_result)     

#################################################第2个版本,英文ENG 数字NUM
        elif pyString.isAllSeperator(word):
            res_list.append((word, 'S'))
        elif pyString.isAllEnglish(word):
            res_list.append(('ENGLISH', 'S'))
        elif pyString.isAllNumber(word):
            res_list.append(('NUMBER', 'S'))
        elif pyString.isAllNumberOrEnglish(word):
            res_list.append(('NUM_ENG', 'S'))
        ###1个
        elif len(word) == 1:
            res_list.append((word, 'S'))
        elif len(word) == 2:
            res_list.append((word[0], 'B'))
            res_list.append((word[1], 'I'))
        else:
            res_list.append((word[0], 'B'))
            for i,e in enumerate(word[1:-1]):
                res_list.append((e, 'M'))
            res_list.append((word[-1], 'I'))
    ###把数字转成字符串:没有数字,无需处理

    ###处理串    
    labeled_result = []
    if flag_single_column:
        labeled_result = [' '.join(e[:-1]) for e in res_list]
    else:
        for e in res_list:
            #print('e= ', e)
            labeled_result.append(' '.join(e))

###################################################    

    res =  '\n'.join(labeled_result)     
    return res

#         print('word= ', word)
#         print('res_list= ', res_list)
#     print('text= ', text)
#     print('res=  ', res)

if __name__ == '__main__':
    pass   
