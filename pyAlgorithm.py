#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os
import pyString

###因为是多个部分，这里按列表输出
def split2MultiParts(text, num = 2):
    if num > len(text):
        logging.error('bad argument: num=%d is bigger than "%s"'%(num, text))
        
    if num <= 0:
        logging.info('bad argument: num%d'%num)
    elif num == 1:
        return [[text,]]
    elif num == 2:
        res_list = []
        for i in range(1, len(text)):
            res_list.append([text[:i], text[i:]])
        return res_list
    elif num > 2:
        res_list = []
        for i in range(1, len(text) - 1):
            f = text[:i]
            s_list = split2MultiParts(text[i:], num - 1)
            ###处理子结果
            for index in range(len(s_list)):
                s_list[index].insert(0, f)
            ###合并子结果
            res_list.extend(s_list)
        return res_list

###2个列表合并，长度是N，M，变为N*M个结果
def mergeTextList(first_list, second_list, splitChar = ' '):
    tmp_result = []

    ###如果first_list是空呢?所以需要判断
    if len(first_list) == 0:
        tmp_result = second_list
        
    for f in first_list:
        for s in second_list:
            text = f + splitChar + s
            tmp_result.append(text)
    return tmp_result 

###最长公共子序列
def maxLengthCommontSequence(first_list, second_list):
    #print 'f= ', first_list, ', s= ', second_list
    
    if len(first_list) == 0 or len(second_list) == 0:
        return 0, []

    ###相等
    if first_list[0] == second_list[0]:
        length, res_list = maxLengthCommontSequence(first_list[1:], second_list[1:])
        tmp_list = [first_list[0], ]
        tmp_list.extend(res_list)
        return length+1, tmp_list

    ###不等(M=N-1)
    max_M_N, res01_list = maxLengthCommontSequence(first_list[1:], second_list)
    max_N_M, res02_list = maxLengthCommontSequence(first_list, second_list[1:])
    if max_M_N >= max_N_M:
        return max_M_N, res01_list
    else:
        return max_N_M, res02_list

def mergeSimilarList(first_list, second_list, diff):
    pass

def averageValue(value_list):
    if len(value_list) == 0:
        print(get_cur_info(), 'error! empty value_list')
        sys.exit(0)
    avg = 0
    for v in value_list:
        avg += v
    avg = avg / len(value_list)
    return avg
    
def minMaxValue(value_list):
    if len(value_list) == 0:
        print(get_cur_info(), 'error! empty value_list')
        sys.exit(0)
    max_v = value_list[0]
    min_v = value_list[0]
    for v in value_list:
        if max_v < v:
            max_v = v
        if min_v > v:
            min_v = v
    return min_v, max_v
        
if __name__ == '__main__':
#     print ('n= 1', split2MultiParts('abcdefghijklmn', 1), '\n')
#     print ('n= 2', split2MultiParts('abcdefghijklmn', 2), '\n')
#     print ('n= 3', split2MultiParts('abcdef', 3), '\n')
#     print ('n= 5', split2MultiParts('abcd', 5), '\n')
    x = range(101)
    print(averageValue(x))
    
    
