#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

###需要安装lxml的外部库
from xml.etree.ElementTree import XMLParser
import xml.etree.ElementTree as ET

import pyString
import pyUsage
import pyIO

def compareValue(e, split = ''):
    return e['PinYin'] + split + e['PartOfSpeech']

def simpleArrayList(old_dict_list):
    old_list = [compareValue(e, '-') for e in old_dict_list]
    return old_list
    
def sortedCompareValueList(old_dict_list, split = ''):
    old_list = [compareValue(e, split) for e in old_dict_list]
    old_list.sort()
    return old_list
    
def singleItem(old_dict_list):
    ###第0步,list本身内部去重
    flag_dict = {}
    res_list = []
    for e in old_dict_list:
        flag = e['PinYin'] + e['PartOfSpeech']
        if flag in flag_dict:
            pass
        else:
            flag_dict[flag] = True
            res_list.append(e)
    return res_list

def readPinyinXmlDict(path, ignore_duplicate = False):
    lang, name, word_info_list = readPinyinXml(path)
    res_dict = {}
    for e in word_info_list:
        if e[0] in res_dict and not ignore_duplicate:
            print('error! duplicate key: ', e)
            sys.exit(0)
        res_dict[e[0]] = e[1]
    print(pyUsage.get_cur_info(), 'len(res_dict)=', len(res_dict), path)
    
    return lang, name, res_dict
    
def readPinyinXml(path):
    print(pyUsage.get_cur_info(), 'path= ', path)
    
    parser01 = XMLParser(encoding='gbk')
    
    ###先转为utf-16格式
    c_list = pyIO.read_file_content(path)
  
#     ###过滤转义符:
#     for i, e in enumerate(c_list):
#         while True:
#             t = pyString.reExtractData('(&#\d\d\d;)', e, 1)
#             if len(t) > 0:
#                 print('reExtractData t= ', t)
#                 c_list[i] = e.replace(t, '')
#                 e = c_list[i]
#                 print('ignore ', t)
#                 print('c_list[i]= ', c_list[i])
#                 pass
#             else:
#                 break
    
#     ###查找转义符
#     strip_line = [reExtractData('(&#\d+;)', e, 1) for e in c_list if e.find('&#') != -1]
#     strip_line = list(set(strip_line))
#     if len(strip_line) > 0:
#         print(strip_line)
#         print(path)
#         sys.exit(0)
    
    flag = 'encoding="GBK"'
    flag.lower()
    pos = [i for i,e in enumerate(c_list) if e.find(flag) != -1]
    #print('pos= ', pos)
    
    if len(pos) == 0:
        s_flag = 'encoding=\'gbk\''
        pos = [i for i,e in enumerate(c_list) if e.find(s_flag) != -1]
        if len(pos) > 0:
            c_list[pos[0]] = c_list[pos[0]].replace('\'gbk\'', '"GBK"')
            #print(' 2 pos= ', pos)
    if len(pos) == 0:
        s_flag = 'encoding=\'GBK\''
        pos = [i for i,e in enumerate(c_list) if e.find(s_flag) != -1]
        c_list[pos[0]] = c_list[pos[0]].replace('\'GBK\'', '"GBK"')
        #print(' 3 pos= ', pos)

    #c_list[pos[0]].replace('encoding="GBK"', 'encoding="utf-8"')
    #print ('           item= ', c_list[pos[0]])
    t = '\n'.join(c_list)

    ###读入数据
    root = ET.fromstring(t)
    
    ###文件头
    lang = ''
    name = ''
    for i,child in enumerate(root[:1]):
        l = child.find('DictionaryLanguage')
        lang= l.text
        n = child.find('DictionaryName')
        name = n.text
    
    ###遍历数据
    word_info_list = []
    for i,child in enumerate(root[1:]):
        ###查找单词
        word = child.find('Word')
        #print(word.text)

        ###查找拼音
        pro_list = []
        for rank in child.iter('Pronunciation'):
            t1 = rank.find('ProID').text
            #print(t1.text)
            t2 = rank.find('PartOfSpeech').text
            #print(t1.text)
            t3 = rank.find('PinYin').text
            #print(t1.text)
            t4 = rank.find('BianDiao').text
            #print(t1.text)
            if not t1:
                t1 = ''
            if not t2:
                t2 = ''
            if not t3:
                t3 = ''
            if not t4:
                t4 = ''
            
            tmp_dict = {
                    'ProID':        t1,
                    'PartOfSpeech': t2,
                    'PinYin':       t3,
                    'BianDiao':     t4,
                    }
            pro_list.append(tmp_dict)
            if not t3:
                print(word.text, tmp_dict)
                sys.exit(0)      

        pro_list = singleItem(pro_list)
        word_info_list.append((word.text, pro_list))

    return lang, name, word_info_list

def checkMultiKey(word_info_list):
    mul_word_list = []
    
    word_info_dict = {}
    for i, (word, pro_list) in enumerate(word_info_list):
        ###添加到词典
        if word in word_info_dict:
            old_list = word_info_dict[word]
            ###记录有问题的汉字
            mul_word_list.append(word)
            ###剩下的拼音去重处理
            for pro in pro_list:
                pos_list = [e for e in word_info_dict[word] if e == pro]
                if len(pos_list) > 0:
                    pass
                else:
                    word_info_dict[word].append(pro)

            print(pyUsage.get_cur_info(), word, 'bad duplicate:')
            ###打印旧的
            for e in old_list:
                print('====', e)
            print('')
            ###打印新的
            for e in pro_list:
                print('----', e)
            print('')
            ###打印
            for e in word_info_dict[word]:
                print('>>>>', e)
            print('\n')
        else:
            word_info_dict[word] = pro_list
    return mul_word_list, word_info_dict
    
def saveWordPronunceList2WordPinyinXml(file_name, lang, name, word_info_dict):
    ###dict2list
    tmp_list = []
    for k in word_info_dict:
        tmp_list.append((k, word_info_dict[k]))
    print(pyUsage.get_cur_info(), 'len(tmp_list)= ', len(tmp_list))
    
    tmp_list.sort(key=xml_sort_list)
    
    ###构造xml文件
    a = ET.Element('Dictionary')
    
    b = ET.SubElement(a, 'DictionaryHeader')
    c = ET.SubElement(b, 'DictionaryLanguage')
    c.text = lang
    d = ET.SubElement(b, 'DictionaryName')
    d.text = name
    
    for index,py_list in enumerate(tmp_list):
        w = py_list[0]###.lower()
        b = ET.SubElement(a, 'DictionaryEntry')
        c = ET.SubElement(b, 'Word')
        c.text = w
#         if w == '上':
#             print(py_list)
        
        for i,pro_dict in enumerate(py_list[1]):
            d = ET.SubElement(b, 'Pronunciation')
            e = ET.SubElement(d, 'ProID')
            #e.text = '%s'%pro_dict['ProID']
            ###重新更改ProgID
            e.text = '%d'%(i+1)
        
            f = ET.SubElement(d, 'PartOfSpeech')
            f.text = pro_dict['PartOfSpeech']
        
            g = ET.SubElement(d, 'PinYin')
            g.text = pro_dict['PinYin']
        
            h = ET.SubElement(d, 'BianDiao')
            h.text = pro_dict['BianDiao']

    text = ET.tostring(a, encoding="gbk", method="xml")
    text = text.decode('gbk')

    text = text.replace('version=\'1.0\'', 'version="1.0"')
    text = text.replace('encoding=\'gbk\'', 'encoding="GBK"')
    text = text.replace('<DictionaryHeader>', '\n<DictionaryHeader>')
    text = text.replace('</DictionaryHeader>', '</DictionaryHeader>\n')
    text = text.replace('</DictionaryEntry>', '</DictionaryEntry>\n')
    
    ###由于多加了空格,目前不知道怎么做比较好,这里去除
    text = text.replace('<PartOfSpeech />', '<PartOfSpeech></PartOfSpeech>')
    text = text.replace('<BianDiao />', '<BianDiao></BianDiao>')
    ###这里补充空格:xp用bash改写过xml
    lapse_space = ' '
    if file_name.find('multi_han.xml') != -1:
        lapse_space = ''
    text = text.replace('<DictionaryHeader>', lapse_space + '<DictionaryHeader>')
    text = text.replace('<DictionaryEntry>',  lapse_space + '<DictionaryEntry>')

    pyIO.clear_to_file(file_name)
    pyIO.add_to_file(file_name, text)

def xml_sort_list(text_list):
    return text_list[0].encode('gb18030')
    
def xml_sort(text):
    return text.encode('gb18030')#text#.encode('utf8')
    
    
# def save2WordTimitXml(file_name, file_description, word_timit_dict, word_list):
#     ###构造xml文件
#     a = ET.Element('Dictionary')
#     
#     b = ET.SubElement(a, 'DictionaryHeader')
#     c = ET.SubElement(b, 'DictionaryLanguage')
#     c.text = 'en'
#     d = ET.SubElement(b, 'DictionaryName')
#     d.text = file_description
#     
#     for i in xrange(len(word_list)):
#         w = word_list[i]###.lower()
#         b = ET.SubElement(a, 'DictionaryEntry')
#         c = ET.SubElement(b, 'Word')
#         c.text = w
#         
#         timit_list = word_timit_dict[w.upper()]
#         for i in xrange(len(timit_list)):
#             timit = timit_list[i]
#             d = ET.SubElement(b, 'Pronunciation')
#             e = ET.SubElement(d, 'ProID')
#             e.text = '%s'%(i+1)
#             
#             f = ET.SubElement(d, 'PartOfSpeech')
#             f.text = ' '
#             
#             g = ET.SubElement(d, 'PinYin')
#             timit = changeDoubleSpace2SingleSpace(timit)
#             timit = removeHeadTailSpace(timit)
#             g.text = timit
#             
#             h = ET.SubElement(d, 'BianDiao')
#             h.text = ' '
# 
#     # PrintObjectInfo(ET)
#     text = ET.tostring(a)
#     text = text.replace('<DictionaryHeader>', '\n<DictionaryHeader>')
#     text = text.replace('</DictionaryHeader>', '</DictionaryHeader>\n')
#     text = text.replace('</DictionaryEntry>', '</DictionaryEntry>\n')
# 
#     ###由于多加了空格,目前不知道怎么做比较好,这里去除
#     text = text.replace('<PartOfSpeech> </PartOfSpeech>', '<PartOfSpeech></PartOfSpeech>')
#     text = text.replace('<BianDiao> </BianDiao>', '<BianDiao></BianDiao>')
#     ###这里补充空格
#     text = text.replace('<DictionaryHeader>', '    <DictionaryHeader>')
#     text = text.replace('<DictionaryEntry>',  '    <DictionaryEntry>')
# 
#     clear_to_file(file_name)
#     add_to_file(file_name, '<?xml version="1.0" encoding="GBK"?>')
#     add_to_file(file_name, text)
# 
# def save2Word_MultiTimitXml(file_name, file_description, word_timit_dict, word_list):
#     ###构造xml文件
#     a = ET.Element('Dictionary')
#     
#     b = ET.SubElement(a, 'DictionaryHeader')
#     c = ET.SubElement(b, 'DictionaryLanguage')
#     c.text = 'en'
#     d = ET.SubElement(b, 'DictionaryName')
#     d.text = file_description
#     
#     for i in xrange(len(word_list)):
#         w = word_list[i]###.lower()
#         b = ET.SubElement(a, 'DictionaryEntry')
#         c = ET.SubElement(b, 'Word')
#         c.text = w
#         
#         timit_chara_list = word_timit_dict[w.upper()]
#         for i in xrange(len(timit_chara_list)):
#             timit_chara = timit_chara_list[i]
# 
#             ###部分情况下,timit是空,例如"id"
#             if timit_chara[0] is None or len(timit_chara[0]) == 0:
#                 continue
#                 
#             d = ET.SubElement(b, 'Pronunciation')
#             e = ET.SubElement(d, 'ProID')
#             e.text = '%s'%(i+1)
#             
#             f = ET.SubElement(d, 'PartOfSpeech')
#             f.text = timit_chara[1]
#             if len(f.text) == 0:
#                 f.text = ' '
#             
#             g = ET.SubElement(d, 'PinYin')
#             g.text = timit_chara[0]
#             
#             h = ET.SubElement(d, 'BianDiao')
#             h.text = ' '
# 
#     # PrintObjectInfo(ET)
#     text = ET.tostring(a)
#     text = text.replace('<DictionaryHeader>', '\n<DictionaryHeader>')
#     text = text.replace('</DictionaryHeader>', '</DictionaryHeader>\n')
#     text = text.replace('</DictionaryEntry>', '</DictionaryEntry>\n')
# 
#     ###由于多加了空格,目前不知道怎么做比较好,这里去除
#     text = text.replace('<PartOfSpeech> </PartOfSpeech>', '<PartOfSpeech></PartOfSpeech>')
#     text = text.replace('<BianDiao> </BianDiao>', '<BianDiao></BianDiao>')
#     ###这里补充空格
#     text = text.replace('<DictionaryHeader>', '    <DictionaryHeader>')
#     text = text.replace('<DictionaryEntry>',  '    <DictionaryEntry>')
# 
#     clear_to_file(file_name)
#     add_to_file(file_name, '<?xml version="1.0" encoding="GBK"?>')
#     add_to_file(file_name, text)
# 
# 
