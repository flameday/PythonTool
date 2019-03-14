#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os
import pyString
import pyUsage
import pyXml

def getDefaultKanji(diff):
    return '--KANJI--'
###默认的特征
def getDefaultText(diff):
#     return '--TEXT--'
    if diff < 0:
        return '--TEXT-%d--'%(abs(diff))
    return '--TEXT+%d--'%(abs(diff))

def getDefaultPos(diff):
#     return '--TEXT--'
    if diff < 0:
        return '--POS-%d--'%(abs(diff))
    return '--POS+%d--'%(abs(diff))

def genCharaDiffList(chara_cnt = 5):
    res_list = []
    for i in range(chara_cnt):
        res_list.append(-1*(i+1))
        res_list.append(1*(i+1))
    return res_list

###提取CRF训练特征:字
def generateKanjiInfo(w_c_list, sen_id, index, sub_index, chara_cnt = 5):
    positive_res_list = []
    negtive_res_list = []
    
    ###目前增加逻辑:如果遇到逗号,那么后面的就不解析了.
    positive_valid_flag = True
    negtive_valid_flag = True
    
    for diff in genCharaDiffList(chara_cnt):
        if (index+diff) >= 0 and (index+diff) < len(w_c_list):
            word = w_c_list[index+diff][0] ###词
            ###针对逗号进行屏蔽
            if word == '，':
                if diff > 0:
                    positive_valid_flag = False
                if diff < 0:
                    negtive_valid_flag = False
            if diff < 0 and negtive_valid_flag:
                negtive_res_list.extend(word[::-1])###对Word逆序
            if diff > 0 and positive_valid_flag:
                positive_res_list.extend(word)
    ###如果不够10个字,就加上DefaultKanJi
    print('negtive_res_list= ', negtive_res_list)
    print('positive_res_list= ', positive_res_list)
    negtive_res_list.extend([getDefaultKanji(diff),]*10)
    positive_res_list.extend([getDefaultKanji(diff),]*10)
    ###找到index的位置
    negtive_invalid_index = [i for i,e in enumerate(negtive_res_list) if e == getDefaultKanji(diff)]
    negtive_invalid_index = negtive_invalid_index[0]
    positive_invalid_index = [i for i,e in enumerate(positive_res_list) if e == getDefaultKanji(diff)]
    positive_invalid_index = positive_invalid_index[0]
    
    res_list = []
    for i in range(10):
        res_list.append(negtive_res_list[i])
        res_list.append(positive_res_list[i])
    res_list.append('%s'%negtive_invalid_index)
    res_list.append('%s'%positive_invalid_index)
    return res_list
    
###提取CRF训练特征:词+词性
def generateCharacteristicInfo(w_c_list, sen_id, index, sub_index, chara_cnt = 5):
    length = len(w_c_list)
    w,c = w_c_list[index]
    relate_info = ['%d'%sen_id,]###句子ID
    relate_info.append('%s'%index)
    relate_info.append(w)
    relate_info.append(c)
    relate_info.append('%d'%len(w))
    relate_info.append('%d'%sub_index)

    #for diff in [-1,1,-2,2,-3,3,-4,4,-5,5]:

    ###目前增加逻辑:如果遇到逗号,那么后面的就不解析了.
    positive_valid_flag = True
    negtive_valid_flag = True
    
    for diff in genCharaDiffList(chara_cnt):
        text = getDefaultText(diff)
        pos = getDefaultPos(diff)
        if (index+diff) >= 0 and (index+diff) < length:
            word = w_c_list[index+diff][0] ###词
            chara = w_c_list[index+diff][1]  ###词性

            ###针对逗号进行屏蔽
            if word == '，':
                if diff < 0:
                    negtive_valid_flag = False
                if diff > 0:
                    positive_valid_flag = False
            if diff > 0 and positive_valid_flag:
                text = word
                pos = chara
            if diff < 0 and negtive_valid_flag:
                text = word
                pos = chara
                
        relate_info.append(text)
        relate_info.append(pos)
    ###加上字的信息
    print(pyUsage.get_cur_info(True), 'relate_info= ', relate_info)
    #t_list = generateKanjiInfo(w_c_list, sen_id, index, sub_index, chara_cnt = 5)
    #print(pyUsage.get_cur_info(True), 'relate_info= ', relate_info)
    #relate_info.extend(t_list)
    return relate_info

# ###提取CRF训练特征
# def extract_Characteristic(sen_id, w_c_list, word):
#     d_characteristic_list = []
#     for index,info in enumerate(w_c_list):
#         w,c = info
#         pos_list = [i for i,e in enumerate(w) if e == word]
#         for val in pos_list:
#             r_info = generateCharacteristicInfo(w_c_list, sen_id, index, val) 
#             d_characteristic_list.append(r_info)
#     return d_characteristic_list

def locateIndexSubindex(w_c_list, total_index):
    length = 0
    index = 0
    sub_index = 0
    for i, wc_info in enumerate(w_c_list):
        w, c = wc_info
        length += len(w)
#         print(get_cur_info(), 'i, w,c= ', i, w, c, 'length= ', length, 'ind, sub_ind=', index, sub_index)
        if length > total_index:
            index = i
            sub_index = total_index - (length - len(w))
            break

    return index, sub_index    