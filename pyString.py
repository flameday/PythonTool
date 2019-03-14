#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import os, sys, re

import full_chinese_character3
import pyUsage

def isCharactorSeperator(ch):
    if ch in full_chinese_character3.half_characters_dict:
        return True
    if ch in full_chinese_character3.full_characters_dict:
        return True
    if ch in full_chinese_character3.other_characters_dict:
        return True

def isCharactorEnglish(ch):
    if ch in full_chinese_character3.full_eng_list:
        return True
    if ch in full_chinese_character3.half_eng_list:
        return True
    return False

def isCharactorNumber(ch):
    if ch in full_chinese_character3.full_digit_list:
        return True
    if ch in full_chinese_character3.half_digit_list:
        return True
    return False

def isAllSeperator(text):
    for e in text:
        if not isCharactorSeperator(e):
            return False
    return True
    
def isAllEnglish(text):
    for e in text:
        if not isCharactorEnglish(e):
            return False
    return True
    
def isAllNumber(text):
    for e in text:
#         print(pyUsage.get_cur_info(), 'e= ', e)
#         print(pyUsage.get_cur_info(), text, '===')
        if not isCharactorNumber(e):
            return False
    return True
    
def isAllNumberOrEnglish(text):
    #for e in text:
    #for i, e in enumerate(text):
#     for i in range(len(text)):
#         print(pyUsage.get_cur_info(), 'i= ', i, 'text[i]= ', text[i])
        
    for i, e in enumerate(text):
#         print(pyUsage.get_cur_info(),'e= ', e, ' len(e)= ',  len(e), 'i= ', i, 'len(text)= ', len(text))
        if not isCharactorNumber(e) and not isCharactorEnglish(e):
#             print(pyUsage.get_cur_info(), 'e= ', e)
#             print(pyUsage.get_cur_info(), text, '===', e, ' is number:', isCharactorNumber(e), '; is eng: ', isCharactorEnglish(e))
            return False
    return True
        
def hasEnglishCharactor(word):
    for i in range(len(word)):
        ch = word[i]
        if isCharactorEnglish(ch):
            return True
    return False
    

def removeHeadTailSpace(word, flag = ' '):
    while len(word) > 0 and word[0] == flag:
        word = word[1:]
    while len(word) > 0 and word[-1] == flag:
        word = word[:-1]
    return word

def changeDoubleSpace2SingleSpace(text):
    while text.find('  ') != -1:
        text = text.replace('  ',' ')
        #print 'text= ',text
    return text

def reExtractData(regex, content, index):
    r = ''
    if index == None:
        index = 1
        
    p = re.compile(regex)
    m = p.search(content)
    #print('m= ', m.group())
    if m != None: 
        #print('m.group()= ', m.group())
        r = m.group(index)
    return r

def my_spider_key(c):
    return c.encode('utf8')

def insert_or_add_dict(some_dict, key, value):
    if key in some_dict:
        some_dict[key] += value
    else:
        some_dict[key] = value
        
def insert_or_append_dict(some_dict, key, value):
    if key in some_dict:
        some_dict[key].append(value)
    else:
        some_dict[key] = [value, ]

def getLengthHan(e):
    length = 0
    for i in xrange(len(e)):
        if charactorIsUnicodeHan(e[i]):
            length += 2
        else:
            length += 1
    return length
            
def formatHan(some_list):
    max = 0
    for e in some_list:
        if max < getLengthHan(e):
            max = getLengthHan(e)
    
    ###2个空格
    max += 2
    ###
    t = []
    for e in some_list:
        #print get_cur_info(), e
        e += ' '*(max - getLengthHan(e))
        t.append(e)
    return t
    

def isEncoding(text, en):
    try:
        text.encode(en)###'gbk'
        return True
    except:
        pass
    return False

def fragmentList(text_list, frag_cnt):
    double_res_list = []
    #size = (len(text_list) + frag_cnt - 1) //frag_cnt
    size = len(text_list) //frag_cnt + 1
    print('size= ', size)

    for i in range(frag_cnt):
        beg = size * i
        end = size *(i+1)
        double_res_list.append(text_list[beg:end])
    for d in double_res_list:
        print ('len(d)= ', len(d))

    return double_res_list

def combineDoubleList2List(d_list):
    t_list = []
    [t_list.extend(e) for e in d_list]
    return t_list

if __name__ == '__main__':
#     a='你好，我是中国人'
#     b='联通'
#     print ('len(a)= %d, len(b)= %d'%(len(a), len(b)))
#     print (a, b)
    
    d = fragmentList(range(100), 3)
    for e in d:
        print ('len(e)= ', len(e))
