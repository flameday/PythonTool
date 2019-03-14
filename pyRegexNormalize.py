#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

##########################################
#######注意事项:############
#######1.&amp;是XML特殊字符
#######2.在正则表达式中,()等特殊符号需要改为\(\)
#######3.一般来说,Voice当中必须有text,否则无法解析具体含义
##############
##########################################
###需要安装lxml的外部库
from xml.etree.ElementTree import XMLParser, Comment
import xml.etree.ElementTree as ET

import pyString
import pyUsage
import pyIO

def readPinyinXml(path):
    print(pyUsage.get_cur_info(), 'path= ', path)
    parser01 = XMLParser(encoding='gbk')
    
    ###先转为utf-16格式
    c_list = pyIO.read_file_content(path)
  
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
        for rank in child.iter('TYPE_PURE_NUMBER'):
            t1 = rank.find('0').text
            #print(t1.text)
            t2 = rank.find('1').text
            #print(t1.text)
            t3 = rank.find('2').text
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

def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行  
    if element:  
        ############################## 判断element是否有子元素  
        if element.text == None or element.text.isspace(): 
            ############################## 如果element的text没有内容  
            element.text = newline + indent * (level + 1)    
        else:  
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)  
    else:  
        ############################## 此处两行如果把注释去掉，Element的text也会另起一行  
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level  
        pass
    temp = list(element) 
    ############################## 将elemnt转成list  
    
    for subelement in temp:  
        if temp.index(subelement) < (len(temp) - 1): 
            ############################## 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致  
            subelement.tail = newline + indent * (level + 1)  
        else:  
            ############################## 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个  
            subelement.tail = newline + indent * level  
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作  
          
# from xml.etree import ElementTree      #导入ElementTree模块  
# tree = ElementTree.parse('test.xml')   #解析test.xml这个文件，该文件内容如上文  
# root = tree.getroot()                  #得到根元素，Element类  
# prettyXml(root, '\t', '\n')            #执行美化方法  
# ElementTree.dump(root)                 #显示出美化后的XML内容

def addNumber(root):
    id_value = 0    
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '一,幺,One,First')
    d.set('ContentType', 'Number')
    d.set('Model', 'regexNormalize_Number_1.crf_model')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '1'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '幺'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '二,两,Two')
    d.set('ContentType', 'Number')
    d.set('Model', 'regexNormalize_Number_2.crf_model')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '2'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', '二')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', '两')
        e.text = '两'
        
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '年份,数量')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1-9][0-9]{0,3}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Bit)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '月份,年份,数量,值为1~12')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '([1-9]|1[0-2])'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Month')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '座机号码')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1-9]\d{5,7}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Telephone')
        e.text = '{Number(Telephone)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '手机号码')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1]\d{10}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Telephone')
        e.text = '{Number(Telephone)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '其他')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    
def addNumber2English(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '3a')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d[a-zA-Z]'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}{English(Bit)}'

def addNumber2Punctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '百分数')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+%'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'ChinesePrecent')
        e.text = '百分之{Number(Count)}'
        e = ET.SubElement(d, 'Voice')

    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '其他')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(BitIgnorePunctuation)}'

def addNumber2Kanji(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '数量')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+年'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit+Kanji')
        e.text = '{Number(Count)}年'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Bit)}年'
        e = ET.SubElement(d, 'Voice')

    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '数量')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count+Kanji')
        e.text = '{Number(Count)}{Kanji}'

def addNumber2Punctuation2Number2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '2,377,155')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+,\d+,\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'CountIgnorePunctuation')
        e.text = '{Number(CountIgnorePunctuation)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '9:26:01')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+:\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}点{Number(Count)}分{Number(Count)}秒'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '2007-10-31')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d{4,4}-\d{1,2}-\d{1,2}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Date')
        e.text = '{Number(Count)}年{Number(Count)}月{Number(Count)}日'

# def addNumber2Punctuation2Number2Punctuation(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '30%~40%(百分数区间)')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\d+%\~\d+%'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'PercentInterval')
#         e.text = '百分之{Number(Count)}到百分之{Number(Count)}'
            
def addNumber2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '时间,比分')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}点{Number(Count)}分'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Score2Score')
        e.text = '{Number(Count)}比{Number(Count)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '时间,比分')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+-\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}点{Number(Count)}分'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}比{Number(Count)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '时间,比分')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'DecimalChinese')
        e.text = '{Number(Count)}点{Number(Count)}'
    
# def addNumber2Punctuation2English(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '时间,比分')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\d+:\d+'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Time')
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Score2Score')
# 
def addPunctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '笑脸符号')
    d.set('ContentType', 'StringValue')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = ':)'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '笑脸'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '<')
    d.set('ContentType', 'StringValue')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '<'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '小于'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Puctuation')
        e.text = ''

# def addPunctuation2Number2Kanji(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '(2013年')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\(\d+(年|月)'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Redirect')
            
# def addPunctuation2Number2English(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '歼-35S')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '-\d+[A-Z]'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'BitIgnorePunctuation')
        
def addPunctuation2Number2Punctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '(000936)股票证券代码')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\(\d+\)'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Count)}'
    
def addPunctuation2English2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '&nbsp1938/nx')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '&nbsp\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}'

def addPunctuation2Number2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '"9:25 分 -9:30 分 之间')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '-\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '至{Time}'

def addKanji(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'mg')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[^0-9a-zA-Z].*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '{Kanji}'
            
def addEnglish(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'mg')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Unit')
        e.text = '{English(Unit)}'

def addEnglish2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'JX06323')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Bit')
        e.text = '{English(Bit)}{Number(Bit)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '动车,快车,城际列车D632')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Bit')
        e.text = '{English(Bit)}{Number(Bit)}'

def addComplicatedText(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '电子邮件')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '.*@.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'EMail')
        e.text = '{ComplicatedText(Email)}'

def addCombinationText(root):
    ###日期+时间
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))

    d = ET.SubElement(c, 'Node')
    d.set('Comment', '日期+时间')
    d.set('ContentType', 'Part')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    if True:
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '日期')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '时间')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
    
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', '默认顺序是:先具体,后正则;先短后长')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###符号+日期+时间
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '符号+日期+时间')
    d.set('ContentType', 'Part')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    
    if True:
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '符号')
        e.set('ContentType', 'Regex')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = ':'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '日期')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '时间')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'

def addComment(root, text):
    ###日期+时间
    comment = ET.Comment(text)
    root.append(comment)
###########################################################################    
def saveRegexNormalizeConfig(file_name):
    ###构造xml文件
    a = ET.Element('Dictionary')
    if True:
        addComment(a, "这里是基本类型:各个种类长度<=5")
        ###################################### Number2Kanji
        addNumber2Kanji(a)
        ###################################### Number2Number
        addNumber(a)
        ###################################### Number2English
        addNumber2English(a)
        ###################################### Number2Punctuation
        addNumber2Punctuation(a)
        ###################################### Number2Punctuation2Number
        addNumber2Punctuation2Number(a)
#         ###################################### Number2Punctuation2Number2Punctuation
#         addNumber2Punctuation2Number2Punctuation(a)
        ###################################### addNumber2Punctuation2Number2Punctuation2Number
        addNumber2Punctuation2Number2Punctuation2Number(a)
#         ###################################### Number2Punctuation2English
#         addNumber2Punctuation2English(a)
        ###################################### Punctuation
        addPunctuation(a)
#         ###################################### Punctuation2Number2English
#         addPunctuation2Number2English(a)
#         ###################################### Punctuation2Number2Kanji
#         addPunctuation2Number2Kanji(a)
        ###################################### Punctuation2Number2Punctuation
        addPunctuation2Number2Punctuation(a)
        ###################################### Punctuation2English2Number
        addPunctuation2English2Number(a)
        ###################################### Punctuation2Number2Punctuation2Number
        addPunctuation2Number2Punctuation2Number(a)
        ###################################### Kanji
        addKanji(a)     
        ###################################### English
        addEnglish(a)     
        ###################################### English2Number
        addEnglish2Number(a)
    #######################################
    addComment(a, "这里是复杂类型:比如电子邮件,特殊代号")
    if True:
        addComplicatedText(a)
        pass
    #######################################
    addComment(a, "这里是组合类型类型:比如Date+Time,特殊格式符号")
    if True:
        #####
        addCombinationText(a)
        pass
        
        
    prettyXml(a, '\t', '\n')
    text = ET.tostring(a, encoding="gbk", method="xml")
    text = text.decode('gbk')
    
    
    pyIO.clear_to_file(file_name)
    pyIO.add_to_file(file_name, text)
