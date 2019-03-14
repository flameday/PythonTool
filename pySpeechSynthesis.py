#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os
import pyString
import pyUsage
import pyXml

###统计字典中多音字的个数
def getPinyin(py_list):
    t_list = [e['PinYin'] for e in py_list]
    t_list = list(set(t_list))
    t_list.sort()
    return t_list
    
###统计字典中多音字的个数
def getPinyinCntDicts(path):
    if not os.path.exists(path):
        print(pyUsage.get_cur_info(), '路径不存在,path= ', path)
        sys.exit(0)
        
    lang, name, word_info_dict = pyXml.readPinyinXmlDict(path)
    
    word_py_dict = {}
    word_py_cnt_dict={}
    pinyin_cnt_distribution_dict = {}
    
    for k in word_info_dict:
        v = word_info_dict[k]
        
        word_py_dict[k] = getPinyin(v)
        word_py_cnt_dict[k] = len(getPinyin(v))
        pyString.insert_or_add_dict(pinyin_cnt_distribution_dict, len(getPinyin(v)),1)
    
    ###单词有多少个拼音
    print(pyUsage.get_cur_info(), 'pinyin_cnt_distribution_dict= ', pinyin_cnt_distribution_dict, 'total_word_cnt= ', len(word_info_dict))
    return word_py_dict, word_py_cnt_dict, pinyin_cnt_distribution_dict

###word转成GBK编码
def getGBKText(word):
    word = word.strip()
    total_gbk_text = ''
    for w in word:
        gbk_val = w.encode('gb18030')
        if len(gbk_val) != 2:
            print(pyUsage.get_cur_info(), 'critical error', '不是GBK编码')
            sys.exit(0)
        gbk_text = '%X%X'%(gbk_val[0], gbk_val[1])
        total_gbk_text += gbk_text
    return total_gbk_text

###合成路径的查找
def findDirByString(path, s):
    path = path.strip()
    path = os.path.abspath(path)
    ###路径加一个斜杠
    if os.path.isdir(path):
        if path[-1] != os.sep:
            path += os.sep

    pos = path.find(s)
    if pos == -1:
        return ''
    
    print(pyUsage.get_cur_info(), 'total path= ', path)
    return path[:pos + len(s)]
    
def getSpeechSynthesis_AlgorithmDir():
    s = '/trunk/algorithm/tools/'
    path = findDirByString(sys.argv[0], s)
    if len(path) == 0:
        path = findDirByString(__file__, s)
    if len(path) == 0:
        path = findDirByString(sys.path[0], s)

    s = '/algorithm/tools/'
    path = findDirByString(sys.argv[0], s)
    if len(path) == 0:
        path = findDirByString(__file__, s)
    if len(path) == 0:
        path = findDirByString(sys.path[0], s)
    
    if not os.path.exists(path):
        path = '/Users/daiqiang/speech_synthesis_svr_proj/trunk/algorithm/'
        
    if len(path) == 0:
        print(pyUsage.get_cur_info(), 'dir not exists! (算法目录不存在!)')
        sys.exit(0)

    algorithm_dir = findDirByString(path, '/algorithm/')
    
    if not os.path.exists(algorithm_dir):
        print(pyUsage.get_cur_info(), 'dir not exists! (算法目录不存在!)')
        sys.exit(0)
    return algorithm_dir
    
def getSpeechSynthesis_DataDictDir():
    dict_dir = getSpeechSynthesis_AlgorithmDir() + '../../document/data/dict/'
    print(pyUsage.get_cur_info(), 'dict_dir= ', dict_dir)
    
    return dict_dir
    
def getSpeechSynthesis_ToolsSegDir():
    seg_dir = getSpeechSynthesis_AlgorithmDir() + '/tools/seg/'
    print(pyUsage.get_cur_info(), 'seg_dir= ', seg_dir)
    return seg_dir

# def getSpeechSynthesis_SourcedataPhonetictrainingDir():
#     phoneticResDir = getSpeechSynthesis_AlgorithmDir() + '/sourcedata/phonetictraining/'
#     return phoneticResDir


###检验汉语拼音是否合法:多个
def isValidWordPinyin(word_py, py_phoneme_dict):
    word_py = word_py.strip()
    py_list = word_py.split(' ')
    for py in py_list:
        if not isValidSinglePinyin(py, py_phoneme_dict):
            return False
    return True
    
###检验汉语拼音是否合法:单个
def isValidSinglePinyin(py, py_phoneme_dict):
    ###长度>=2: m2,hao3
    py = py.strip()
    py = py.lower()
    if len(py) < 2:
        return False
        
    ###最后是一个数字
    if py[-1] < '0' or py[-1] > '6':
        return False

    ###其他是英文字符
    for e in py[:-1]:
        if e < 'a' or e > 'z':
            return False
    ###在音素列表内
    if py[:-1] not in py_phoneme_dict:
        return False
    ###儿化音:
    if py[:-1][-1] == 'r' and py[:-1] != 'er':
        return False
        
    return True