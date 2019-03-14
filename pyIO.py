#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import codecs
import sys
import os
import pyLog
import pyString

def clear_to_file(path):
    fw = codecs.open(path, 'w', 'GB18030')
    fw.close()
    
def add_to_file(path, content, ignoreLineReturn = False, encoding = None):
    en = 'GB18030'
    if encoding:
        en = encoding
        
    fw = codecs.open(path, 'a+', en)
    #fw.write('|||' + content + '|||\n')
    if ignoreLineReturn:
        fw.write(content)
    else:
        fw.write(content + '\n')
    fw.close()

###dist含义是:每隔dist行,选择一行
def read_file_content(path, encoding = None, dist = 0):
    result_list = []
    
    en = 'GB18030'
    if encoding:
        en = encoding
    fr = codecs.open(path, 'r', en)
    index = 0;
    for text in fr:
        index += 1
        if dist != 0 and index % dist != 0:
            #print '-----ignore! index= %d'%index
            continue
        
        tmp = text.replace('\r\n','')
        tmp = tmp.replace('\n','')
        tmp = tmp.replace('\t', ' ')
        result_list.append(tmp)
    return result_list

en_list = ['ucs-bom','utf-8','cp936','gb18030','utf16', 'big5','euc-jp','euc-kr','latin1',]
def tryDecode(data):
    res = ''
    for en in en_list:
        try:
            res = data.decode(en)
            break
        except:
            pass
    return res
    
def tryReadFile(file):
    if not os.path.exists(file):
        pyLog.logging.error('error! not exists file: %s'%file)
        sys.exit(0)
        
    c_list = []
    for en in en_list:
        try:
            c_list = read_file_content(file, en)
            break
        except:
            pass
    return c_list

def subDirs(path):
    file_list = []
    dir_list = []
    for i in os.listdir(path):
        sub_path = path + os.sep + i 
        sub_path = sub_path.replace(os.sep + os.sep, os.sep)
        if os.path.isfile(sub_path):
            file_list.append(sub_path)
        elif os.path.isdir(sub_path):
            dir_list.append(sub_path)
    return file_list, dir_list
        
def traversalDir(path):
    file_list = []
    dir_list = []
    for i in os.listdir(path):
        sub_path = path + os.sep + i 
        sub_path = sub_path.replace(os.sep + os.sep, os.sep)
        if os.path.isfile(sub_path):
            file_list.append(sub_path)
        elif os.path.isdir(sub_path):
            dir_list.append(sub_path)
            pass
            sub_file_list, sub_dir_list = traversalDir(sub_path)
            file_list.extend(sub_file_list)
            dir_list.extend(sub_dir_list)
            pass
    return file_list, dir_list

def generateFileByCurrentScripyName(label):
    current_file = os.path.realpath(sys.argv[0])
    pos = current_file.rfind(os.sep)
    pos02 = current_file.rfind('.')
    path = current_file[:pos]
    file = current_file[pos + 1:pos02]
    suf = current_file[pos + 1:]
    
    label = pyString.removeHeadTailSpace(label)
    if len(label) == 0:
        pyLog.logging.info('error! label is 0')
        sys.exit(0)
    
    return path, file+label

def FormatEncoding(IN_FILE, IN_ENCODING, OUT_FILE, OUT_ENCODING):
    fp = open(IN_FILE, 'rb')
    index = 0
    text_list = []
    while True:
        eachline = fp.readline()
        if not eachline:
            break

        ###打印信息
        index += 1
        if (index + 1) % 10000 == 0:
            print ('index= %d'%index)
        try:
            text = eachline.decode(IN_ENCODING, 'replace')
            text.encode(OUT_ENCODING)
            text_list.append(text)
        except:
            #print 'bad index= %d'%index
            pass

    f = codecs.open(OUT_FILE, 'w', OUT_ENCODING)
    f.write(''.join(text_list))
    f.close()
    
import filecmp 
def isFileEqual(file01, file02):
    ###相等返回True
    return filecmp.cmp(file01, file02)

def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def currentDirFile():
    current_file = os.path.realpath(sys.argv[0])
    pos = current_file.rfind(os.sep)
    current_dir = current_file[:pos + 1]
    current_file = current_file[pos + 1:]
    return current_dir, current_file