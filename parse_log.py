#!/usr/bin/python2
import codecs
import sys
import os
import datetime

en_list = ['utf-8','cp936','gb18030','utf16', 'big5','euc-jp','euc-kr','latin1',]
def read_file_content_en(filename, encoding = 'utf8', ignore_empty = True):
    result_list = []
    fr = codecs.open(filename, 'r', encoding)
    index = 0;
    #print ('filename= ', filename)
    for text in fr:
        index += 1
        text = text.strip('\n')
        text = text.strip()
        if len(text) > 0 and text[0] != '#':
            result_list.append(text)
        elif not ignore_empty:
            result_list.append(text)
    return result_list

def is_good_line(line):
    line = line.strip()
    if len(line) > 0:
        return True
    return False
def trimTime(line):
    pos1 = line.find('[')
    if pos1 != -1:
        return line[pos1:]
    return line

def get_prefix(line):
    pos1 = line.find('[')
    pos2 = line.find(']')
    if pos1 != -1 and pos2 != -1:
        return line[pos1:pos2+1]
    return ''

def takeSecond(elem):
    return elem[1]
if __name__ == '__main__':
    filename = sys.argv[1]
    ###print('filename:', filename)

    c_list = read_file_content_en(filename)
    ###find ']'
    count_dict = {}
    item_dict = {}

    ###print(c_list[:3])
    for i,c in enumerate(c_list):
        if not is_good_line(c):
            print("bad line:", c)
            continue
        prefix = get_prefix(c)
        if prefix not in count_dict:
            count_dict[prefix] = 0
            item_dict[prefix] = trimTime(c)
        v = count_dict[prefix]
        count_dict[prefix] = v+1
    ###sort
    sort_list = []
    for k, v in count_dict.items():
        sort_list.append((k, v))
    sort_list.sort(key = takeSecond)
    ###print
    print '\n'+filename
    for k,v in sort_list[::-1]:
        print '%-6d'%v, item_dict[k]
    print '\n'




