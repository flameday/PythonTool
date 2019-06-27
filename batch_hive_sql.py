#!/usr/bin/python2
# -*- coding:utf-8 -*-
import codecs
import sys
import os
import datetime
import time
import datetime

en_list = ['utf-8','cp936','gb18030','utf16', 'big5','euc-jp','euc-kr','latin1',]
def read_file_content_en(filename, encoding = 'utf8', ignore_empty = False):
    result_list = []
    fr = codecs.open(filename, 'r', encoding)
    index = 0;
    #print ('filename= ', filename)
    for text in fr:
        index += 1
        text = text.strip('\n')
        text = text.strip()

        if len(text) >= 3 and text[:3] == '---':
            pass
        elif len(text) > 0 and text[0] != '#':
            result_list.append(text)
        elif not ignore_empty:
            result_list.append(text)
    return result_list

def add_to_file(path, content, ignoreLineReturn = False, encoding = None):
    en = 'utf-8'
    if encoding:
        en = encoding
        
    fw = codecs.open(path, 'a+', en)
    #fw.write('|||' + content + '|||\n')
    if ignoreLineReturn:
        fw.write(content)
    else:
        fw.write(content + '\n')
    fw.close()

def clear_to_file(path):
    fw = codecs.open(path, 'w', 'GB18030')
    fw.close()

if __name__ == '__main__':
    if len(sys.argv[1]) < 2:
        print('usage: <program> hive_show_click.sql')
        sys.exit(0)

    filename = sys.argv[1]
    print('filename:', filename)
    c_list = read_file_content_en(filename)

    demo = '\n'.join(c_list) + "\n\n"
    result_list = []

    day = datetime.datetime.now()
    for i in range(21):
    # for i in range(2):
        ddelay = datetime.timedelta(days=21 - i)
        current = day - ddelay
        #print ('date:', time.strftime("%Y-%m-%d", time.localtime()))
        time_value = current.strftime('%Y-%m-%d')
        print('time_value:', time_value)
        result_list.append(demo.replace('2019-06-06', time_value))

    print('\n'.join(result_list) + "\n\n")
    clear_to_file('res.txt')
    add_to_file('res.txt', '\n'.join(result_list) + "\n\n")




