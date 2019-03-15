# python2
# coding = utf-8
import io,shutil
import codecs
import sys
import os
import datetime
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

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


tmp_list = read_file_content_en(sys.argv[1])
j = json.loads(''.join(tmp_list))
print('\n\n\n')
print(json.dumps(j))
print('\n\n\n')


